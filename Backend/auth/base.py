from abc import ABC, abstractmethod
from typing import Optional
from flask import Request

class AuthStrategy(ABC):
    @abstractmethod
    def protect_route(self, func):
        """Decorator to protect a route."""
        raise NotImplementedError

    @abstractmethod
    def get_current_user(self, request: Request) -> Optional[object]:
        """Return the current user or None."""
        raise NotImplementedError
