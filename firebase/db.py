from firebase.fb_account import config


def firebasedb():
    import pyrebase



    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("users").child("Morty")
    data = {"name": "Mortimer 'Morty' Smith"}
    db.child("users").push(data)

    def stream_handler(message):
        print(message["event"])  # put
        print(message["path"])  # /-K7yGTTEp7O549EzTYtI
        print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}

    my_stream = db.child("users").stream(stream_handler)