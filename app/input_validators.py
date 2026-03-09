"""Input validation for calculator operands.

Converts raw input to Decimal values, enforces maximum value limits,
and normalizes scientific notation for display.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import logging
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


@dataclass
class InputValidator:
    """Validates and converts user input to Decimal values."""

    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """Validate and convert input to a Decimal, enforcing max value limits."""
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > config.max_input_value:
                logging.warning(f"Input value {value} exceeds maximum allowed: {config.max_input_value}")
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")  # pragma: no cover
            normalized = number.normalize()
            if normalized.as_tuple().exponent > 0:
                normalized = normalized.quantize(Decimal('1'))
            return normalized
        except InvalidOperation as e:
            logging.warning(f"Invalid number format: {value}")
            raise ValidationError(f"Invalid number format: {value}") from e  # pragma: no cover