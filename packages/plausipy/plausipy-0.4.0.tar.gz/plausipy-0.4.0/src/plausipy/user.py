import json
import logging
import uuid
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path

from .paths import CONSENT_FILE, IDS_FILE

# logger
logger = logging.getLogger(__name__)


class Profile(Enum):
    USER = "u"
    PACKAGE = "p"
    ANONYMOUS = "a"

    @property
    def score(self) -> int:
        return {
            Profile.USER: 100,
            Profile.PACKAGE: 10,
            Profile.ANONYMOUS: 1,
        }[self]

    # make profile comparable
    def __lt__(self, other: "Profile") -> bool:
        return self.score < other.score

    def __le__(self, other: "Profile") -> bool:
        return self.score <= other.score

    def __gt__(self, other: "Profile") -> bool:
        return self.score > other.score

    def __ge__(self, other: "Profile") -> bool:
        return self.score >= other.score


class Consent(Enum):
    ALLOW = "y"
    DENY = "n"
    ASK = "a"


class Scope:
    def __init__(self, location: bool, usage: bool, system: bool, python: bool):
        self.location = location
        self.usage = usage
        self.system = system
        self.python = python


class TrackID:
    def __init__(self, profile: Profile, id: str):
        self.profile = profile
        self.id = id


class IDManager:
    def __init__(self):
        self._data = {}
        self._clean = True
        self.load()

    def _get_default_data(self) -> dict:
        return {
            "user": None,
            "packages": {},
            "anonymous": [],
        }

    def _load_data(self) -> tuple[dict, bool]:
        try:
            with open(IDS_FILE, "r") as f:
                return json.load(f), True
        except Exception:
            return self._get_default_data(), False

    def load(self) -> None:
        self._data, self._clean = self._load_data()

    def store(self) -> None:
        if not self._clean:
            self._clean = True

            # Ensure directory exists
            IDS_FILE.parent.mkdir(parents=True, exist_ok=True)

            # Write data
            with open(IDS_FILE, "w") as f:
                json.dump(self._data, f)

    def _request_id(self) -> str:
        return str(uuid.uuid4())

    def get_id(self, profile: Profile, package: str | None) -> TrackID:
        # get id based on profile
        if profile == Profile.USER:
            if self._data["user"] is None:
                self._data["user"] = self._request_id()
                self._clean = False

            id = self._data["user"]

        elif profile == Profile.PACKAGE:
            if package not in self._data["packages"]:
                self._data["packages"][package] = self._request_id()
                self._clean = False

            id = self._data["packages"][package]

        elif profile == Profile.ANONYMOUS:
            id = self._request_id()
            self._data["anonymous"].append(id)
            self._clean = False

        # check
        assert id is not None, "ID not generated"

        # store
        self.store()

        # return
        return TrackID(profile, id)


