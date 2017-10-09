from styletransfer import config
from styletransfer.src.model import styletransfer_model
from styletransfer.src.utils import get_img, save_img


def main():
    style_target = get_img(config._STYLE_PATH)
    content_target_paths = [config._CONTENT_PATH]
    content_img = get_img(content_target_paths[0])
    output_img = styletransfer_model(content_img)
    save_img(config.OUTPUT_PATH(), output_img[0])


if __name__ == '__main__':
    main()