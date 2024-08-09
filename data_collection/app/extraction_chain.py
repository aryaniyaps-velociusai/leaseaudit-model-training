from typing import Any

from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel

from app.core.output_parsers import get_json_schema_parser_instructions, parse_json
from app.output_models.extract_fields import ExtractFieldsResult


async def run_extraction_chain(chat_model: BaseChatModel, text: str) -> dict[str, Any]:
    messages = [
        (
            "system",
            """
                You are an intelligent analyst that can extract relevant values from a lease agreement.
                You will be given a block of text that has been extracted from a lease agreement using OCR.
                The OCR text may contain some obvious errors (see examples below). You should fix these errors and
                extract the following fields in the format given below:\n
                You should ONLY respond in the format as described below.\n
                ## RESPONSE FORMAT:\n
                {format_instructions}

                ## EXAMPLES OF ERRORS YOU MAY HAVE TO CORRECT\n\n
                '1' misread as '/', 'O' as '0', 'S' as '5', 'B' as '8', 'Z' as '2', 'G' as '6', 'I' as '1', 'A' as '4', 'l' as '1'\n

                ## OTHER NOTES\n\n
                1. The leases may not have an explicit lease end date but may have a period from one date to another date. In this case, lease end date is the another date.\n
                2. The leases may not have an explicit lease end date but may have a lease duration in months or years. In this case, you should calculate the end date by adding the lease duration.\n
                3. The leases may not have an explicit lease end but may be renew automatically for some years. In this case, you should calculate the lease end by adding automatic renew year to the lease start date.\n
                4. Please note that 'monthly rent', 'rent income', 'monthly base rent', and 'rent for each month' all refer to the charges that an employee/tenat will be charged for rental accommodations.\n
                5. Security deposit and Monthly Rent are different. Do not extract value of Security deposit as Monthly Rent.
                6. Prorated Rent and Monthly Rent are different. Do not extract value of Prorated Rent as Monthly Rent.
                7. If they do not mention the monthly rent, you should calculate the monthly rent by dividing the total rent by the lease term
                8. If they do not mention the lease rent, you should calculate the lease rent by multiplying the monthly rent with the lease term.
                9. if the value of any fields is not found, give the value as null for that field
                10. Unit Type is generally where the resident is going to stay. If not mentioned, skip
                11. 'Apartment Number', 'Apartment No', 'Apt No', 'Apt #', 'Unit #' and 'unit number' are same.
                12. make sure Monthly Payment Breakdown values should be extracted as they are present in the text without any manipulation.\n
                \t a. If the rent in Monthly Payment Breakdown does not take discounts into account, in the output also do the same.
                13. Do not apply any common practices while extracting the value of the fields.
                14. make sure Utility Charges values are extracted without any manipulation
                \t - look for charges like water charge, pest control, garage fee, pet fee
                \t - W, S, T stands for Water, Sewer, and Trash and they may be charged together\n
                15. If multiple tenant names are found in the OCR text, extract the first tenant name only.
                16. 'Resident name' and 'tenant name' all mean the same.
                17. If multiple lease rent values are found, select the one that matches the lease start and end date. Return only a single lease rent value, and not a dictionary of lease rent values.
                18. If multiple monthly rent values are found, select the one that matches the lease start and end date. Return only a single monthly rent value, and not a dictionary of monthly rent values.
                19. If multiple original rent values are found, select the one that matches the lease start and end date. Return only a single original rent value, and not a dictionary of original rent values.
        """,
        ),
        (
            "human",
            """
            ## OCR TEXT:\n\n
            ```
            {text}
            ```\n\n\n
            Extract the values from the above text, following previously given instructions.
            """,
        ),
    ]

    chain = ChatPromptTemplate.from_messages(messages) | chat_model | parse_json

    # Send the messages to the model and get the response
    return await chain.ainvoke(
        {
            "format_instructions": get_json_schema_parser_instructions(
                pydantic_model=ExtractFieldsResult
            ),
            "text": text,
        }
    )
