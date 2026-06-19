class UserNotFoundError(Exception):
    """Raised when a referenced user does not exist or has been soft-deleted."""


class InvalidGoogleTokenError(Exception):
    """Raised when a Google ID token fails server-side verification."""


class UnauthenticatedError(Exception):
    """Raised when a request requires authentication but no valid token is present."""


class InactiveUserError(Exception):
    """Raised when a matched user account is inactive or soft-deleted."""


class AuthorizationError(Exception):
    """Raised when an authenticated user lacks permission for the requested resource."""
