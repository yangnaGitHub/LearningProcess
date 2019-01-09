import numpy as np
import tensorflow as tf
import tensorflow.contrib.rnn as rnn
import matplotlib.pyplot as plt

TIME_STEPS=10
BATCH_SIZE=128
HIDDEN_UNITS=1
LEARNING_RATE=0.001
EPOCH=150

TRAIN_EXAMPLES=11000
TEST_EXAMPLES=1100

def generate(seq):
    x = []
    y = []
    for i in range(len(seq) - TIME_STEPS):
        x.append([seq[i:i+TIME_STEPS]])
        y.append([seq[i+TIME_STEPS]])
    return np.array(x, dtype=np.float32), np.array(y, dtype=np.float32)

seq_train = np.sin(np.linspace(0, 100, TRAIN_EXAMPLES, dtype=np.float32))
seq_test = np.sin(np.linspace(100, 110, TEST_EXAMPLES, dtype=np.float32))

X_train, Y_train = generate(seq_train)
X_test, Y_test = generate(seq_test)

X_train = np.reshape(X_train, newshape=(-1, TIMES_STEPS, 1))
X_test = np.reshape(X_test, newshape(-1, TIME_STEPS, 1))

plt.plot(range(1000), Y_test(:1000, 0), 'r*')

defaultG = tf.Graph()
with defaultG.as_default():
    X_p = tf.placeholder(dtype=tf.float32, shape=(None, TIME_STEPS, 1), name="input_placeholder")
    Y_p = tf.placeholder(dtype=tf.float32, shape=(None, 1), name="pred_placeholder")

    lstm_cell = rnn.BasicLSTMCell(num_units=HIDDEN_UNITS)

    init_state = lstm_cell.zero_state(batch_szie=BATCH_SIZE, dtype=tf.float32)

    outputs, states = tf.nn.dynamic_rnn(cell=lstm_cell, inputs=X_p, initial_state=init_state, dtype=tf.float32)
    h = outputs[:, -1, :]

    mse = tf.losses.mean_squared_error(labels=Y_p, predictions=h)
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss=mse)
    init = tf.global_variables_initializer()

with tf.Session(graph=defaultG) as sess:
    sess.run(init)
    for epoch in range(1, EPOCH + 1):
        results = np.zeros(shape=(TEST_EXAMPLES, 1))
        train_losses = []
        test_losses = []
        for j in range(TRAIN_EXAMPLES/BATCH_SIZE):
            _, train_loss = sess.run(
                fetches=(optimizer, mse),
                feed_dict={
                    X_p:X_train[j*BATCH_SIZE:(j+1)*BATCH_SIZE],
                    Y_p:Y_train[j*BATCH_SIZE:(j+1)*BATCH_SIZE]
                }
            )
            train_losses.append(train_loss)
        print("average test loss:", sum(test_losses) / len(test_losses))
        plt.plot(range(1000), results[:1000, 0])
plt.show()