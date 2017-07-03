import json
import logging
import zipfile
from service.document_downloader_zipper_service import DocumentDownloaderZipper
logger.setLevel(logging.INFO)

logger.info('Loading function')


def is_int(input_string):
    type_int = False
    try:
        int(input_string)
        type_int = True
    except Exception as e:
        pass
    return type_int


def lambda_handler(event, context):
    customer_ids = event.get('query', {}).get('customer_ids', '').split(',')
    customer_ids = [customer_id for customer_id in event.get('query', {}).get(
        'customer_ids', '').split(',') if is_int(customer_id)]
    zip_path = DocumentDownloaderZipper(customer_ids)
    return {
        'statusCode': '200',
        'body': zipfile.ZipFile(zip_path, 'r'),
        'headers': {
            'Content-Type': 'application/zip',
            'Content-Disposition': 'attachment; filename=%s' % zip_path.split('')[-1]
        },
    }
