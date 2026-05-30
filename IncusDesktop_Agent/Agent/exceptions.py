"""Agent-wide exception hierarchy.

All exceptions raised by controllers, middleware, utilities, and rawCommands
should derive from AgentError. A single Flask error handler (registered in
app.py) converts any AgentError into a structured JSON envelope that the GUI
deserializes and acts on.

Envelope shape (mirrored on the GUI side):

    {
        "code":        "INCUS_UNAVAILABLE",    # machine-readable, GUI dispatches on this
        "message":     "Incus daemon ...",     # default toast text
        "details":     {"socket": "..."},      # optional, context-specific
        "retriable":   true,                   # whether GUI should offer a Retry button
        "user_action": "Check the ..."         # optional hint shown to the user
    }

Adding a new error type: subclass AgentError (or one of its children), set
`code`, `status`, and optionally `retriable` / `user_action` defaults. Do not
raise bare Exception in the request path — wrap in AgentError so the GUI gets
a structured response instead of an opaque 500.
"""


class AgentError(Exception):
    """Base class for every exception the agent intentionally raises.

    Subclasses override `code`, `status`, `retriable`, `user_action`.
    """

    code: str = "AGENT_ERROR"
    status: int = 500
    retriable: bool = False
    user_action: str | None = None

    def __init__(
        self,
        message: str,
        *,
        details: dict | None = None,
        user_action: str | None = None,
        retriable: bool | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        if user_action is not None:
            self.user_action = user_action
        if retriable is not None:
            self.retriable = retriable

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "retriable": self.retriable,
            "user_action": self.user_action,
        }


# ─── Request-level errors ─────────────────────────────────────────────────

class ValidationError(AgentError):
    """Request body or query parameters failed validation."""
    code = "VALIDATION_FAILED"
    status = 400


class AuthError(AgentError):
    """Missing, malformed, or rejected agent key."""
    code = "AUTH_FAILED"
    status = 401
    user_action = "Re-enroll the agent key in the GUI."


class NotFoundError(AgentError):
    """Requested resource does not exist on this agent."""
    code = "NOT_FOUND"
    status = 404


# ─── Incus-related errors ─────────────────────────────────────────────────

class IncusError(AgentError):
    """Common base for any Incus-related failure.

    Kept as an intermediate class so existing `except IncusError` blocks in
    scenarios catch both transport (IncusUnavailableError) and API
    (IncusApiError) failures without changes.
    """
    code = "INCUS_ERROR"
    status = 502


class IncusUnavailableError(IncusError):
    """Incus daemon is not reachable: socket missing, connection refused,
    transport timeout."""
    code = "INCUS_UNAVAILABLE"
    status = 503
    retriable = True
    user_action = "Check the incus service on the host: systemctl status incus."


class IncusApiError(IncusError):
    """Incus REST API returned an error envelope, an unexpected payload,
    or a non-success status code."""
    code = "INCUS_API_ERROR"
    status = 502


# ─── RawCommand errors ────────────────────────────────────────────────────

class CommandFailedError(AgentError):
    """A rawCommand process exited with a non-zero return code."""
    code = "COMMAND_FAILED"
    status = 500


class CommandTimeoutError(AgentError):
    """A rawCommand exceeded its timeout and was killed."""
    code = "COMMAND_TIMEOUT"
    status = 504
    retriable = True
