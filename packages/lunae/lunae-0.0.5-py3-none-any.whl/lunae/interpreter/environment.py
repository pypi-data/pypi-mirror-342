"""
This module defines the Environment class used for managing variable scopes and bindings.
"""

from typing import Any, Optional

from lunae.utils.errors import InterpreterError


class Environment:
    """
    Represents a variable environment for the interpreter.

    Attributes:
        vars (dict[str, Any]): A dictionary storing variable names and their values.
        parent (Optional[Environment]): The parent environment, if any.
    """

    def __init__(self, parent: "Optional[Environment]" = None):
        """
        Initializes a new Environment.

        Args:
            parent (Optional[Environment]): The parent environment, if any.
        """
        self.vars: dict[str, Any] = {}
        self.parent = parent

    def get(self, name):
        """
        Retrieves the value of a variable.

        Args:
            name (str): The name of the variable.

        Returns:
            Any: The value of the variable.

        Raises:
            InterpreterError: If the variable is not defined.
        """
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise InterpreterError(f"Undefined variable '{name}'", None)

    def set(self, name, value):
        """
        Updates or creates a variable in the current environment.

        Args:
            name (str): The name of the variable.
            value (Any): The value to assign to the variable.
        """
        self.vars[name] = value

    def define(self, name, value):
        """
        Defines a new variable in the current environment.

        Args:
            name (str): The name of the variable.
            value (Any): The value to assign to the variable.
        """
        self.vars[name] = value
