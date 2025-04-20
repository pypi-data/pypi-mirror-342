from io import BytesIO
from http import HTTPStatus

from .api.configuration import delete_configuration, get_configuration, list_configurations, save_configuration
from .api.document import process_document, upload_document, upload_files
from .api.job import result, status
from .api.template import delete_template, fill, list_templates, metadata
from .client import AuthenticatedClient
from .models import UploadCommand, UploadDocumentBody, OcrType, LlmType
from .models.template_fill_request import TemplateFillRequest

# New imports for concrete parameters:
from .models.upload_files_body import UploadFilesBody
from .types import File, Unset


class DocuDevsClient:
    def __init__(self, api_url: str = "https://api.docudevs.ai", token: str = None):
        # Create the openapi-python-client AuthenticatedClient
        self._client = AuthenticatedClient(base_url=api_url, token=token)

    async def list_configurations(self):
        """List all named configurations."""
        return await list_configurations.asyncio_detailed(client=self._client)

    async def get_configuration(self, name: str):
        """Get a named configuration."""
        return await get_configuration.asyncio_detailed(client=self._client, name=name)

    async def save_configuration(self, name: str, body: UploadCommand):
        """Save a named configuration."""
        return await save_configuration.asyncio_detailed(client=self._client, name=name, body=body)

    async def delete_configuration(self, name: str):
        """Delete a named configuration."""
        return await delete_configuration.asyncio_detailed(client=self._client, name=name)

    async def upload_files(self, body: UploadFilesBody):
        """Upload multiple files."""
        return await upload_files.asyncio_detailed(client=self._client, body=body)

    async def upload_document(self, body: UploadDocumentBody):
        """Upload a single document."""
        return await upload_document.asyncio_detailed(client=self._client, body=body)

    async def list_templates(self):
        """List document templates."""
        return await list_templates.asyncio_detailed(client=self._client)

    async def metadata(self, template_id: str):
        """Get metadata for a template."""
        return await metadata.asyncio_detailed(client=self._client, template_id=template_id)

    async def delete_template(self, template_id: str):
        """Delete template by ID."""
        return await delete_template.asyncio_detailed(client=self._client, template_id=template_id)

    async def process_document(self, guid: str, body: UploadCommand):
        """Process a document."""
        return await process_document.asyncio_detailed(client=self._client, guid=guid, body=body)

    async def result(self, uuid: str):
        """Get job result."""
        return await result.asyncio_detailed(client=self._client, uuid=uuid)

    async def status(self, guid: str):
        """Get job status."""
        return await status.asyncio_detailed(client=self._client, guid=guid)

    async def fill(self, name: str, body: TemplateFillRequest):
        """Fill a template."""
        return await fill.asyncio_detailed(client=self._client, name=name, body=body)

    async def submit_and_process_document(
        self,
        document: BytesIO,
        document_mime_type: str,
        prompt: str = "",
        schema: str = "",
        ocr: str = None,
        barcodes: bool = None,
        llm: str = None,
        extraction_mode=None,
    ) -> str:
        # Check mimetype
        if not document_mime_type:
            raise ValueError("document_mime_type is required")
        if not document:
            raise ValueError("document is required")

        document_file = File(payload=document, file_name="omitted", mime_type=document_mime_type)
        # Create the upload document body
        upload_body = UploadDocumentBody(document=document_file)

        # Upload the document
        upload_response = await self.upload_document(body=upload_body)
        if upload_response.status_code != HTTPStatus.OK:
            # Decode bytes to string to avoid escaped byte representation
            content_str = upload_response.content.decode('utf-8', errors='replace')
            raise Exception(f"Error uploading document: {content_str}")
        # Process the uploaded document
        guid = upload_response.parsed.guid


        process_body = UploadCommand(
            prompt=prompt,
            schema=schema,
            mime_type=document_mime_type,
            ocr=ocr,
            barcodes=barcodes,
            llm=llm,
            extraction_mode=extraction_mode,
        )
        process_resp = await self.process_document(guid=guid, body=process_body)
        if process_resp.status_code != HTTPStatus.OK:
            # Decode bytes and use process_resp for error content
            content_str = process_resp.content.decode('utf-8', errors='replace')
            raise Exception(f"Error processing document: {content_str}")
        return upload_response.parsed.guid

    async def wait_until_ready(self, guid: str):
        # Await the async result call and return parsed response
        response = await self.result(uuid=guid)
        if response.status_code != HTTPStatus.OK:
            content_str = response.content.decode('utf-8', errors='replace')
            raise Exception(f"Error getting result: {content_str} (status code: {response.status_code})")
        return response.parsed


