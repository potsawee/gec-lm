'''
Script for calling sequence labeler to make predictions
'''

import sys
# specify path to sequence labeler's directory here
path_to_labeler = '/home/alta/BLTSpeaking/ged-pm574/local/sequence-labeler'
sys.path.insert(0, path_to_labeler)

import labeler
import experiment
import numpy
import collections

class WordPrediction(object):
    def __init__(self):
        self.word = ''
        self.c_prob = None
        self.i_prob = None
    def __init__(self, word, c_prob, i_prob):
        self.word = word
        self.c_prob = c_prob
        self.i_prob = i_prob
    def add(self, word, c_prob, i_prob):
        self.word = word
        self.c_prob = c_prob
        self.i_prob = i_prob


def labeler_predict(model_path, input_file, c_prob=True):
    '''
    c_prob = True : print the prob of being correct
    c_prob = False: print the prob of being incorrect
    '''
    model = labeler.SequenceLabeler.load(model_path)
    config = model.config

    predictions_cache = {}
    sentences_prediction = [] # a list of sentence_prediction
                              # sentence_prediction = a list of word_prediciton

    sentences_test = experiment.read_input_files(input_file)
    batches_of_sentence_ids = experiment.create_batches_of_sentence_ids(sentences_test, config["batch_equal_size"], config['max_batch_size'])

    if c_prob:
        k = 0
    else: # i_prob
        k = -1

    for sentence_ids_in_batch in batches_of_sentence_ids:
        batch = [sentences_test[i] for i in sentence_ids_in_batch]
        cost, predicted_labels, predicted_probs = model.process_batch(batch, is_training=False, learningrate=0.0)

        assert(len(sentence_ids_in_batch) == len(predicted_labels))

        for i in range(len(sentence_ids_in_batch)):
            key = str(sentence_ids_in_batch[i])

            predictions = []

            for j in range(len(predicted_probs[i])):
                predictions.append(predicted_probs[i][j][k])
            predictions_cache[key] = predictions

    sentence_id = 0
    word_id = 0

    sentence_prediction = []

    with open(input_file, "r") as f:
        for line in f:

            if len(line.strip()) == 0: # end of a sentence
                # print("")
                sentences_prediction.append(sentence_prediction)
                sentence_prediction = []
                if word_id == 0:
                    continue
                assert(len(predictions_cache[str(sentence_id)]) == word_id), str(len(predictions_cache[str(sentence_id)])) + " " + str(word_id)
                sentence_id += 1
                word_id = 0
                continue
            assert(str(sentence_id) in predictions_cache)
            assert(len(predictions_cache[str(sentence_id)]) > word_id)

            word = line.split()[0]

            # print(line.strip() + "\t" + predictions_cache[str(sentence_id)][word_id].strip())
            prob = predictions_cache[str(sentence_id)][word_id]
            if c_prob:
                word_prediction = WordPrediction(word, prob, 1-prob)
            else: # i_prob
                word_prediction = WordPrediction(word, 1-prob, prob)

            sentence_prediction.append(word_prediction)
            word_id += 1

    return sentences_prediction
