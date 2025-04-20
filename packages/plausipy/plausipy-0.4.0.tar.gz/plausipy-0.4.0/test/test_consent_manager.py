import tempfile
from pathlib import Path

import pytest

from plausipy.user import Consent, ConsentManager, Profile


@pytest.fixture
def cm():
    with tempfile.NamedTemporaryFile() as temp_file:
        ConsentManager._consent_file = Path(temp_file.name)
        cm = ConsentManager()
        yield cm


def test_default_consent(cm):
    assert cm.consent == Consent.ASK


def test_add_package_to_whitelist(cm):
    package = "test_package"
    profile = Profile.USER
    cm.addPackageToWhitelist(package, profile)
    assert cm.isPackageWhitelisted(package)
    assert cm.getPackageWhitelistProfile(package) == profile


def test_add_package_to_blacklist(cm):
    package = "test_package"
    cm.addPackageToBlacklist(package)
    assert cm.isPackageBlacklisted(package)


def test_remove_from_blacklist_when_whitelisted(cm):
    package = "test_package"
    profile = Profile.USER
    cm.addPackageToBlacklist(package)
    cm.addPackageToWhitelist(package, profile)
    assert not cm.isPackageBlacklisted(package)
    assert cm.isPackageWhitelisted(package)


def test_remove_from_whitelist_when_blacklisted(cm):
    package = "test_package"
    profile = Profile.USER
    cm.addPackageToWhitelist(package, profile)
    cm.addPackageToBlacklist(package)
    assert not cm.isPackageWhitelisted(package)
    assert cm.isPackageBlacklisted(package)


# def test_check_consent_allow(cm):
#     cm.consent = Consent.ALLOW
#     assert cm.checkConsent("test_package", None, False)

# def test_check_consent_deny(cm):
#     cm.consent = Consent.DENY
#     assert not cm.checkConsent("test_package", None, False)

# def test_check_consent_ask(cm):
#     cm.consent = Consent.ASK
#     assert not cm.checkConsent("test_package", None, False)

# def test_check_consent_blacklisted(cm):
#     package = "test_package"
#     cm.addPackageToBlacklist(package)
#     assert not cm.checkConsent(package, None, False)

# def test_check_consent_whitelisted(cm):
#     package = "test_package"
#     profile = Profile.USER
#     cm.addPackageToWhitelist(package, profile)
#     assert cm.checkConsent(package, profile, False)


def test_reset_cm(cm):
    cm.addPackageToWhitelist("test_package_1", Profile.USER)
    cm.addPackageToBlacklist("test_package_2")
    cm.reset()
    assert len(cm.whitelist) == 0
    assert not cm.isPackageWhitelisted("test_package_1")
    assert len(cm.blacklist) == 0
    assert not cm.isPackageBlacklisted("test_package_2")
    assert cm.consent == Consent.ASK
    assert cm.profile == Profile.PACKAGE
