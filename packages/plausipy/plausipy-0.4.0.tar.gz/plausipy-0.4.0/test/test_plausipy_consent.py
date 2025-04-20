from unittest.mock import patch

from plausipy.plausipy import PlausipyConsent
from plausipy.user import Consent


def test_plausipy_consent_initial_state():
    for c in [Consent.ALLOW, Consent.DENY, Consent.ASK]:
        with patch("plausipy.user.ConsentManager.getPackageConsent", return_value=c):
            pc = PlausipyConsent("anyPackageName")
            assert pc.value == c
            assert pc.granted == (c == Consent.ALLOW)
            assert not pc.hasBeenAsked


def test_plausipy_consent_allow_once():
    for c in [Consent.ALLOW, Consent.DENY, Consent.ASK]:
        with patch("plausipy.user.ConsentManager.getPackageConsent", return_value=c):
            pc = PlausipyConsent("anyPackageName")
            pc.allowOnce()
            assert pc.granted


def test_plausipy_consent_deny_once():
    for c in [Consent.ALLOW, Consent.DENY, Consent.ASK]:
        with patch("plausipy.user.ConsentManager.getPackageConsent", return_value=c):
            pc = PlausipyConsent("anyPackageName")
            pc.denyOnce()
            assert not pc.granted


def test_plausipy_consent_asked():
    with patch(
        "plausipy.user.ConsentManager.getPackageConsent", return_value=Consent.ASK
    ):
        pc = PlausipyConsent("anyPackageName")
        assert not pc.hasBeenAsked
        assert not pc.granted
        pc.asked()
        assert pc.hasBeenAsked
        assert pc.granted


def test_plausipy_consent_not_asked():
    with patch(
        "plausipy.user.ConsentManager.getPackageConsent", return_value=Consent.ASK
    ):
        pc = PlausipyConsent("anyPackageName")
        assert not pc.hasBeenAsked
        assert not pc.granted


def test_plausipy_consent_comparison_with_consent_enum():
    with patch(
        "plausipy.user.ConsentManager.getPackageConsent", return_value=Consent.ALLOW
    ):
        pc = PlausipyConsent(Consent.ALLOW)
        assert pc == Consent.ALLOW
        assert pc != Consent.DENY


def test_plausipy_consent_comparison_with_string():
    with patch(
        "plausipy.user.ConsentManager.getPackageConsent", return_value=Consent.ALLOW
    ):
        pc = PlausipyConsent(Consent.ALLOW)
        assert pc == "y"
        assert pc != "d"


def test_plausipy_consent_comparison_with_other_instance():
    with patch(
        "plausipy.user.ConsentManager.getPackageConsent", return_value=Consent.ALLOW
    ):
        pc1 = PlausipyConsent("anyPackageName1")
        pc2 = PlausipyConsent("anyPackageName2")

        assert pc1 == pc2
