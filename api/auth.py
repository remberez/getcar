from typing import Optional

from fastapi_users import BaseUserManager, models, IntegerIDMixin
from starlette.requests import Request

from models import UserModel

import logging

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = "903242390hf0sefh0sefobuaiad34"
    verification_token_secret = "403mai4nd90hf0mdai0sfobuaia334"

    async def on_after_forgot_password(
        self, user: models.UP, token: str, request: Optional[Request] = None
    ) -> None:
        log.warning("User %r has forgot password. Reset token: %r", user.id, token)

    async def on_after_register(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        log.warning("User %r has registered.", user.id)

    async def on_after_request_verify(
        self, user: models.UP, token: str, request: Optional[Request] = None
    ) -> None:
        log.warning(
            "Verification requested for user %r. Verification token: %r", user.id, token
        )
