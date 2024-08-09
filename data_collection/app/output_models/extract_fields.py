from datetime import date
from typing import Annotated, Any

from pydantic import BaseModel, Field


class ExtractFieldsResult(BaseModel):
    tenant_name: Annotated[
        str | None, Field(description="The name of the tenant, found in the OCR text.")
    ]

    unit_address: Annotated[
        str | None, Field(description="The unit address found in the OCR text.")
    ]

    unit_number: Annotated[
        str | None, Field(description="The unit number found in the OCR text.")
    ]

    unit_type: Annotated[
        str | None, Field(description="The unit type found in the OCR text.")
    ]

    agreement_date: date | None

    lease_start: Annotated[
        date | None,
        Field(description="The date when the lease starts, found in the OCR text."),
    ]

    lease_end: Annotated[
        date | None,
        Field(description="The date when the lease ends, found in the OCR text."),
    ]

    lease_auto_renew: Annotated[
        str | None,
        Field(description="The type of lease auto renewal, found in the OCR text."),
    ]

    hourly_rate: Annotated[
        float | None, Field(description="The hourly rate found in the OCR text.")
    ]

    monthly_rent: Annotated[
        float | None, Field(description="The monthly rent found in the OCR text.")
    ]

    prorated_rent: Annotated[
        float | None, Field(description="The prorated rent found in the OCR text.")
    ]

    security_deposit: Annotated[
        float | None, Field(description="The security deposit found in the OCR text.")
    ]

    lease_rent: Annotated[
        float | None, Field(description="The security deposit found in the OCR text.")
    ]

    monthly_payment_breakdown: Annotated[
        dict[str, Any] | None,
        Field(description="The monthly payment breakdown data found in the OCR text."),
    ]

    utility_charges: Annotated[
        dict[str, float | None] | None,
        Field(
            description="The utility charges found in the OCR text. This is a dictionary with utility charges as the key, and their price as the value."
        ),
    ]
