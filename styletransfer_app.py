import time

import os

from download.download_script import downloadtraineddatafromftp, downloadcontentfromurl, mkdir_unless_exist
from memory import printMemory
from styletransfer import config
from styletransfer.src.model import styletransfer_model, StyleModel
from styletransfer.src.utils import get_img, save_img
import skimage.transform


# def feedfoward_with_func(content_img):
#     output_img = styletransfer_model(content_img)
#     save_img(config.OUTPUT_PATH(), output_img[0])
SIZE = [474, 712]

def feedfoward_with_clazz(styleModel, content_img, stylename):
    output_img = styleModel.feedfoward(content_img)
    save_img(config.OUTPUT_PATH(stylename), output_img[0])


def crop_img(content_img):
    original_siz = content_img.shape
    crop_st = int((original_siz[0]/2) - (SIZE[0]/2)), int((original_siz[1]/2) - (SIZE[1]/2))
    return content_img[crop_st[0]:crop_st[0]+SIZE[0],crop_st[1]:crop_st[1]+SIZE[1]]


def get_dirnames(target):
    for (path, dir, files) in os.walk(target):
        return dir


def resize_img(image):
    return skimage.transform.resize(image, SIZE)


def main():
    # from firebase.db import firebasedb
    # firebasedb()
    # from firebase.storage import firebasestorage
    # firebasestorage()

    # downloaded = downloadtraineddatafromftp(config.CKPT_BASE)
    url = "https://scontent-icn1-1.xx.fbcdn.net/v/t31.0-8/22459128_1676848559024079_955624277813855533_o.jpg?oh=f8463db22482524ca9c6748ac5ad40bd&oe=5A629DDB"
    # url = "https://scontent-icn1-1.xx.fbcdn.net/v/t31.0-8/22519801_1683350981707170_4623081986041934371_o.jpg?oh=82036de63e7408d432eeaef1085e6d33&oe=5A812D08"
    # url = "https://firebasestorage.googleapis.com/v0/b/styletransfer-ba06f.appspot.com/o/chicago.jpg?alt=media&token=ada17c2f-a910-4cc5-a925-aed14333b334"
    # url = "https://firebasestorage.googleapis.com/v0/b/styletransfer-ba06f.appspot.com/o/photo.jpg?alt=media&token=ecea1013-3947-4e2d-ad9e-bafa93159806"
    # # url = "https://trello-attachments.s3.amazonaws.com/58d8e46f3932af08817b04fd/59dd8196c14ca71a19dfca96/569ce45e10adfc260c0c86dc572db000/chicago.jpg"
    filename = "chicago.jpg"
    downloadcontentfromurl(url, config.CONTENT_BASE, filename)
    # tasks = downloaded

    tasks = get_dirnames("data/ckpts")
    mkdir_unless_exist(config.OUTPUT_DIR)


    # printMemory()
    content_img = get_img(config._CONTENT_PATH)
    content_img = resize_img(content_img)
    # content_img = crop_img(content_img)
    # printMemory()
    iteration = len(tasks)
    start = time.time()
    # printMemory()
    #
    styleModel = StyleModel()
    # printMemory()
    styleModel.init_network()
    # printMemory()
    #
    ckpt_dir = os.path.join(config.CKPT_BASE, tasks[0])
    styleModel.load_ckpt(ckpt_dir)
    for i, stylename in enumerate(tasks):
        # ckpt_dir = os.path.join(config.CKPT_BASE, stylename)
        # styleModel.load_ckpt(ckpt_dir)
        # printMemory()
        feedfoward_with_clazz(styleModel, content_img, stylename)
        # printMemory()
        # feedfoward_with_func(content_img)
        cur = time.time()
        elapsed = cur - start
        print("Iteration %s, Elapsed time %s" % (i, elapsed))

    final = time.time()
    elapsed = final - start
    print("Iteration %s, Average Elapsed time %s" % (iteration, elapsed/iteration))


if __name__ == '__main__':
    main()