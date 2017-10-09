import os

LEARNING_RATE = 1E-3
LOGDIR = '/tmp/styletransfer/'

# STYLE_DIR = "data/style"
# STYLE_FILENAME = "wave.jpg"
# _STYLE_NAME = os.path.splitext(STYLE_FILENAME)[0]
# _STYLE_PATH = os.path.join(STYLE_DIR, STYLE_FILENAME)

CONTENT_DIR = "data/content"
CONTENT_FILENAME = "chicago.jpg"
_CONTENT_NAME = os.path.splitext(CONTENT_FILENAME)[0]
_CONTENT_PATH = os.path.join(CONTENT_DIR, CONTENT_FILENAME)

CKPT_BASE = "data/trained_data"

OUTPUT_DIR = "data/outputs"

CONTENT_SHAPE = (1, 474, 712, 3)

def OUTPUT_PATH(style_name=""):
    import time
    timestr = time.strftime("%Y%m%d%H%M%S")

    filename = style_name + "_" + timestr + ".png"
    return os.path.join(OUTPUT_DIR, filename)
