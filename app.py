from flask import Flask
from flask_restful import Api, Resource, reqparse

import os
from nltk import word_tokenize
from nltk import sent_tokenize
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from keras import backend as K
import json
from tensorflow import get_default_graph
import re

APP = Flask(__name__)
API = Api(APP)

def ignore_class_accuracy(to_ignore=0):
    def ignore_accuracy(y_true, y_pred):
        y_true_class = K.argmax(y_true, axis=-1)
        y_pred_class = K.argmax(y_pred, axis=-1)
 
        ignore_mask = K.cast(K.not_equal(y_pred_class, to_ignore), 'int32')
        matches = K.cast(K.equal(y_true_class, y_pred_class), 'int32') * ignore_mask
        accuracy = K.sum(matches) / K.maximum(K.sum(ignore_mask), 1)
        return accuracy
    return ignore_accuracy

def load_pretrained_model():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    global graph
    global model
    graph = get_default_graph()
    model = load_model('model.hdf5',custom_objects={'ignore_accuracy': ignore_class_accuracy(0)})
    model._make_predict_function()

    global MAX_LENGTH
    MAX_LENGTH = 82
    global word2index
    global prefix_rule, suffix_rule
    global prefix2index, suffix2index
    global inv_tag2index

    with open('word2index.json') as f:
        word2index = json.loads(f.read())
    with open('tag2index.json') as f:
        tag2index = json.loads(f.read())
    inv_tag2index = {v: k for k, v in tag2index.items()}
    with open('prefix2index.json') as f:
        prefix2index = json.loads(f.read())
    with open('suffix2index.json') as f:
        suffix2index = json.loads(f.read())
    prefixes = [x for x in prefix2index.keys() if '-' not in x]
    prefixes = sorted(prefixes, key= lambda x: len(x), reverse=True)
    prefix_rule = '|'.join([r'^'+i for i in prefixes])
    suffixes = [x for x in suffix2index.keys() if '-' not in x]
    suffixes = sorted(suffixes, key= lambda x: len(x), reverse=True)
    suffix_rule = '|'.join([i+r'$' for i in suffixes])

class postag(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sentence',type=str)

        args = parser.parse_args()
        sentence = args['sentence']

        sentence = [word_tokenize(word) for word in sent_tokenize(sentence)]

        sentences_X = []
        for s in sentence:
            s_int = []
            for w in s:
                w_int = []
                try:
                    w_int.append(word2index[w.lower()])
                    prefix = re.search(prefix_rule,w.lower())
                    suffix = re.search(suffix_rule,w.lower())
                    if prefix != None:
                        w_int.append(prefix2index[prefix[0]])
                    else:
                        w_int.append(prefix2index['-NA-']) #has no prefix
                    if suffix != None:
                        w_int.append(suffix2index[suffix[0]])
                    else:
                        w_int.append(suffix2index['-NA-']) #has no suffix            
                    if w.lower() == w:
                        w_int.append(0) # non-capital
                    else:
                        w_int.append(1) # capital
                except KeyError: # OOV
                    w_int.append(word2index['-OOV-'])
                    prefix = re.search(prefix_rule,w.lower())
                    suffix = re.search(suffix_rule,w.lower())
                    if prefix != None:
                        w_int.append(prefix2index[prefix[0]])
                    else:
                        w_int.append(prefix2index['-NA-']) #has no prefix
                    if suffix != None:
                        w_int.append(suffix2index[suffix[0]])
                    else:
                        w_int.append(suffix2index['-NA-']) #has no suffix            
                    if w.lower() == w:
                        w_int.append(0) # non-capital
                    else:
                        w_int.append(1) # capital
                s_int.append(w_int)
            sentences_X.append(s_int)

        sentences_X = pad_sequences(sentences_X, maxlen=MAX_LENGTH, padding='post')
        sentences_X_embedded = np.array([[i[0] for i in j] for j in sentences_X])
        sentences_X_engineered = np.array([[i[1:] for i in j] for j in sentences_X])
        
        predicted = model.predict([sentences_X_embedded,sentences_X_engineered])
        predicted = [[np.argmax(i) for i in j] for j in predicted] #argmax
        #K.clear_session()
        
        result = []
        for i,j in zip(sentence,predicted):
            for k,l in zip(i,j):
                result.append(k+'/'+inv_tag2index[l])
        result = ' '.join(result)
        return {'result':result}

API.add_resource(postag, '/tag')

if __name__ == '__main__':
    load_pretrained_model()
    APP.run(debug=True)