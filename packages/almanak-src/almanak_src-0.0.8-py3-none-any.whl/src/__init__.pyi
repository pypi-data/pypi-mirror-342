def patched_find_dotenv(filename: str = '.env', raise_error_if_not_found: bool = False, usecwd: bool = False):
    """
    A replacement for python-dotenv's find_dotenv that works with compiled
    .pyc files by using sys.argv[0] as a fallback.
    """
