import os
from mistralai import Mistral

class MistralOCR:
    def __init__(self, api_key):
        self.client = Mistral(api_key=api_key)

    def upload_pdf(self, file_path):
        with open(file_path, 'rb') as f:
            uploaded_pdf = self.client.files.upload(
                file={
                    'file_name': os.path.basename(file_path),
                    'content': f,
                },
                purpose='ocr'
            )
        return uploaded_pdf

    def get_signed_url(self, file_id):
        return self.client.files.get_signed_url(file_id=file_id)

    def process_ocr(self, document_url):
        return self.client.ocr.process(
            model='mistral-ocr-latest',
            document={
                'type': 'document_url',
                'document_url': document_url,
            }
        )
