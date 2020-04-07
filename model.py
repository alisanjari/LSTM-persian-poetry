import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.callbacks import ModelCheckpoint

PATH_POEMS = 'D:/poem/molana_chapter2.txt'
PATH_SAVE_MODEL_ARCHITECTURE = 'D:/poem/model2/model128_128.yaml'
PATH_SAVE_MODEL_PARAMETERS = 'D:/poem/model12_8128/weights-{epoch:02d}-{loss:.3f}.hdf5'


PATH_POEMS = r'D:\learning-ai\LSTM-persian-poetry\poem_data\full_molana.txt'
PATH_SAVE_MODEL_ARCHITECTURE = r'D:\learning-ai\LSTM-persian-poetry\model_data\molana_model128_128.yaml'
PATH_SAVE_MODEL_PARAMETERS = r'D:\learning-ai\LSTM-persian-poetry\model_data\molana_model128_128-weights-{epoch:02d}-{loss:.3f}.hdf5'
PATH_SAVE_ENCODINGS = r'D:\learning-ai\LSTM-persian-poetry\model_data\molana_model128_128-encoding.p'

with open(PATH_POEMS, 'r', encoding='utf-16') as textfile:
    lines = [line for i, line in enumerate(textfile) ]
    corpus = ''.join(lines)

chars = sorted(list(set(corpus)))
num_chars = len(chars)

encoding = {c: i for i, c in enumerate(chars)}
decoding = {i: c for i, c in enumerate(chars)}


encoding_decoding = { "encoding": encoding, "decoding": decoding }
pickle.dump( encoding_decoding, open( PATH_SAVE_ENCODINGS, "wb" ) )

print("Our corpus contains {0} unique characters.".format(num_chars))

# it slices, it dices, it makes julienned datasets!
# chop up our data into X and y, slice into roughly (num_chars / skip) overlapping 'sentences'
# of length sentence_length, and encode the chars

sentence_length = 80
skip = 1
X_data = []
y_data = []

for i in range (0, len(corpus) - sentence_length, skip):
    sentence  = corpus[i:i + sentence_length]
    next_char = corpus[i + sentence_length]

    X_data.append([encoding[char] for char in sentence])
    y_data.append(encoding[next_char])

num_sentences = len(X_data)
print("Sliced our corpus into {0} sentences of length {1}".format(num_sentences, sentence_length))


# Vectorize our data and labels. We want everything in one-hot
# because smart data encoding cultivates phronesis and virtue.
print("Vectorizing X and y...")
X = np.zeros((num_sentences, sentence_length, num_chars), dtype=np.bool)
y = np.zeros((num_sentences, num_chars), dtype=np.bool)

for i, sentence in enumerate(X_data):
    for t, encoded_char in enumerate(sentence):
        X[i, t, encoded_char] = 1
    y[i, y_data[i]] = 1

# Double check our vectorized data before we sink hours into fitting a model
print("Sanity check y. Dimension: {0} # Sentences: {1} Characters in corpus: {2}".format(y.shape, num_sentences, len(chars)))
print("Sanity check X. Dimension: {0} Sentence length: {1}".format(X.shape, sentence_length))



# Define our model
print("Let's build a brain!")

model = Sequential()
model.add(LSTM(128, input_shape=(sentence_length, num_chars)))
#model.add(LSTM(128, input_shape=(sentence_length, num_chars)))
model.add(Dense(num_chars))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')



# Dump our model architecture to a file so we can load it elsewhere
architecture = model.to_yaml()
with open(PATH_SAVE_MODEL_ARCHITECTURE, 'a') as model_file:
    model_file.write(architecture)

# Set up checkpoints
checkpoint = ModelCheckpoint(PATH_SAVE_MODEL_PARAMETERS, monitor="loss", verbose=1, save_best_only=True, mode="min")
callbacks = [checkpoint]

# Action time! [Insert guitar solo here]
model.fit(X, y, nb_epoch=3, batch_size=128, callbacks=callbacks)