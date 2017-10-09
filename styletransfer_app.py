import time

from styletransfer import config
from styletransfer.src.model import styletransfer_model
from styletransfer.src.utils import get_img, save_img


def feedfoward_with_func(content_img):
    output_img = styletransfer_model(content_img)
    save_img(config.OUTPUT_PATH(), output_img[0])


def main():
    content_img = get_img(config._CONTENT_PATH)
    iteration = 10
    start = time.time()

    for i in range(iteration):
        feedfoward_with_func(content_img)
        cur = time.time()
        elapsed = cur - start
        print("Iteration %s, Elapsed time %s" % (i, elapsed))

    final = time.clock()
    elapsed = final - start
    print("Iteration %s, Average Elapsed time %s" % (iteration, elapsed/iteration))


if __name__ == '__main__':
    main()