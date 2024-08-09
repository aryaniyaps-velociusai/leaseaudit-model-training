import asyncio
import os
from pathlib import Path
from typing import Annotated

from langchain_core.language_models import BaseChatModel
from pdf2image import convert_from_path

from app.extraction_chain import run_extraction_chain
from app.ocr_client import get_ocr_client, perform_ocr_from_image
import typer
import sqlite3
from dotenv import load_dotenv

from app.chat_model import get_chat_model
from app.core.logger import configure_logging, logger


# Initialize the database connection and create the table
def init_db():
    logger.debug("Initializing SQLite3 database")
    db_path = "../output/extracted_lease_agreements.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extracted_text TEXT,
            extracted_fields TEXT
        )
        """
    )
    conn.commit()
    return conn


async def store_extracted_fields(
    extracted_text: str, chat_model: BaseChatModel, conn: sqlite3.Connection
) -> None:
    try:
        # Run the extraction chain
        extracted_fields = await run_extraction_chain(
            chat_model=chat_model, text=extracted_text
        )

        cursor = conn.cursor()

        # Insert the extracted text and fields into the table
        cursor.execute(
            """
            INSERT INTO extracted_data (extracted_text, extracted_fields)
            VALUES (?, ?)
        """,
            (extracted_text, str(extracted_fields)),
        )

        # Commit the transaction
        conn.commit()

        logger.debug("Data successfully stored in the SQLite3 database")

    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")


async def process_image(image, conn, image_index: int, num_images: int):
    logger.debug(f"Processing image {image_index + 1}/{num_images}")
    extracted_text = await perform_ocr_from_image(image=image, client=get_ocr_client())
    await store_extracted_fields(
        extracted_text=extracted_text,
        chat_model=get_chat_model(),
        conn=conn,
    )


async def process_lease_agreements(folder_path: Path, conn: sqlite3.Connection) -> None:
    for root, _, files in os.walk(folder_path):
        for file_index, file in enumerate(files):
            logger.debug(f"Processing file {file_index + 1}/{len(files)}: {file}")
            converted_images = convert_from_path(folder_path / file, last_page=10)
            tasks = [
                process_image(
                    image, conn, image_index=index, num_images=len(converted_images)
                )
                for index, image in enumerate(converted_images)
            ]
            await asyncio.gather(*tasks)
            await asyncio.sleep(2)


def main(
    folder_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    *,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            "-d",
            help="Enable debug mode",
        ),
    ] = False,
) -> None:
    load_dotenv()
    configure_logging(debug_mode=debug)
    conn = init_db()
    asyncio.run(process_lease_agreements(folder_path=folder_path, conn=conn))
    conn.close()


if __name__ == "__main__":
    typer.run(main)
