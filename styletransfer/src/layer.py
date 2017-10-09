import tensorflow as tf

WEIGHTS_INIT_STDEV = .1
#
# def conv_layer(input, size_in, size_out, name="conv"):
#   with tf.name_scope(name):
#     w = tf.Variable(tf.truncated_normal([5, 5, size_in, size_out], stddev=0.1), name="W")
#     b = tf.Variable(tf.constant(0.1, shape=[size_out]), name="B")
#     conv = tf.nn.conv2d(input, w, strides=[1, 1, 1, 1], padding="SAME")
#     act = tf.nn.relu(conv + b)
#     tf.summary.histogram("weights", w)
#     tf.summary.histogram("biases", b)
#     tf.summary.histogram("activations", act)
#     return tf.nn.max_pool(act, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
#
#
# def fc_layer(input, size_in, size_out, name="fc"):
#   with tf.name_scope(name):
#     w = tf.Variable(tf.truncated_normal([size_in, size_out], stddev=0.1), name="W")
#     b = tf.Variable(tf.constant(0.1, shape=[size_out]), name="B")
#     act = tf.nn.relu(tf.matmul(input, w) + b)
#     tf.summary.histogram("weights", w)
#     tf.summary.histogram("biases", b)
#     tf.summary.histogram("activations", act)
#     return act

def _conv_layer(net, num_filters, filter_size, strides, relu=True):
  weights_init = _conv_init_vars(net, num_filters, filter_size)
  strides_shape = [1, strides, strides, 1]
  net = tf.nn.conv2d(net, weights_init, strides_shape, padding='SAME')
  net = _instance_norm(net)
  if relu:
    net = tf.nn.relu(net)

  return net

def _conv_tranpose_layer(net, num_filters, filter_size, strides):
  weights_init = _conv_init_vars(net, num_filters, filter_size, transpose=True)

  batch_size, rows, cols, in_channels = [i.value for i in net.get_shape()]
  new_rows, new_cols = int(rows * strides), int(cols * strides)
  # new_shape = #tf.pack([tf.shape(net)[0], new_rows, new_cols, num_filters])

  new_shape = [batch_size, new_rows, new_cols, num_filters]
  tf_shape = tf.stack(new_shape)
  strides_shape = [1, strides, strides, 1]

  net = tf.nn.conv2d_transpose(net, weights_init, tf_shape, strides_shape, padding='SAME')
  net = _instance_norm(net)
  return tf.nn.relu(net)

def _residual_block(net, filter_size=3):
  tmp = _conv_layer(net, 128, filter_size, 1)
  return net + _conv_layer(tmp, 128, filter_size, 1, relu=False)

def _instance_norm(net, train=True):
  batch, rows, cols, channels = [i.value for i in net.get_shape()]
  var_shape = [channels]
  mu, sigma_sq = tf.nn.moments(net, [1, 2], keep_dims=True)
  shift = tf.Variable(tf.zeros(var_shape))
  scale = tf.Variable(tf.ones(var_shape))
  epsilon = 1e-3
  normalized = (net - mu) / (sigma_sq + epsilon) ** (.5)
  return scale * normalized + shift

def _conv_init_vars(net, out_channels, filter_size, transpose=False):
  _, rows, cols, in_channels = [i.value for i in net.get_shape()]
  if not transpose:
    weights_shape = [filter_size, filter_size, in_channels, out_channels]
  else:
    weights_shape = [filter_size, filter_size, out_channels, in_channels]

  weights_init = tf.Variable(tf.truncated_normal(weights_shape, stddev=WEIGHTS_INIT_STDEV, seed=1), dtype=tf.float32)
  return weights_init
