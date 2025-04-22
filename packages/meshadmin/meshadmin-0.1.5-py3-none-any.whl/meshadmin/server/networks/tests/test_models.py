from datetime import timedelta

from django.utils import timezone

from meshadmin.server.networks.models import CA


class TestCAModel:
    def test_days_until_expiry(self, test_network):
        test_net = test_network(name="testnet", cidr="100.100.64.0/24")
        expired_ca = CA.objects.create(
            network=test_net,
            name="expired_ca",
            cert="test_cert",
            key="test_key",
            cert_print={
                "details": {
                    "notAfter": (timezone.now() - timedelta(days=1)).isoformat()
                }
            },
        )
        assert expired_ca.days_until_expiry == 0
        warning_ca = CA.objects.create(
            network=test_net,
            name="warning_ca",
            cert="test_cert",
            key="test_key",
            cert_print={
                "details": {
                    "notAfter": (timezone.now() + timedelta(days=15)).isoformat()
                }
            },
        )
        assert warning_ca.days_until_expiry == 14
        no_expiry_ca = CA.objects.create(
            network=test_net,
            name="no_expiry_ca",
            cert="test_cert",
            key="test_key",
            cert_print={"details": {}},
        )
        assert no_expiry_ca.days_until_expiry is None
        invalid_date_ca = CA.objects.create(
            network=test_net,
            name="invalid_date_ca",
            cert="test_cert",
            key="test_key",
            cert_print={"details": {"notAfter": "invalid-date"}},
        )
        assert invalid_date_ca.days_until_expiry is None
