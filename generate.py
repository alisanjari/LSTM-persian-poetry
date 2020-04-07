import numpy as np
from tensorflow.keras.models import model_from_yaml
from random import randint


PATH_TO_SAVE = 'D:/learning-ai/poem/test_molana.txt'


class GenerativeNetwork:

    def __init__(self, corpus_path, model_path, weights_path):
        with open(corpus_path, encoding='utf-16') as corpus_file:
            self.corpus =  corpus_file.read()

        # Get a unique identifier for each char in the corpus,
        # then make some dicts to ease encoding and decoding

        self.chars = sorted(list(set(self.corpus)))
        self.encoding = {c: i for i, c in enumerate(self.chars)}
        self.decoding = {i: c for i, c in enumerate(self.chars)}

        print(len(self.chars))

        print(self.chars)



        # Some fields we'll need later
        self.num_chars = len(self.chars)
        self.sentence_length = 50
        self.corpus_length = len(self.corpus)

        # Build our network from loaded architecture and weights
        with open(model_path) as model_file:
            architecture = model_file.read()

        self.model = model_from_yaml(architecture)
        self.model.load_weights(weights_path)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

    def generate(self, seed_pattern):

        X = np.zeros((1, self.sentence_length, self.num_chars), dtype=np.bool)
        for i, character in enumerate(seed_pattern):

            X[0, i, self.encoding[character]] = 1

        generated_text = ""

        for i in range(1500):

            prediction = np.argmax(self.model.predict(X, verbose=0))
            generated_text += self.decoding[prediction]
            activations = np.zeros((1, 1, self.num_chars), dtype=np.bool)
            activations[0, 0, prediction] = 1
            X = np.concatenate((X[:, 1:, :], activations), axis=1)

        return generated_text

    def make_seed(self, seed_phrase=""):

        if seed_phrase:

            phrase_length = len(seed_phrase)

            pattern = ""

            for i in range (0, self.sentence_length):

                pattern += seed_phrase[i % phrase_length]

        else:

            seed = randint(0, self.corpus_length - self.sentence_length)
            pattern = self.corpus[seed:seed + self.sentence_length]



        return pattern


model = GenerativeNetwork(corpus_path='D:/learning-ai/poem/molana_chapter2.txt',
                          model_path='D:/learning-ai/poem/model2/model.yaml',
                          weights_path="D:/learning-ai/poem/model2/weights-02-0.446.hdf5")



seed_pattern0 = model.make_seed()
model_generated_poem = model.generate(seed_pattern0)

with open(PATH_TO_SAVE, 'w', newline='', encoding='utf-16') as writefile:
    writefile.write(model_generated_poem[::-1])