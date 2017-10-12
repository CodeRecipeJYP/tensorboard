import urllib.request

url = "https://firebasestorage.googleapis.com/v0/b/styletransfer-ba06f.appspot.com/o/chicago.jpg?alt=media&token=ada17c2f-a910-4cc5-a925-aed14333b334"
urllib.request.urlretrieve(url, "urlchicago.jpg")
