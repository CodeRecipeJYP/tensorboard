import time

import os

from download.download_script import downloadtraineddatafromftp
from memory import printMemory
from styletransfer import config
from styletransfer.src.model import styletransfer_model, StyleModel
from styletransfer.src.utils import get_img, save_img


# def feedfoward_with_func(content_img):
#     output_img = styletransfer_model(content_img)
#     save_img(config.OUTPUT_PATH(), output_img[0])


def feedfoward_with_clazz(styleModel, content_img, stylename):
    output_img = styleModel.feedfoward(content_img)
    save_img(config.OUTPUT_PATH(stylename), output_img[0])


def main():
    downloaded = downloadtraineddatafromftp(config.CKPT_BASE)
    tasks = downloaded

    printMemory()
    content_img = get_img(config._CONTENT_PATH)
    printMemory()
    iteration = len(tasks)
    start = time.time()
    printMemory()

    styleModel = StyleModel()
    printMemory()
    styleModel.init_network()
    printMemory()

    for i, stylename in enumerate(tasks):
        ckpt_dir = os.path.join(config.CKPT_BASE, stylename)
        styleModel.load_ckpt(ckpt_dir)
        printMemory()
        feedfoward_with_clazz(styleModel, content_img, stylename)
        printMemory()
        # feedfoward_with_func(content_img)
        cur = time.time()
        elapsed = cur - start
        print("Iteration %s, Elapsed time %s" % (i, elapsed))

    final = time.time()
    elapsed = final - start
    print("Iteration %s, Average Elapsed time %s" % (iteration, elapsed/iteration))


if __name__ == '__main__':
    main()