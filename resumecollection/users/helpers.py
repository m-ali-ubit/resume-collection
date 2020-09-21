import logging
from datetime import datetime, timedelta
import jwt
from django.core.cache import cache


from config.settings import local as settings

logger = logging.getLogger(__name__)


class UpdatePasswordHelper:
    key_prefix = "UPDATE_PASSWORD"

    @classmethod
    def generate_update_password_url(cls, user):
        user_payload = {
            "sub": user.id,
            "exp": datetime.now() + timedelta(seconds=3600),
        }
        encoded_token = jwt.encode(user_payload, settings.JWT_SECRET_KEY)
        cache.set(
            cls.get_key_value_from_email(user.email), user_payload, 3600,
        )
        update_password_link = (
            f"{settings.BASE_URL}/resumecollection/account/new-password?"
            f"token={encoded_token.decode('utf-8')}&email={user.email}"
        )

        logger.info(
            f"Payload successfully saved for the update password token of {user.email}"
        )
        return update_password_link

    @classmethod
    def verify_update_password(cls, token: str, email: str) -> bool:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
            payload_data_cache = cache.get(cls.get_key_value_from_email(email))
            if payload == payload_data_cache:
                logger.info(f"Update password token verified for {email}")
                return True
            logger.info(f"Update password token is invalid for {email}")
            raise Exception("The token for the reset password is not valid.")
        except jwt.ExpiredSignatureError:
            logger.error("Token Signature has been expired.")
            return False

    @classmethod
    def get_key_value_from_email(cls, email: str) -> str:
        return f"{cls.key_prefix}:{email}"

    @classmethod
    def invalidate_update_password_token(cls, email: str) -> None:
        key = cls.get_key_value_from_email(email)
        cache.delete(key)
        logger.info(f"{key} key removed from the cache")
