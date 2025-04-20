import argparse
import logging
import os
import sys

from .plausipy import Plausipy, Profile
from .utils import get_caller_package_name, setup_debug_logger

# logging
logger = logging.getLogger(__name__)

# check if PLAUSIPY_DEBUG is enabled
if "PLAUSIPY_DEBUG" in os.environ:
    setup_debug_logger(logger)


# - lib / run
def lib(
    key: str = None,
    profile: Profile = Profile.PACKAGE,
    require_consent: bool = False,
    endpoint: str = None,
):
    # get caller package name
    package_name = get_caller_package_name()

    # instantiate plausipy
    pp = Plausipy(
        app_name=package_name,
        app_key=key,
        profile=profile,
        require_consent=require_consent,
        start=False,
        endpoint=endpoint,
    )

    # register cli
    _ppcli(pp)

    if not Plausipy.hasMainPackage():
        logger.warning(
            "No main package found, consent will be asked for %s", package_name
        )

        # set first lib that registers as main package if no main package is set
        # NOTE: on purpose, an error will be thrown if a main package tries to register after
        #       one of it's lib packages which indicates, that the main app didn't follow the
        #       rules of initializing plausipy at the beginning
        Plausipy.setMainPackage(pp)

        # ask for consent
        # Plausipy.askForConsent()

    # return plausipy
    return pp


# - app / package
def app(
    key: str = None,
    profile: Profile = Profile.PACKAGE,
    endpoint: str = None,
    # delay_consent: bool = False,
    require_consent: bool = False,
) -> Plausipy | None:
    # get caller package name
    package_name = get_caller_package_name()

    # initialize plausipy
    pp = Plausipy(
        app_name=package_name,
        app_key=key,
        profile=profile,
        require_consent=require_consent,
        start=False,
        endpoint=endpoint,
    )

    # register cli
    _ppcli(pp)

    # register as main package
    # NOTE: - there must only be one main package be registered
    #       - main package will be resonsible for asking for collective consent
    Plausipy.setMainPackage(pp)

    # check for consent
    # TODO: we could consider registering an exit event that enforces the consent to be
    #       asked before the program exits if the developer did not implement the
    #       plausipy.consent() call as required.
    # if not delay_consent:
    #     Plausipy.askForConsent()

    # start plausipy
    pp.start()


def get(
    name: str | None = None,
) -> Plausipy:
    # get plausipy
    if name is None:
        name = get_caller_package_name()

    # get plausipy by name
    for pp in Plausipy._pps:
        if pp._app_name == name:
            logger.debug("Plausipy for %s found", name)
            return pp

    # raise error
    raise ValueError(f"Plausipy for {name} not found")


def setData(**kwargs) -> None:
    pp = get()
    if pp is not None:
        pp.setData(**kwargs)


def consent() -> None:
    pp = get()
    assert pp._is_main, "Consent should only be asked for the main package"
    Plausipy.askForConsent()


# -------------------------------


def _ppcli(pp: Plausipy) -> None:
    # capture argument outside of argparse (to also work under -h / --help flags, defining rhe argument in the parser only is for meta then)
    pp.disabled = "--no-tracking" in sys.argv

    # print plausipy
    if "--plausipy-print" in sys.argv:
        Plausipy._print_payload_before_terminate = True

    # profile
    if "--plausipy-profile" in sys.argv:
        _arg_i = sys.argv.index("--plausipy-profile")
        _profile = sys.argv[_arg_i + 1] if _arg_i + 1 < len(sys.argv) else None
        if _profile is not None and _profile in Profile.__members__:
            pp._requested_profile = Profile[_profile]


def argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--no-tracking", action="store_true", help="Disable tracking by plausipy"
    )
    parser.add_argument(
        "--plausipy-print", action="store_true", help="Disable tracking by plausipy"
    )
    parser.add_argument(
        "--plausipy-profile",
        type=str,
        help="Set the profile for plausipy",
        choices=[s.name for s in Profile],
    )
