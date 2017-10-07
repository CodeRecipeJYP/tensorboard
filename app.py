import tensorflow as tf


LOGDIR = '/tmp/mnist_tutorial/'
GIST_URL = 'https://gist.githubusercontent.com/dandelionmane/4f02ab8f1451e276fea1f165a20336f1/raw/dfb8ee95b010480d56a73f324aca480b3820c180'

def main():
    mnist = tf.contrib.learn.datasets.mnist.read_data_sets(train_dir=LOGDIR + 'data', one_hot=True)
    print(mnist)

if __name__ == '__main__':
    main()