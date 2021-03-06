from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
from tqdm import tqdm

from .utils import *

def main():
    mnist = input_data.read_data_sets("/tmp/data/")

    n_inputs = 28 * 28
    n_hidden1 = 300
    n_hidden2 = 150
    n_hidden3 = n_hidden1
    n_outputs = n_inputs

    learning_rate = 0.01
    noise_level = 1.0

    X = tf.placeholder(tf.float32, shape=[None, n_inputs])
    X_noisy = X + noise_level * tf.random_normal(tf.shape(X))

    hidden1 = tf.layers.dense(X_noisy, n_hidden1, activation=tf.nn.relu, name="hidden1")
    hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.relu, name="hidden2")
    hidden3 = tf.layers.dense(hidden2, n_hidden3, activation=tf.nn.relu, name="hidden3")
    outputs = tf.layers.dense(hidden3, n_outputs, name="outputs")

    reconstruction_loss = tf.reduce_mean(tf.square(outputs - X))

    optimizer = tf.train.AdamOptimizer(learning_rate)
    training_op = optimizer.minimize(reconstruction_loss)

    init = tf.global_variables_initializer()

    n_epochs = 50
    batch_size = 100

    with tf.Session() as sess:
        init.run()
        for epoch in range(n_epochs):
            n_batches = mnist.train.num_examples // batch_size
            for iteration in tqdm(range(n_batches)):
                X_batch, y_batch = mnist.train.next_batch(batch_size)
                sess.run(training_op, feed_dict={X: X_batch})
            loss_train = reconstruction_loss.eval(feed_dict={X: X_batch})
            print("\r{}".format(epoch), "Train MSE:", loss_train)

        n_test_digits = 2
        X_test = mnist.test.images[:n_test_digits]
        outputs_val = outputs.eval(feed_dict={X: X_test})

    show_reconstructed_digits(X_test, outputs_val, 2)

if __name__ == '__main__':
    main()
