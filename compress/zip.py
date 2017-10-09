import zipfile


jungle_zip = zipfile.ZipFile("dozip.zip", 'w')

jungle_zip.write('zip.py', compress_type=zipfile.ZIP_DEFLATED)
jungle_zip.write('tensorboard.sh', compress_type=zipfile.ZIP_DEFLATED)

jungle_zip.close()