class ConsentManager:
    _consent_file: Path = CONSENT_FILE

    @classmethod
    def get(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    @classmethod
    def _get_default_data(cls) -> dict:
        return {
            "created_on": date.today().isoformat(),
            "general": {
                "consent": Consent.ASK.name,
                "profile": Profile.PACKAGE.name,
            },
            "blacklist": [],
            "whitelist": [],
        }

    @classmethod
    def _get_package_whitelist_entry(cls, package: str, profile: Profile) -> dict:
        return {
            "package": package,
            "profile": profile.name,
            "updated_on": datetime.now().isoformat(),
        }

    @classmethod
    def _get_package_blacklist_entry(cls, package: str) -> dict:
        return {
            "package": package,
            "updated_on": datetime.now().isoformat(),
            "deny_until": None,
        }

    def __init__(self):
        if hasattr(self.__class__, "_instance"):
            raise RuntimeError(
                "ConsentManager singleton is already initialized. Use ConsentManager.get() to get the instance."
            )

        self._data = {}
        self.load()

    def load(self) -> None:
        try:
            with open(self._consent_file, "r") as f:
                self._data = json.load(f)
        except Exception:
            self._data = self._get_default_data()

    def store(self) -> None:
        # Ensure directory exists
        self._consent_file.parent.mkdir(parents=True, exist_ok=True)

        # Write data
        with open(self._consent_file, "w") as f:
            json.dump(self._data, f)

        # log
        logger.info(f"Consent data stored to {self._consent_file}.")

    def reset(self):
        if self._consent_file.exists():
            self._consent_file.unlink()
        self.load()

    @property
    def whitelist(self) -> dict[str, Profile]:
        return {e["package"]: Profile[e["profile"]] for e in self._data["whitelist"]}

    @property
    def blacklist(self) -> list:
        return [e["package"] for e in self._data["blacklist"]]

    @property
    def consent(self) -> Consent:
        # load stored default consent
        consent = Consent[self._data["general"]["consent"]]

        # updae deny -> ask conditionally
        # NOTE: to minimize the impact on the user, we will deny tracking for ALL not whitelisted package
        #       when the user denies tracking for ANY package. However, we will ask again after 2 weeks.
        if consent == Consent.DENY:
            if self._data["general"]["deny_until"] is None:
                self._data["general"]["deny_until"] = (
                    datetime.now() + timedelta(weeks=2)
                ).isoformat()
            else:
                deny_until = datetime.fromisoformat(self._data["general"]["deny_until"])
                if deny_until < datetime.now():
                    self.consent = Consent.ASK
                    consent = Consent.ASK
            self.store()

        # return consent
        return consent

    @consent.setter
    def consent(self, value: Consent):
        self._data["general"]["consent"] = value.name
        self._data["general"]["updated_on"] = datetime.now().isoformat()

        if value == Consent.DENY:
            self._data["general"]["deny_until"] = (
                datetime.now() + timedelta(weeks=2)
            ).isoformat()

        self.store()

    @property
    def profile(self) -> Profile:
        return Profile[self._data["general"]["profile"]]

    @profile.setter
    def profile(self, value: Profile):
        self._data["general"]["profile"] = value.name
        self._data["general"]["updated_on"] = datetime.now().isoformat()
        self.store()

    def isPackageWhitelisted(self, package: str) -> bool:
        return any(entry["package"] == package for entry in self._data["whitelist"])

    def getPackageWhitelistProfile(self, package: str) -> Profile:
        for entry in self._data["whitelist"]:
            if entry["package"] == package:
                return Profile[entry["profile"]]
        raise ValueError(f"Package {package} not whitelisted")

    def isPackageBlacklisted(self, package: str) -> bool:
        return any(entry["package"] == package for entry in self._data["blacklist"])

    def addPackageToWhitelist(self, package: str, profile: Profile):
        if self.isPackageWhitelisted(package) and self.whitelist[package] == profile:
            logger.info(
                f"Package {package} is already whitelisted with profile {profile.name}"
            )
            return

        # remove from blacklist
        if self.isPackageBlacklisted(package):
            logger.info(
                f"Package {package} is currently blacklisted, removing it from blacklist."
            )
            self.removePackageFromBlacklist(package, store=False)

        # log
        logger.info(
            f"Package {package} is being whitelisted with profile {profile.name}"
        )

        # add to whitelist & save
        self._data["whitelist"].append(
            self._get_package_whitelist_entry(package, profile)
        )
        self.store()

    def removePackageFromWhitelist(self, package: str, store: bool = True):
        self._data["whitelist"] = list(
            filter(lambda x: x["package"] != package, self._data["whitelist"])
        )
        if store:
            self.store()

    def addPackageToBlacklist(self, package: str):
        if self.isPackageBlacklisted(package):
            logger.info(f"Package {package} is already blacklisted.")
            return

        # remove from whitelist
        if self.isPackageWhitelisted(package):
            logger.info(f"Package {package} is in whitelist, removing it")
            self.removePackageFromWhitelist(package, store=False)

        # log
        logger.info(f"Package {package} is being blacklisted.")

        # add to blacklist & save
        self._data["blacklist"].append(self._get_package_blacklist_entry(package))
        self.store()

    def removePackageFromBlacklist(self, package: str, store: bool = True):
        self._data["blacklist"] = list(
            filter(lambda x: x["package"] != package, self._data["blacklist"])
        )
        if store:
            self.store()

    def checkPackageConsent(
        self, package: str, required_profile: Profile | None, asked: False
    ) -> bool:
        raise DeprecationWarning

        if self.isPackageBlacklisted(package):
            return False

        if self.isPackageWhitelisted(package):
            if required_profile is None:
                return True
            return self.getPackageWhitelistProfile(package) >= required_profile

        if self.consent == Consent.DENY:
            return False

        if self.consent == Consent.ALLOW:
            return True

        if self.consent == Consent.ASK:
            return asked

        return False

    def getPackageProfile(self, package: str) -> Profile:
        """Return the minimal profile allowed for the package.
           This method does NOT check if tracking is allowed for the package.
           Use getConsent() or checkConsent() for that.

        Args:
            package (str): name of the package

        Returns:
            Profile: profile granted to the package
        """

        try:
            granted_profile = self.getPackageWhitelistProfile(package)
        except ValueError:
            granted_profile = self.profile

        return granted_profile

    def getPackageConsent(self, package: str) -> Consent:
        """Return the consent for the package.
           This method checks if the package is blacklisted or whitelisted.
           If the package is not in either list, it returns the global consent.

        Args:
            package (str): name of the package

        Returns:
            Consent: consent for the package
        """

        if self.isPackageBlacklisted(package):
            return Consent.DENY

        if self.isPackageWhitelisted(package):
            return Consent.ALLOW

        return self.consent
