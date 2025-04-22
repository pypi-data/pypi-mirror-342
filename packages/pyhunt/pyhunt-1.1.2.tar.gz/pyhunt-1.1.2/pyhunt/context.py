import contextvars
from typing import Optional

# Stores the name or identifier (string) of the function running in the current context.
current_function_context: contextvars.ContextVar[Optional[str]] = (
    contextvars.ContextVar(
        "current_function_context",
        default=None,
    )
)

# Tracks the depth of the call stack (an integer) within the current context.
call_depth: contextvars.ContextVar[int] = contextvars.ContextVar(
    "call_depth",
    default=0,
)
