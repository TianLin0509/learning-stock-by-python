import tushare as ts
import numpy as np
import pandas as pd
from tensorflow.python.keras import *
from tensorflow.python.keras.layers import *
import tensorflow as tf
import netron
import random
from mpl_finance import candlestick_ochl
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

datas = np.load('june4.npy')
print(datas.shape)
print('load data complete')
train_data = datas[:1100]
test_data = datas[1100:]
inputs = train_data[:, :250]
labels = train_data[:, 250: 254]
test_inputs = test_data[:, :250]
test_labels = test_data[:, 250: 254]

input_data = Input(name='input_data', shape=(250,))
temp = BatchNormalization()(input_data)
temp = Dense(2048, activation='relu')(temp)
temp = BatchNormalization()(temp)
temp = Dense(1024, activation='relu')(temp)
temp = BatchNormalization()(temp)
temp = Dense(512, activation='relu')(temp)
temp = BatchNormalization()(temp)
temp = Dense(256, activation='relu')(temp)
temp = BatchNormalization()(temp)
temp = Dense(64, activation='relu')(temp)
output_predict = Dense(4)(temp)
model = Model(inputs=input_data, outputs=output_predict)
model.compile(optimizer='adam', loss='mse')
model.summary()
checkpoint = callbacks.ModelCheckpoint('model.h5', monitor='val_loss',
                                       verbose=1, save_best_only=True, mode='min', save_weights_only=False)
Ts = callbacks.TensorBoard(log_dir='./logs')
# netron.start('model.h5')
#model.fit(x=inputs, y=labels, batch_size=128, epochs=2000, verbose=2, validation_split=0.2, callbacks=[checkpoint, Ts])

model.load_weights('./model.h5')
pred = model.predict(test_inputs)
# normalize
# 除以各自开盘价，防止由于股价差距过大图画出来很难看
pred = np.einsum('ij,i->ij', pred, 1 / pred[:, 0])
test_labels = np.einsum('ij,i->ij', test_labels, 1 / test_labels[:, 0])
index = np.reshape(np.arange(pred.shape[0]), [-1, 1])
pred_for_plot = np.concatenate([index, pred], 1)
label_for_plot = np.concatenate([index, test_labels], 1)
fig = plt.figure()
ax1 = fig.add_subplot(211)
#fig, ax = plt.subplots()
candlestick_ochl(ax1, pred_for_plot, colordown='#53c156', colorup='#ff1717')
plt.title('网络预测股票周线')
ax2 = fig.add_subplot(212)
candlestick_ochl(ax2, label_for_plot, colordown='#53c156', colorup='#ff1717')
plt.title('真实周线')
plt.show()
pass
