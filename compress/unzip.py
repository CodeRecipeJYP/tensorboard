import zipfile
path_to_zip_file = "dozip.zip"
directory_to_extract_to = "dozip"
zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
zip_ref.extractall(directory_to_extract_to)
zip_ref.close()

