from _typeshed import Incomplete

class Config:
    """
    A singleton Config class that strictly ensures:
    - You call get(name, required=True/False, default=...)
    - The environment variable is read only once and stored.
    - Any subsequent calls to get(name, ...) return the same stored value.
    - No updates to the stored values are allowed.
    """
    def __new__(cls): ...
    def __init__(self) -> None: ...
    @classmethod
    def get_bool(cls, name: str, required: bool = True, default: Incomplete | None = None): ...
    @classmethod
    def get(cls, name: str, required: bool = True, default: Incomplete | None = None):
        """
        Retrieve the environment variable 'name' and store it if not already stored.
        - If 'required' is True and the env var is missing, raise an error (unless a default is given).
        - If 'required' is False, return the default (or None if no default).
        - Once stored, subsequent calls ignore environment changes or new defaults.
        """
    def __setattr__(self, name, value) -> None:
        """
        Prevent normal attribute setting on the class unless it's an internal attribute.
        This ensures we don't accidentally mutate config values by direct assignment.
        """
