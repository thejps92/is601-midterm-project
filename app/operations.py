"""Arithmetic operations module using the Strategy pattern.

Defines an abstract Operation base class and concrete implementations for
each supported arithmetic operation. An OperationFactory provides dynamic
creation of operation instances by name.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List, Tuple
from app.exceptions import ValidationError


class Operation(ABC):
    """Abstract base class for all arithmetic operations (Strategy pattern)."""

    description: str = "Perform operation"

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Validate operands before execution. Override in subclasses for specific checks."""
        pass

    def __str__(self) -> str:
        return self.__class__.__name__


class Addition(Operation):
    description = "Addition (a + b)"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    description = "Subtraction (a - b)"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    description = "Multiplication (a * b)"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    description = "Division (a / b)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    description = "Exponentiation (a ^ b)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    description = "Nth root (b-th root of a)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


class Modulus(Operation):
    description = "Modulus (a mod b)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a % b


class IntegerDivision(Operation):
    description = "Integer division (a / b, truncated)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(int(a / b))


class Percentage(Operation):
    description = "Percentage (a / b * 100)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return (a / b) * Decimal('100')


class AbsoluteDifference(Operation):
    description = "Absolute difference (|a - b|)"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return abs(a - b)


class OperationFactory:
    """Factory for creating Operation instances by name (Factory pattern)."""

    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntegerDivision,
        'percent': Percentage,
        'abs_diff': AbsoluteDifference
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """Register a new operation class under the given name."""
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """Create and return an Operation instance for the given type name."""
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()

    @classmethod
    def is_valid_operation(cls, name: str) -> bool:
        """Check if an operation name is registered."""
        return name.lower() in cls._operations

    @classmethod
    def get_operations_help(cls) -> List[Tuple[str, str]]:
        """Return a list of (name, description) for all registered operations."""
        return [
            (name, op_class.description)
            for name, op_class in cls._operations.items()
        ]