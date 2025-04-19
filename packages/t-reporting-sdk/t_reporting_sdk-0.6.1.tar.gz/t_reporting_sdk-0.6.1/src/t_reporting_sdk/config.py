import os
from typing import Optional

from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClientConfig


class ReportingSDKConfig:
    """Singleton configuration class for the SDK."""
    _instance: Optional["ReportingSDKConfig"] = None

    fabric_client_config: FabricClientConfig

    def __new__(cls) -> "ReportingSDKConfig":
        """Singleton instance creation."""
        if cls._instance is None:
            # The super() function here refers to the base (object) class, which is the default parent of all Python classes. 
            # Calling super().__new__(cls) invokes the object class's __new__ method to allocate memory for a new instance. 
            # This is crucial for the singleton pattern, as it ensures proper instance creation and allows us to enforce 
            # that only one instance of the class is ever created. The intent of this code is to control object creation 
            # and reuse a single shared instance across the application.
            cls._instance = super().__new__(cls)
            # This ensures that the config is always initialized with values
            cls._instance.configure()
        return cls._instance

    @classmethod
    def configure(
        cls,
        *,
        fabric_base_url: Optional[str] = None,
        fabric_user_email: Optional[str] = None,
        fabric_user_secret: Optional[str] = None,
    ) -> "ReportingSDKConfig":
        """Set the configuration for the SDK."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        cls._instance.fabric_client_config = FabricClientConfig(
            base_url=fabric_base_url or os.getenv("FABRIC_BASE_URL"),
            user_email=fabric_user_email or os.getenv("FABRIC_USER_EMAIL"),
            user_otp_secret=fabric_user_secret or os.getenv("FABRIC_USER_OTP_SECRET"),
        )

        return cls._instance
