"""Custom exceptions for Aurora Quant platform."""

class AuroraQuantException(Exception):
    """Base exception for Aurora Quant."""
    pass


class InsufficientDataError(AuroraQuantException):
    """Raised when insufficient market data is available."""
    pass


class InsufficientCapitalError(AuroraQuantException):
    """Raised when insufficient capital for trade execution."""
    pass


class DataFetchError(AuroraQuantException):
    """Raised when market data fetch fails."""
    pass


class StrategyError(AuroraQuantException):
    """Raised when strategy execution fails."""
    pass


class ExecutionError(AuroraQuantException):
    """Raised when trade execution fails."""
    pass
