def firebasestorage():
    from firebase.fb_account import config
    import pyrebase
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    # as admin
    filepath = "data/outputs/wave_20171009195003.png"
    storage.child("images/wave_20171009195003.png").put(filepath)
