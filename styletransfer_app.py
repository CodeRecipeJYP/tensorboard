import time

from memory import printMemory
from styletransfer import config
from styletransfer.src.model import styletransfer_model, StyleModel
from styletransfer.src.utils import get_img, save_img


def feedfoward_with_func(content_img):
    output_img = styletransfer_model(content_img)
    save_img(config.OUTPUT_PATH(), output_img[0])


def feedfoward_with_clazz(styleModel, content_img):
    output_img = styleModel.feedfoward(content_img)
    save_img(config.OUTPUT_PATH(), output_img[0])


def main():
    printMemory()
    content_img = get_img(config._CONTENT_PATH)
    printMemory()
    iteration = 10
    start = time.time()
    printMemory()

    styleModel = StyleModel()
    printMemory()
    styleModel.init_network()
    printMemory()
    styleModel.load_ckpt()
    printMemory()
    for i in range(iteration):
        printMemory()
        feedfoward_with_clazz(styleModel, content_img)
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