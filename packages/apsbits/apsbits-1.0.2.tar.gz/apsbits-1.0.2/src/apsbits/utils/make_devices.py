"""
Make devices from YAML files
=============================

Construct ophyd-style devices from simple specifications in YAML files.

.. autosummary::
    :nosignatures:

    ~make_devices
    ~Instrument
"""

import logging
import pathlib
import sys
import time

import guarneri
from apstools.plans import run_blocking_function
from apstools.utils import dynamic_import
from bluesky import plan_stubs as bps

from apsbits.utils.aps_functions import host_on_aps_subnet
from apsbits.utils.config_loaders import get_config
from apsbits.utils.config_loaders import load_config_yaml
from apsbits.utils.controls_setup import oregistry  # noqa: F401

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

MAIN_NAMESPACE = "__main__"


def _get_make_devices_log_level() -> int:
    """(internal) User choice for log level used in 'make_devices()'."""
    level = get_config().get("MAKE_DEVICES", {}).get("LOG_LEVEL", "info")
    if isinstance(level, str):
        # Allow log level as str or int in iconfig.yml.
        level = logging._nameToLevel[level.upper()]
    return level


def make_devices(
    *, pause: float = 1, clear: bool = True, file: str | pathlib.Path | None = None
):
    """
    (plan stub) Create the ophyd-style controls for this instrument.

    Feel free to modify this plan to suit the needs of your instrument.

    EXAMPLE::

        RE(make_devices())  # Use default iconfig.yml
        RE(make_devices(file="custom_devices.yml"))  # Use custom devices file

    PARAMETERS

    pause : float
        Wait 'pause' seconds (default: 1) for slow objects to connect.
    clear : bool
        Clear 'oregistry' first if True (the default).
    file : str | pathlib.Path | None
        Optional path to a custom YAML/TOML file containing device configurations.
        If provided, this file will be used instead of the default iconfig.yml.
        If None (default), uses the standard iconfig.yml configuration.

    """
    logger.debug("(Re)Loading local control objects.")

    if clear:
        log_level = _get_make_devices_log_level()

        main_namespace = sys.modules[MAIN_NAMESPACE]
        for dev_name in oregistry.device_names:
            # Remove from __main__ namespace any devices registered previously.
            if hasattr(main_namespace, dev_name):
                logger.log(log_level, "Removing %r from %r", dev_name, MAIN_NAMESPACE)
                delattr(main_namespace, dev_name)

        oregistry.clear()

    if file is not None:
        # Use the provided file directly
        device_path = pathlib.Path(file)
        if not device_path.exists():
            logger.error("Device file not found: %s", device_path)
            return
        logger.info("Loading device file: %s", device_path)
        try:
            yield from run_blocking_function(_loader, device_path, main=True)
        except Exception as e:
            logger.error("Error loading device file %s: %s", device_path, str(e))
            return
    else:
        # Use standard iconfig.yml configuration
        iconfig = get_config()

        instrument_path = pathlib.Path(iconfig.get("INSTRUMENT_PATH")).parent
        configs_path = instrument_path / "configs"

        # Get device files and ensure it's a list
        device_files = iconfig.get("DEVICES_FILES", [])
        if isinstance(device_files, str):
            device_files = [device_files]
        logger.debug("Loading device files: %r", device_files)

        # Load each device file
        for device_file in device_files:
            device_path = configs_path / device_file
            if not device_path.exists():
                logger.error("Device file not found: %s", device_path)
                continue
            logger.info("Loading device file: %s", device_path)
            try:
                yield from run_blocking_function(_loader, device_path, main=True)
            except Exception as e:
                logger.error("Error loading device file %s: %s", device_path, str(e))
                continue

        # Handle APS-specific device files if on APS subnet
        aps_control_devices_files = iconfig.get("APS_DEVICES_FILES", [])
        if isinstance(aps_control_devices_files, str):
            aps_control_devices_files = [aps_control_devices_files]

        if aps_control_devices_files and host_on_aps_subnet():
            for device_file in aps_control_devices_files:
                device_path = configs_path / device_file
                if not device_path.exists():
                    logger.error("APS device file not found: %s", device_path)
                    continue
                logger.info("Loading APS device file: %s", device_path)
                try:
                    yield from run_blocking_function(_loader, device_path, main=True)
                except Exception as e:
                    logger.error(
                        "Error loading APS device file %s: %s", device_path, str(e)
                    )
                    continue

    if pause > 0:
        logger.debug(
            "Waiting %s seconds for slow objects to connect.",
            pause,
        )
        yield from bps.sleep(pause)

    # Configure any of the controls here, or in plan stubs


def _loader(yaml_device_file, main=True):
    """
    Load our ophyd-style controls as described in a YAML file.

    PARAMETERS

    yaml_device_file : str or pathlib.Path
        YAML file describing ophyd-style controls to be created.
    main : bool
        If ``True`` add these devices to the ``__main__`` namespace.

    """
    logger.debug("Devices file %r.", str(yaml_device_file))
    t0 = time.time()
    _instr.load(yaml_device_file)
    logger.info("Devices loaded in %.3f s.", time.time() - t0)

    if main:
        log_level = _get_make_devices_log_level()

        main_namespace = sys.modules[MAIN_NAMESPACE]
        for label in oregistry.device_names:
            logger.log(log_level, "Adding ophyd device %r to main namespace", label)
            setattr(main_namespace, label, oregistry[label])


class Instrument(guarneri.Instrument):
    """Custom YAML loader for guarneri."""

    def parse_yaml_file(self, config_file: pathlib.Path | str) -> list[dict]:
        """Read device configurations from YAML format file."""
        if isinstance(config_file, str):
            config_file = pathlib.Path(config_file)

        def parser(creator, specs):
            if creator not in self.device_classes:
                self.device_classes[creator] = dynamic_import(creator)
            entries = [
                {
                    "device_class": creator,
                    "args": (),  # ALL specs are kwargs!
                    "kwargs": table,
                }
                for table in specs
            ]
            return entries

        with open(config_file, "r") as f:
            config_data = load_config_yaml(f)

            devices = [
                device
                # parse the file using already loaded config data
                for k, v in config_data.items()
                # each support type (class, factory, function, ...)
                for device in parser(k, v)
            ]
        return devices


_instr = Instrument({}, registry=oregistry)  # singleton
