from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Self, TypeVar

from pydantic import StrictInt, field_validator, model_validator

from archipy.models.dtos.base_dtos import BaseDTO

# Generic types
T = TypeVar("T", bound=Enum)


class RangeDTO(BaseDTO):
    """Data Transfer Object for decimal range queries.

    This DTO encapsulates a range of decimal values with from_ and to fields.
    Provides validation to ensure range integrity.
    """

    from_: Decimal | None = None
    to: Decimal | None = None

    @field_validator("from_", "to", mode="before")
    def convert_to(cls, value: Decimal | str | None) -> Decimal | None:
        """Convert string values to Decimal type.

        Args:
            value: The value to convert, can be None, string or Decimal.

        Returns:
            The converted Decimal value or None.

        Raises:
            TypeError: If the value is not a string or Decimal.
        """
        if value is None:
            return None

        # Convert value to Decimal if it's valid
        try:
            return Decimal(value)
        except (TypeError, ValueError):
            error_message = "Decimal input should be str or decimal."
            raise TypeError(error_message) from None

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that from_ is less than to when both are provided.

        Returns:
            The validated model instance if valid.

        Raises:
            ValueError: If from_ is greater than or equal to to.
        """
        if self.from_ and self.to and self.from_ >= self.to:
            error_message = "from_ can`t be bigger than to"
            raise ValueError(error_message)
        return self


class IntegerRangeDTO(BaseDTO):
    """Data Transfer Object for integer range queries.

    This DTO encapsulates a range of integer values with from_ and to fields.
    Provides validation to ensure range integrity.
    """

    from_: StrictInt | None = None
    to: StrictInt | None = None

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that from_ is less than to when both are provided.

        Returns:
            The validated model instance if valid.

        Raises:
            ValueError: If from_ is greater than to.
        """
        if self.from_ and self.to and self.from_ > self.to:
            error_message = "from_ can`t be bigger than to"
            raise ValueError(error_message)
        return self


class DateRangeDTO(BaseDTO):
    """Data Transfer Object for date range queries.

    This DTO encapsulates a range of date values with from_ and to fields.
    Provides validation to ensure range integrity.
    """

    from_: date | None = None
    to: date | None = None

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that from_ is less than to when both are provided.

        Returns:
            The validated model instance if valid.

        Raises:
            ValueError: If from_ is greater than to.
        """
        if self.from_ and self.to and self.from_ > self.to:
            error_message = "from_ can`t be bigger than to"
            raise ValueError(error_message)
        return self


class DatetimeRangeDTO(BaseDTO):
    """Data Transfer Object for datetime range queries.

    This DTO encapsulates a range of datetime values with from_ and to fields.
    Provides validation to ensure range integrity.
    """

    from_: datetime | None = None
    to: datetime | None = None

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that from_ is less than to when both are provided.

        Returns:
            The validated model instance if valid.

        Raises:
            ValueError: If from_ is greater than to.
        """
        if self.from_ and self.to and self.from_ > self.to:
            error_message = "from_ can`t be bigger than to"
            raise ValueError(error_message)
        return self
