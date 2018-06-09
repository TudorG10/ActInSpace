import keras
import tensorflow as tf
class MyCallbacks(keras.callbacks.Callback):
    def __init__(self, pretrained_file):
        self.pretrained_file = pretrained_file
        self.sess = keras.backend.get_session()
        self.saver = tf.train.Saver()
    def on_train_begin(self, logs=None):
        if self.pretrian_model_path:
            self.saver.restore(self.sess, self.pretrian_model_path)
            print('load weights: OK.')


#model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
testCallBack = MyCallbacks(pretrained_file='_retrain_checkpoint.data-00000-of-00001') 
model.fit(x_train, y_train, batch_size=128, epochs=1, callbacks=[testCallBack])
