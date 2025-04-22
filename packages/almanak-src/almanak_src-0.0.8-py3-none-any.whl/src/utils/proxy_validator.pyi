from _typeshed import Incomplete
from fastapi.security import HTTPAuthorizationCredentials as HTTPAuthorizationCredentials
from src.utils.config import Config as Config

IS_AGENT_DEPLOYMENT: Incomplete
USE_GCS_PROXY: Incomplete
IS_GCS_PROXY: Incomplete
USE_SQL_PROXY: Incomplete
IS_SQL_PROXY: Incomplete
STAGING_PLATFORM_JWT_PUBLIC_KEY: str
PRODUCTION_PLATFORM_JWT_PUBLIC_KEY: str
DEPLOYMENT_ENVIRONMENT: Incomplete
PLATFORM_JWT_PUBLIC_KEY = STAGING_PLATFORM_JWT_PUBLIC_KEY
PLATFORM_JWT_PUBLIC_KEY = PRODUCTION_PLATFORM_JWT_PUBLIC_KEY
platform_jwt_token_auth_scheme: Incomplete
platform_static_token_auth_scheme: Incomplete
PLATFORM_GENERAL_BEARER_TOKEN: Incomplete

def validate_jwt(credentials: HTTPAuthorizationCredentials = ...): ...
def validate_platform_static_token(credentials: HTTPAuthorizationCredentials = ...): ...
def validate_user_has_access(decoded_token: dict, user_id: str): ...
def validate_wallet_has_access(decoded_token: dict, wallet_address: str): ...
