import urllib.request

url = "https://firebasestorage.googleapis.com/v0/b/styletransfer-ba06f.appspot.com/o/chicago.jpg?alt=media&token=ada17c2f-a910-4cc5-a925-aed14333b334"
# url = "ftp://admin:12345677@yangyinetwork.asuscomm.com/My_Passport/Download2/workspace/data/DeepArts/fast-style-transfer/image_style_dataset/nature/nature0001.jpg"
urllib.request.urlretrieve(url, "urlnature.jpg")
