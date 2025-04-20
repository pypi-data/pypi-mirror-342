import json
import logging
import os
import uuid
from datetime import datetime

import requests
import safe_exit

from .error import PlausipyError
from .info import (
    _print_box,
    show_setup_plausipy_box,
    show_tracking_info,
    show_tracking_required,
)
from .paths import DATA_DIR
from .user import Consent, ConsentManager, IDManager, Profile
from .utils import (
    get_localtion_data,
    get_package_tree,
    get_package_version,
    get_python_data,
    get_system_data,
    get_usage_data,
)

# logger
logger = logging.getLogger(__name__)

# api endpoint
API_ENDPOINT = "https://plausipy.com/api/records"


class Record:
    @classmethod
    def getUserLocation(cls):
        if not hasattr(cls, "_user_location"):
            cls._user_location = get_localtion_data()
        return cls._user_location

    @classmethod
    def getUserUsage(cls):
        if not hasattr(cls, "_user_usage"):
            cls._user_usage = get_usage_data()
        return cls._user_usage

    @classmethod
    def getUserSystem(cls):
        if not hasattr(cls, "_user_system"):
            cls._user_system = get_system_data()
        return cls._user_system

    @classmethod
    def getUserPython(cls):
        if not hasattr(cls, "_user_python"):
            cls._user_python = get_python_data()
        return cls._user_python


class PlausipyConsent:
    def __init__(self, package: str):
        self._package: str = package
        self._asked: bool = False
        self._allowed_once: bool = False
        self._denied_once: bool = False

    @property
    def hasBeenAsked(self) -> bool:
        return self._asked

    def asked(self, value: bool = True):
        self._asked = value

    def allowOnce(self):
        self._allowed_once = True

    def denyOnce(self):
        self._denied_once = True

    @property
    def value(self) -> Consent:
        return ConsentManager.get().getPackageConsent(self._package)

    @property
    def granted(self) -> bool:
        return (
            self.value == Consent.ALLOW
            or self == Consent.ASK
            and self.hasBeenAsked
            or self._allowed_once
        ) and not self._denied_once

    # make comparable
    def __eq__(self, other):
        consent: Consent = self.value
        if isinstance(other, Consent):
            return consent == other
        elif isinstance(other, PlausipyConsent):
            return consent == other.value
        elif isinstance(other, str) and other in [c.value for c in Consent]:
            return consent.value == other
        return NotImplemented