# Convenience facade: synchronous client wrapping sync_detailed and blocking calls
class DocuDevsClientSync:
    def __init__(self, api_url: str = "https://api.docudevs.ai", token: str = None):
        self._client = AuthenticatedClient(base_url=api_url, token=token)

    def list_configurations(self):
        return list_configurations.sync_detailed(client=self._client)

    def get_configuration(self, name: str):
        return get_configuration.sync_detailed(client=self._client, name=name)

    def save_configuration(self, name: str, body: UploadCommand):
        return save_configuration.sync_detailed(client=self._client, name=name, body=body)

    def delete_configuration(self, name: str):
        return delete_configuration.sync_detailed(client=self._client, name=name)

    def upload_files(self, body: UploadFilesBody):
        return upload_files.sync_detailed(client=self._client, body=body)

    def upload_document(self, body: UploadDocumentBody):
        return upload_document.sync_detailed(client=self._client, body=body)

    def list_templates(self):
        return list_templates.sync_detailed(client=self._client)

    def metadata(self, template_id: str):
        return metadata.sync_detailed(client=self._client, template_id=template_id)

    def delete_template(self, template_id: str):
        return delete_template.sync_detailed(client=self._client, template_id=template_id)

    def process_document(self, guid: str, body: UploadCommand):
        return process_document.sync_detailed(client=self._client, guid=guid, body=body)

    def result(self, uuid: str):
        return result.sync_detailed(client=self._client, uuid=uuid)

    def status(self, guid: str):
        return status.sync_detailed(client=self._client, guid=guid)

    def fill(self, name: str, body: TemplateFillRequest):
        return fill.sync_detailed(client=self._client, name=name, body=body)

    def submit_and_process_document(
        self,
        document: BytesIO,
        document_mime_type: str,
        prompt: str = "",
        schema: str = "",
        ocr: str = None,
        barcodes: bool = None,
        llm: str = None,
        extraction_mode=None,
    ) -> str:
        if not document_mime_type:
            raise ValueError("document_mime_type is required")
        if not document:
            raise ValueError("document is required")
        document_file = File(payload=document, file_name="omitted", mime_type=document_mime_type)
        upload_body = UploadDocumentBody(document=document_file)
        upload_resp = self.upload_document(body=upload_body)
        if upload_resp.status_code != HTTPStatus.OK:
            content_str = upload_resp.content.decode('utf-8', errors='replace')
            raise Exception(f"Error uploading document: {content_str}")
        guid = upload_resp.parsed.guid
        process_body = UploadCommand(
            prompt=prompt,
            schema=schema,
            mime_type=document_mime_type,
            ocr=ocr,
            barcodes=barcodes,
            llm=llm,
            extraction_mode=extraction_mode,
        )
        process_resp = self.process_document(guid=guid, body=process_body)
        if process_resp.status_code != HTTPStatus.OK:
            content_str = process_resp.content.decode('utf-8', errors='replace')
            raise Exception(f"Error processing document: {content_str}")
        return guid

    def wait_until_ready(self, guid: str):
        # Note: This sync version will block until the result is ready.
        # A more robust implementation might involve polling with delays.
        response = self.result(uuid=guid)
        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Error getting result: {response.content} (status code: {response.status_code})")
        return response.parsed 


# Module-level re-export for sync client convenience
DocuDevsClientSync = DocuDevsClientSync

__all__ = [
    "DocuDevsClient",
    "UploadDocumentBody",
    "DocuDevsClientSync",
    "UploadCommand",
    "File",
    "UploadFilesBody",
    "TemplateFillRequest",
    # ... add other models if needed ...
]
