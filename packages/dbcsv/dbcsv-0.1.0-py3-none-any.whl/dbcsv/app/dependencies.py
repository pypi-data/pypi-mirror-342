# Create instance

from fastapi import Depends

from .core.config import settings
from .security.auth import AuthManager

auth = AuthManager(
    settings.SECRET_KEY, settings.ALGORITHM, settings.ACCESS_TOKEN_EXPIRE_MINUTES
)


current_user_dependency = Depends(auth.get_current_user)
