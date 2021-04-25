# POS Tagger for Bahasa Indonesia
This Part of Speech (POS) Tagger is made by utilizing morphological features of word. The maximum accuracy obtained is at 96.4%

### How To use
1. Run ```app.py```
2. Open web browser (or postman) or via GET request, access ```http://127.0.0.1:5000/tag?sentence=```
3. Immediately type your sentence, e.g. ```http://127.0.0.1:5000/tag?sentence=127.0.0.1:5000/tag?sentence=Beberapa penelitian menunjukkan bahwa pemanfaatan morfologis kata meningkatkan performa dari tagger.```
4. The result will be shown in dictionary format such as ```{"result": "Beberapa/CD penelitian/NN menunjukkan/VB bahwa/SC pemanfaatan/NN morfologis/NN kata/VB meningkatkan/VB performa/NN dari/IN tagger/NN ./Z"}```
5. The address of API can be changed manually in the code.

### Dependency
1. Flask
2. Flask-RESTful
3. Numpy
3. NLTK
4. Tensorflow
5. Keras

### Citation
If you want to use this API, please cite:

I. N. P. Trisna, A. Musdholifah and Y. Sari, "Utilizing Morphological Features for Part-of-Speech Tagging of Bahasa Indonesia in Bidirectional LSTM," 2020 6th International Conference on Science in Information Technology (ICSITech), 2020, pp. 51-56, doi: 10.1109/ICSITech49800.2020.9392076.

https://ieeexplore.ieee.org/abstract/document/9392076
