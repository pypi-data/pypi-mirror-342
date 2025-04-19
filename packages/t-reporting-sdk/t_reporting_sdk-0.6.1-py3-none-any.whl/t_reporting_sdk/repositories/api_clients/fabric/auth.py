from __future__ import annotations

import datetime

import jwt

import logging

import pyotp
import requests
from requests.auth import AuthBase


POST_TIMEOUT_SECONDS = 10


class JWTToken:
    """A JWT token."""

    def __init__(self, encoded_value: str, algorithm="HS256"):
        self.encoded_value = encoded_value

        decoded_values = jwt.decode(
            jwt=self.encoded_value,
            algorithms=[algorithm],
            options={"verify_signature": False},
        )
        self.expires_at = datetime.datetime.fromtimestamp(
            decoded_values["exp"], tz=datetime.timezone.utc
        )
        self.issued_at = datetime.datetime.fromtimestamp(
            decoded_values["iat"], tz=datetime.timezone.utc
        )

    def __str__(self):
        return self.encoded_value

    def is_expired(self, expiry_margin: float = 0.1) -> bool:
        """
        Check if the token is expired or will expire soon.

        expiry_margin: A float between 0 and 1 representing the fraction of the
            token's total lifetime. For example, 0.1 means the token is considered
            expired if it will expire within 10% of its total lifetime.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        if now >= self.expires_at:
            return True

        lifetime_seconds = (self.expires_at - self.issued_at).total_seconds()
        expiry_margin_seconds = lifetime_seconds * expiry_margin
        is_within_expiry_margin = now + datetime.timedelta(seconds=expiry_margin_seconds) >= self.expires_at
        if is_within_expiry_margin:
            return True

        return False


class JWTAuth(AuthBase):
    access_token: JWTToken
    refresh_token: JWTToken
    refresh_url: str

    def __init__(self, email: str, otp_secret: str, auth_url: str, refresh_url: str):
        self.user_email = email
        self.user_otp_secret = otp_secret
        self.auth_url = auth_url
        self.refresh_url = refresh_url

        self.access_token = None
        self.refresh_token = None

    def __call__(self, r: requests.Request) -> requests.Request:
        if self.access_token is None:
            self.auth()

        if self.access_token.is_expired():
            self.refresh()
        
        r.headers["Authorization"] = f"Bearer {str(self.access_token)}"
        logging.debug(
            f"JWT auth called with token {self.access_token} and headers: {r.headers}"
        )

        return r
    
    def auth(self) -> None:
        # The configuration must match the one used in Fabric; otherwise, the request will fail.
        otp = pyotp.TOTP(self.user_otp_secret, interval=300).now()

        response = requests.post(
            self.auth_url,
            json={
                "email": self.user_email,
                "otp": otp,
            },
            timeout=POST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        new_values = response.json()
        self.access_token = JWTToken(new_values["accessToken"])
        self.refresh_token = JWTToken(new_values["refreshToken"])

    def refresh(self) -> None:
        if not self.access_token.is_expired():
            return None

        logging.info("Access token expired, refreshing")
        response = requests.post(
            self.refresh_url,
            json={
                "refreshToken": str(self.refresh_token),
            },
            timeout=POST_TIMEOUT_SECONDS,
        )

        if not response.ok:
            logging.warning("Could not refresh JWT token!")
            logging.warning(
                f"Received response {response.status_code}: {response.text}"
            )
            return None

        logging.info("Successfully refreshed JWT token")
        new_values = response.json()
        self.access_token = JWTToken(new_values["accessToken"])
        self.refresh_token = JWTToken(new_values["refreshToken"])
