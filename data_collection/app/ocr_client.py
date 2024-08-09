from functools import lru_cache
from io import BytesIO

from PIL.Image import Image
from app.core.config import settings
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@lru_cache()
def get_ocr_client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(
        endpoint=settings.azure_document_intelligence_endpoint,
        credential=AzureKeyCredential(
            key=settings.azure_document_intelligence_key.get_secret_value()
        ),
    )


async def perform_ocr_from_image(
    image: Image, client: DocumentIntelligenceClient
) -> str:
    # Convert the PILImage to a byte stream
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)  # Reset the stream position to the beginning
    poller = await client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=image_bytes,
        content_type="application/octet-stream",
    )
    result = await poller.result()
    return result.content