class Plausipy:
    _id = str(uuid.uuid4())
    _pps: list = []
    _termination_event_registered = False
    _print_payload_before_terminate = False
    _has_asked_for_consent = False

    @classmethod
    def registerTerminationEvent(cls, key: str):
        """
        Register safe exit once
        """

        # check if already registered
        if cls._termination_event_registered:
            logger.info("Termination event already registered.")
            return

        # register
        safe_exit.register(cls.terminate)
        cls._termination_event_registered = True

    @classmethod
    def terminate(cls):
        """
        Indicate to plausipy that the trackable execution has ended.
        This usually meand that the program is terminated.
        """

        # TODO: maybe disabled on class level makes more sense when it's a user input, however, we also want
        #       to allow disabling tracking on a package level while dependency tracking is still active.

        #  log
        logger.info("Terminating plausipy")

        # DEBUG / WARNING
        # NOTE: upon safe_exit the stdin is closed and we cannot display the interactive modal.
        #       however, whith multiple libraries using plausipy and no main app acting as orchestrator we only have the following options
        #       - do not make the first lib the main app and ask for consent on every lib -> negative UX
        #       - ignore tracking -> negative UX (for developers / maintainers)
        #       - inform the user -> we do this below for now
        # NOTE: For ALLOW/DENY and white-/blacklisted packages, the askForConsent method does not have to be executed,
        #       because they use the pre-defined consent setup to determine if usage statistics shall be send or not.
        if "PLAUSIPY_DEBUG" in os.environ and any(
            [not pp._consent_checked for pp in cls._pps]
        ):
            print(
                "Some packages have been checked for consent, but not all. Please check your code."
            )
            for pp in cls._pps:
                if not pp._consent_checked:
                    print(f"- {pp.name} ({pp.profile.name})")

        # check if any packages have not been checked but needed askForConsent
        # TODO: ALthough we cannot ask for content here, we have some alternative options to explore:
        #       - we can delay consent, store the data as file and process it as soon as consent is asked [fav]
        #       - we could run plausipy as a separate process in the background and hand over the job.
        if any(
            p.consent == Consent.ASK and not p._consent_checked for p in cls._pps
        ) or any(
            not p.consent.granted and p._require_consent and not p._consent_checked
            for p in cls._pps
        ):
            # find the packages that need whitelisting because they require tracking
            request_whitelist = [pp for pp in cls._pps if pp._require_consent]

            # display non-interactive promt
            show_setup_plausipy_box(request_whitelist)

        # terminate silently if no plausipy instances are running or all are disabled
        if not any([pp.allowed for pp in cls._pps]):
            logger.info("No plausipy instances to terminate")
            return

        # stop all plausipy instances that are not already stopped
        for pp in cls._pps:
            if pp._started_on and not pp._ended_on:
                pp.stop()

        # print data
        if "PLAUSIPY_DEBUG" in os.environ or cls._print_payload_before_terminate:
            print("\033[90m", end="")
            _print_box("Plausipy", json.dumps(cls.json(), indent=2))
            print("\033[0m", end="")

        # store data
        # NOTE: storing the data is not necessary and may even cause negative side effects
        #       as long as the id's are kept, a user can technically remove and request their tracked data.
        # cls.store()

        # send data
        cls.send()

    @classmethod
    def json(cls) -> dict:
        """
        Get the data in a json format
        """

        # apps
        apps = [pp for pp in cls._pps if pp.allowed]

        # gather general information
        granted_profile = max([pp._granted_profile for pp in apps])
        asked = any([pp.consent.hasBeenAsked for pp in apps])

        # experimentally we first downgraded all packages to their common minimal profile
        # Needs discussion: is this the right / best aproach?
        # If we take a request as one-request, using different profiles would diminish
        #  the idea of user-id separation in some profiles. However, the information of
        #  which packages are used together (independent of the user) might be of a higher
        #  relevance (and is also less sensitive).
        # Now, with the simplified profile system, all packages use the default profile unless specifically whitelisted.
        #  The rationale is, theat the initial experimental strategy would likely almost always downgrage all packages which
        #  is in conflict with the desire of all package maintainers to choose the lowest profile possible.
        # for pp in apps:
        #   pp.profile = granted_profile

        # return data
        return {
            "uuid": cls._id,
            "ppy": {
                "version": get_package_version("plausipy"),
            },
            "user": {
                "profile": granted_profile.name,
                "consented": True,  # we only filter apps with allowed == True
                "asked": asked,
                "location": Record.getUserLocation(),
                "system": Record.getUserSystem(),
                "python": Record.getUserPython(),
                "timestamp": datetime.now().isoformat(),
            },
            "app": [pp._app_json() for pp in apps],
        }

    @classmethod
    def store(cls):
        raise DeprecationWarning

        """
        Store the data in a file
        """

        # get data
        data = cls.json()

        # get directory
        file = DATA_DIR / f"{cls._id}.json"

        # ensure file exists
        file.parent.mkdir(parents=True, exist_ok=True)

        # write data
        with open(file, "w") as f:
            json.dump(data, f)

    @classmethod
    def send(cls):
        """
        Send the data to the server
        """

        # get data
        data = cls.json()

        # check if data is empty
        if not data["app"]:
            logger.info("No application data to send")
            return

        # make request
        logger.info("Sending data to server")
        logger.info(json.dumps(data, indent=2))

        # get key from main package
        main_package = cls.getMainPackage()
        key = (
            main_package._app_key
            if main_package
            else cls._pps[0]._app_key
            if cls._pps
            else None
        )

        if not key:
            logger.error("No key found")
            return

        # prepare header
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
            "User-Agent": "plausipy",
        }

        # send data
        response = requests.post(API_ENDPOINT, json=data, headers=headers, timeout=5)

        # check response
        if response.status_code == 200:
            logger.info("Data sent successfully")
        else:
            logger.error("Data could not be sent: %s", response.text)

    @classmethod
    def setMainPackage(cls, pp: "Plausipy"):
        """
        Set the main package
        """
        assert pp in cls._pps, "Package not found"
        assert cls.getMainPackage() is None, "Main package already set"
        pp._is_main = True

    @classmethod
    def getMainPackage(cls) -> "Plausipy | None":
        """
        Get the main package
        """
        assert sum([pp._is_main for pp in cls._pps]) <= 1, (
            "Multiple main packages found"
        )
        return next((pp for pp in cls._pps if pp._is_main), None)

    @classmethod
    def hasMainPackage(cls) -> bool:
        """
        Check if a main package has been set
        """
        return any([pp._is_main for pp in cls._pps])

    @classmethod
    def askForConsent(cls):
        """
        Ask for consent
        """

        # FIXME: we implemented a clie argument to disable plausipy, however, this conflicts with
        #        packages that require collection of usage statistics. There is reasonable interest on
        #        both sides. For now, we terminate with an error message and will revisit this later.
        if any([(pp.disabled and pp._require_consent) for pp in cls._pps]):
            print(
                "Plausipy is disabled, but some packages require consent. Please enable Plausipy."
            )
            exit(1)

        # get all non-disabled packages that have not been consented yet
        packages: list[Plausipy] = [pp for pp in cls._pps if not pp.disabled]

        # mark packages as chekced
        # NOTE: we will mark packages as checked that were registered when askForConsent was called
        #       the termination event will capture unchecked packages.
        for package in packages:
            package._consent_checked = True

        # find the main package by key
        main_package = cls.getMainPackage()

        # raise exception if no main package is found
        # NOTE: when used with the official api, there is always a main package
        if not main_package:
            logger.error("No main package found")
            raise PlausipyError("No main package found")

        # determine if we shall ask for consent
        # NOTE: Interrupting execution of the program is not pleasant and, in the interest of the user,
        #       must be limited to the required minimum.
        # NOTE: For allow and deny, the content manager is already used in PlausipyConsetn class.
        #       For ask, the contnet manager will be updated below and the user selection will
        #       be automatically reflected in PlausipyConsent.
        if any(p.consent == Consent.ASK for p in packages):
            logger.info(
                "User has set default consent to ASK, we will ask him for consent."
            )
            consent_response = show_tracking_info(main_package, packages)
            logger.info("User replied to consent dialogue with: %s.", consent_response)

            # flag packages as asked (this is temporary, kept in PlausipyConsent)
            for package in packages:
                package.consent.asked()

            # update user consent (this is permanent, saved by ContentManager)
            if consent_response == Consent.ALLOW:
                ConsentManager.get().consent = Consent.ALLOW

            if consent_response == Consent.DENY:
                ConsentManager.get().consent = Consent.DENY

        # check if any package has denied tracking where required
        if any([not p.allowed and p._require_consent for p in packages]):
            logger.error("Tracking denied where required")

            required_packages = [
                p for p in packages if not p.allowed and p._require_consent
            ]
            handling_response = show_tracking_required(required_packages)
            assert handling_response in ["a", "w", "x"], "Invalid response"

            # conditionally, give consent once for required packages
            if handling_response == "a":
                for package in required_packages:
                    package.consent.allowOnce()

            # conditionally, whitelist required packages
            if handling_response == "w":
                for package in required_packages:
                    ConsentManager.get().addPackageToWhitelist(
                        package.name, package.profile
                    )

            # exit application if tracking is required but not consented
            if any([not p.allowed and p._require_consent for p in packages]):
                exit(1)

    def __init__(
        self,
        app_name: str,
        app_key: str,
        profile: Profile = Profile.PACKAGE,
        require_consent: bool = False,
        start: bool = False,
        endpoint: str | None = None,
    ):
        # log
        logger.info("Initializing plausipy for %s", app_name)

        # ptree
        self._ptree = get_package_tree()
        logger.info("Package tree: %s", self._ptree)

        # api endpoint
        if endpoint:
            global API_ENDPOINT
            logger.info("Setting API endpoint to %s", endpoint)
            API_ENDPOINT = endpoint

        # register self and terminate event
        self._pps.append(self)
        self.registerTerminationEvent(app_key)

        # app info
        self._is_main = False
        self._id = str(uuid.uuid4())
        self._app_name = app_name
        self._app_key = app_key
        self._require_consent = require_consent

        # parameter
        self.disabled = False
        self._ppy_version = get_package_version("plausipy")
        self._version = get_package_version(self._app_name)

        # consent, profile and id
        self._consent_checked = (
            False  # check -> Plausipy.askForContent was run when package was registered
        )
        self._consent = PlausipyConsent(
            app_name
        )  # ask   -> user interaction initiated by Plausipy.askForContent
        self._granted_profile = ConsentManager.get().getPackageProfile(app_name)
        self._requested_profile = profile
        self._track_id = IDManager().get_id(self.profile, app_name)

        # ...
        self._returncode = None
        self._started_on = None
        self._ended_on = None
        self._initial_usage = None
        self._memory_delta = None
        self._data = {}

        # start collection
        if start:
            self.start()

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._app_name

    @property
    def consent(self) -> PlausipyConsent:
        return self._consent

    def start(self):
        """
        Indicate to plausipy that the trackable execution has started.
        This usually means that the program is started.
        """

        # start run
        self._started_on = datetime.now()

        # capture initial usage
        # NOTE: usage information is collected but won't be captured if tracking has not been consented
        self._initial_usage = get_usage_data()

    def stop(self):
        # stop
        self._ended_on = datetime.now()

        # update usage
        final_usage = get_usage_data()
        memory_delta = final_usage["memory"] - self._initial_usage["memory"]
        self._memory_delta = memory_delta

    @property
    def profile(self) -> Profile:
        """
        Get the profile of the current track-id
        """
        return min(self._requested_profile, self._granted_profile)

    @property
    def returncode(self) -> int | None:
        """
        Get the return code of the run
        """
        return self._returncode

    @returncode.setter
    def returncode(self, value: int):
        """
        Set the return code of the run
        """
        self._returncode = value

    @property
    def allowed(self) -> bool:
        return not self.disabled and self.consent.granted

    def setData(self, **kwargs):
        """
        Set data for the current run
        """
        self._data.update(kwargs)

    def _app_json(self) -> dict:
        parent_package = self._ptree[2] if len(self._ptree) > 2 else None
        parent_version = get_package_version(parent_package)
        runtime = (
            (self._ended_on - self._started_on).total_seconds() if self._ended_on else 0
        )
        cpu = self._initial_usage["cpu"] if self._initial_usage else None

        return {
            "uuid": self._id,
            "name": self._app_name,
            "key": self._app_key,
            "version": self._version,
            "granted_profile": self._granted_profile.name,
            "requested_profile": self._requested_profile.name,
            "applied_profile": self.profile.name,
            "profile": self.profile.name,  # NOTE: LEGACY
            "user": self._track_id.id,
            "parent": parent_package,
            "parent_version": parent_version,
            "returncode": self._returncode,
            "runtime": runtime,
            "cpu": cpu,
            "memory": self._memory_delta,
            "data": self._data,
        }

    def __eq__(self, value: "Plausipy | str"):
        if isinstance(value, Plausipy):
            return self._id == value._id
        elif isinstance(value, str):
            return self._app_name == value
        return NotImplemented
