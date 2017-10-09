import os
import tensorflow as tf

from styletransfer import config
from styletransfer.src.layer import _conv_layer, _residual_block, _conv_tranpose_layer


class StyleModel():
    def init_network(self):
        tf.reset_default_graph()
        self.sess = tf.Session()

        self.img_placeholder = tf.placeholder(tf.float32, shape=config.CONTENT_SHAPE,
                                     name='img_placeholder')
        self.preds = feedfoward_net(self.img_placeholder)

    def load_ckpt(self):
        saver = tf.train.Saver()
        if os.path.isdir(config.CKPT_DIR):
            ckpt = tf.train.get_checkpoint_state(config.CKPT_DIR)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(self.sess, ckpt.model_checkpoint_path)
            else:
                raise Exception("No checkpoint found...")
        else:
            saver.restore(self.sess, config.CKPT_DIR)

    def feedfoward(self, img):
        _preds = self.sess.run(self.preds, feed_dict={self.img_placeholder: [img]})
        return _preds


def feedfoward_net(img):
    conv1 = _conv_layer(img, 32, 9, 1)
    conv2 = _conv_layer(conv1, 64, 3, 2)
    conv3 = _conv_layer(conv2, 128, 3, 2)
    resid1 = _residual_block(conv3, 3)
    resid2 = _residual_block(resid1, 3)
    resid3 = _residual_block(resid2, 3)
    resid4 = _residual_block(resid3, 3)
    resid5 = _residual_block(resid4, 3)
    conv_t1 = _conv_tranpose_layer(resid5, 64, 3, 2)
    conv_t2 = _conv_tranpose_layer(conv_t1, 32, 3, 2)
    conv_t3 = _conv_layer(conv_t2, 3, 9, 1, relu=False)
    preds = tf.nn.tanh(conv_t3) * 150 + 255. / 2
    return preds


def stylemodel(img_placeholder):
    preds = feedfoward_net(img_placeholder)

    return preds


def styletransfer_model(img, batch_size=1):
    from styletransfer import config

    tf.reset_default_graph()
    sess = tf.Session()

    img_shape = img.shape
    batch_shape = (batch_size,) + img_shape

    img_placeholder = tf.placeholder(tf.float32, shape=batch_shape,
                                     name='img_placeholder')
    preds = feedfoward_net(img_placeholder)

    saver = tf.train.Saver()
    if os.path.isdir(config.CKPT_DIR):
        ckpt = tf.train.get_checkpoint_state(config.CKPT_DIR)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            raise Exception("No checkpoint found...")
    else:
        saver.restore(sess, config.CKPT_DIR)

    _preds = sess.run(preds, feed_dict={img_placeholder: [img]})
    return _preds
    #
    # x_image = tf.reshape(x, [-1, 28, 28, 1])
    # tf.summary.image('input', x_image, 3)
    # y = tf.placeholder(tf.float32, shape=[None, 10], name="labels")
    #
    # conv1 = conv_layer(x_image, 1, 32, "conv1")
    # conv_out = conv_layer(conv1, 32, 64, "conv2")
    #
    # flattened = tf.reshape(conv_out, [-1, 7 * 7 * 64])
    #
    # fc1 = fc_layer(flattened, 7 * 7 * 64, 1024, "fc1")
    # embedding_input = fc1
    # embedding_size = 1024
    # logits = fc_layer(fc1, 1024, 10, "fc2")
    #
    # with tf.name_scope("xent"):
    #     xent = tf.reduce_mean(
    #         tf.nn.softmax_cross_entropy_with_logits(
    #             logits=logits, labels=y), name="xent")
    #     tf.summary.scalar("xent", xent)
    #
    # with tf.name_scope("train"):
    #     train_step = tf.train.AdamOptimizer(config.LEARNING_RATE).minimize(xent)
    #
    # with tf.name_scope("accuracy"):
    #     correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
    #     accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #     tf.summary.scalar("accuracy", accuracy)
    #
    # summ = tf.summary.merge_all()
    #
    # embedding = tf.Variable(tf.zeros([1024, embedding_size]), name="test_embedding")
    # assignment = embedding.assign(embedding_input)
    # saver = tf.train.Saver()
    #
    # sess.run(tf.global_variables_initializer())
    # writer = tf.summary.FileWriter(config.LOGDIR + config.STYLE)
    # writer.add_graph(sess.graph)
    #
    # config = tf.contrib.tensorboard.plugins.projector.ProjectorConfig()
    # embedding_config = config.embeddings.add()
    # embedding_config.tensor_name = embedding.name
    #
    # embedding_config.sprite.single_image_dim.extend([28, 28])
    # tf.contrib.tensorboard.plugins.projector.visualize_embeddings(writer, config)
    #
    # run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    # run_metadata = tf.RunMetadata()
    #
    # for i in range(501):
    #     batch = mnist.train.next_batch(100)
    #     if i % 5 == 0:
    #         [train_accuracy, s] = sess.run([accuracy, summ],
    #                                        feed_dict={
    #                                            x: batch[0],
    #                                            y: batch[1]},
    #                                        options=run_options,
    #                                        run_metadata=run_metadata)
    #         writer.add_summary(s, i)
    #         writer.add_run_metadata(run_metadata, 'step%d' % i)
    #         print('step%04d, train_accuracy = %02.1f %%' % (i, train_accuracy*100))
    #     if i % 500 == 0:
    #         sess.run(assignment, feed_dict={x: mnist.test.images[:1024], y: mnist.test.labels[:1024]})
    #         saver.save(sess, os.path.join(config.LOGDIR, "model.ckpt"), i)
    #     sess.run(train_step, feed_dict={x: batch[0], y: batch[1]})
