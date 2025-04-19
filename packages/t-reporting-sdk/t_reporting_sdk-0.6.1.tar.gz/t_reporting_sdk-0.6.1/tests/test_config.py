import os
import pytest

from t_reporting_sdk.config import ReportingSDKConfig


class TestReportingSDKConfig:
    def setup_class(self):
        os.environ["FABRIC_BASE_URL"] = "http://localhost:8000"
        os.environ["FABRIC_USER_EMAIL"] = "default@reporter.test"
        os.environ["FABRIC_USER_OTP_SECRET"] = "fake_secret"

    def teardown_class(self):
        del os.environ["FABRIC_BASE_URL"]
        del os.environ["FABRIC_USER_EMAIL"]
        del os.environ["FABRIC_USER_OTP_SECRET"]

    @pytest.mark.unit
    def test_singleton(self):
        config1 = ReportingSDKConfig()
        config2 = ReportingSDKConfig()
        config3 = ReportingSDKConfig.configure()

        assert config1 is config2
        assert config1 is config3

    @pytest.mark.unit
    def test_default_values(self):
        config = ReportingSDKConfig()

        assert config.fabric_client_config.base_url == "http://localhost:8000"
        assert config.fabric_client_config.user_email == "default@reporter.test"
        assert config.fabric_client_config.user_otp_secret == "fake_secret"

    @pytest.mark.unit
    def test_partial_configure(self):
        ReportingSDKConfig.configure(fabric_base_url="http://localhost:8001")

        config = ReportingSDKConfig()

        assert config.fabric_client_config.base_url == "http://localhost:8001"
        assert config.fabric_client_config.user_email == "default@reporter.test"
        assert config.fabric_client_config.user_otp_secret == "fake_secret"

    @pytest.mark.unit
    def test_configure(self):
        ReportingSDKConfig.configure(
            fabric_base_url="http://localhost:8001",
            fabric_user_email="non_default@reporter.test",
            fabric_user_secret="another_fake_secret",
        )

        config = ReportingSDKConfig()

        assert config.fabric_client_config.base_url == "http://localhost:8001"
        assert config.fabric_client_config.user_email == "non_default@reporter.test"
        assert config.fabric_client_config.user_otp_secret == "another_fake_secret"
