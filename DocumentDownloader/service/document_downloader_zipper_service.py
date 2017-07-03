#!/usr/bin/python

import os
import sys
import requests
from settings import IMAGE_BASE_URL
from database_service import Database
from folder_zip_service import ZipFolder


class CustomerDocumentDownloader(object):

    def __init__(self, customer_id, base_folder, db):
        self.customer_id = customer_id
        self.base_folder = base_folder
        self.folder_path = self.__create_folder()
        self.db = db
        self.documents_sql_query = self.__documents_sql_query()
        self.document_type_sql_query = self.__document_type_sql_query()
        self.document_type = self.__document_type()
        self.documents = self.__documents()

    def __create_folder(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
        folder_path = '{base_folder}/{customer_id}/'.format(
            base_folder=self.base_folder, customer_id=self.customer_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def __documents_sql_query(self):
        return """
                     SELECT  document_1, document_2, document_3, document_4, document_5, document_6, document_type_id
                     FROM customer_documents
                     WHERE customer_id={customer_id};
               """.format(customer_id=self.customer_id)

    def __document_type_sql_query(self):
        return """
                    SELECT id, name FROM customer_document_types;
               """

    def __document_type(self):
        rows = self.db.execute_query(self.document_type_sql_query)
        document_type = {}
        for row in rows:
            document_type[row['id']] = row['name']
        return document_type

    def __documents(self):
        rows = self.db.execute_query(self.documents_sql_query)
        documents = {}
        for row in rows:
            documents[self.document_type[row['document_type_id']]] = row
            documents[self.document_type[row['document_type_id']]].pop(
                'document_type_id')
        return documents

    def __file_downloader(self, url):
        file_name = self.folder_path + url.split('/')[-1]
        print "Downloading File: {file_name} from URL: {url}".format(file_name=file_name, url=url)
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)

    def download(self):
        for document_type, document_dict in self.documents.iteritems():
            for document_key, document_value in document_dict.iteritems():
                if document_value:
                    url = IMAGE_BASE_URL + document_value
                    self.__file_downloader(url)


class DocumentDownloaderZipper(object):

    def __init__(self, customer_ids):
        self.customer_ids = customer_ids
        self.base_folder = '/Users/nimesh/workspace/AWS-APIGateway-Lambda-S3-Downloader/DocumentDownloader/service/tmp/'
        self.to_be_zip_folder = self.base_folder + 'documents/'
        self.db = Database()
        self.__download_customer_documents()
        self.zip_path = self.__zip_documents()

    def __download_customer_documents(self):
        for customer_id in self.customer_ids:
            CustomerDocumentDownloader(
                customer_id, self.to_be_zip_folder, self.db).download()

    def __zip_documents(self):
        zip_path = self.base_folder + \
            'documents_for{customer_ids}.zip'.format(
                customer_ids=','.join(self.customer_ids))
        ZipFolder(self.to_be_zip_folder, zip_path)
        return zip_path
