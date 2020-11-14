'''
keras: 大幅降低代码量
    compile
    fit
    evaluate
    predict
'''
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, optimizers, Sequential, metrics

# 预处理
def preprocess(x, y):
    x = tf.cast(x, dtype=tf.float32) / 255
    x = tf.reshape(x,[28*28])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x, y

(x, y), (x_test, y_test) = datasets.fashion_mnist.load_data()
print(x.shape, y.shape)

batch_size = 128
db = tf.data.Dataset.from_tensor_slices((x, y))
db = db.map(preprocess).shuffle(10000).batch(128)

db_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))
db_test = db_test.map(preprocess).shuffle(10000).batch(128)

db_iter = iter(db)
sample = next(db_iter)
print(sample[0].shape, sample[1].shape)

# 在容器中建立网络
model = Sequential([
    layers.Dense(256, activation=tf.nn.relu),  # 784 ->256
    layers.Dense(128, activation=tf.nn.relu),  # 256 ->128
    layers.Dense(64, activation=tf.nn.relu),  # 128 ->64
    layers.Dense(32, activation=tf.nn.relu),  # 64 ->32
    layers.Dense(10)  # 32 ->10
])
# 预创建
model.build(input_shape=[None, 28 * 28])
model.summary()
# w = w-lr*grad
optimizer = optimizers.Adam(lr=1e-3)


def main():
    # for epoch in range(30):
    #     for step, (x, y) in enumerate(db):
    #         x = tf.reshape(x, [-1, 28 * 28])

            model.compile(optimizer=optimizers.Adam(lr=0.01),
                          loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])
            model.fit(db, epochs=10, validation_data=db_test, validation_freq=2)

            # 和上面的validation_data功能一致，但是其由于在外面，Wimbledon可以根据精确度来进行早停止
            model.evaluate(db_test)


            # 将模型用于预测
            sample = next(iter((db_test)))
            x = sample[0]
            y = sample[1]
            pred = model(x)
            y = tf.argmax(y,axis=1)
            pred = tf.argmax(pred,axis=1)
            print(pred)
            print(y)
            print(tf.where(tf.equal(pred, y)==False))
            print(tf.gather_nd(pred,tf.where(tf.equal(pred, y)==False)))
            # with tf.GradientTape() as tape:
            #     # [b,784] [b,10]
            #     logits = model(x)
            #     y_onehot = tf.one_hot(y, depth=10)
            #     prob = tf.nn.softmax(logits, axis=1)
            #     loss = tf.reduce_mean(tf.losses.MSE(y_onehot, prob))
            #     loss2 = tf.reduce_mean(tf.losses.categorical_crossentropy(y_onehot, logits, from_logits=True))
            # # 自动获得当前梯度
            # grads = tape.gradient(loss, model.trainable_variables)
            # # 原地更新梯度
            # optimizer.apply_gradients(zip(grads, model.trainable_variables))

            # if step % 100 == 9:
            #     print(step, float(loss2), float(loss))
            #     # 拿测试集用于验证
            #     total_correct,total_num =0,0
            #     for x,y in db_test:
            #         x = tf.reshape(x, [-1, 28*28])
            #         logits = model(x) # [b,10]
            #         prob = tf.nn.softmax(logits, axis=1)
            #         #b,10 ==> [b]
            #         pred = tf.cast(tf.argmax(prob, axis=1),tf.int32)
            #         # true,equa;
            #         correct = tf.cast(tf.equal(pred,y),tf.int32)
            #         corrct_num = tf.reduce_sum(correct)
            #         total_correct += corrct_num
            #         total_num += x.shape[0]
            #     acc =total_correct/total_num
            #     print(acc)

if __name__ == '__main__':
    main()


