import zipfile
import sys
import os


class ZipFolder(object):

    def __init__(self, folder_path, output_path):
        self.folder_path = folder_path
        self.output_path = output_path
        self.parent_folder = os.path.dirname(self.folder_path)
        self.__zip_folder()

    def __zip_folder(self):
        contents = os.walk(self.folder_path)
        zip_file = zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED)
        try:
            for root, folders, files in contents:
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(
                        self.parent_folder + '/', '')
                    zip_file.write(absolute_path, relative_path)
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(
                        self.parent_folder + '/', '')
                    zip_file.write(absolute_path, relative_path)
        except IOError, message:
            print message
            sys.exit(1)
        except OSError, message:
            print message
            sys.exit(1)
        except zipfile.BadZipfile, message:
            print message
            sys.exit(1)
        finally:
            zip_file.close()
