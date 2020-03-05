# POS Tagger for Bahasa Indonesia
This Part of Speech (POS) Tagger is made by utilizing morphological features of word. The maximum accuracy obtained is at 96.4%

### How To use:
1. Run ```app.py```
2. Open web browser (or postman), access ```http://127.0.0.1:5000/tag?sentence=```
3. Immediately type your sentence, e.g. ```http://127.0.0.1:5000/tag?sentence=127.0.0.1:5000/tag?sentence=Beberapa penelitian menunjukkan bahwa pemanfaatan morfologis kata meningkatkan performa dari tagger.```
4. The result will be shown in dictionary format such as ```{"result": "Beberapa/CD penelitian/NN menunjukkan/VB bahwa/SC pemanfaatan/NN morfologis/NN kata/VB meningkatkan/VB performa/NN dari/IN tagger/NN ./Z"}```
5. The address of API can be changed manually in the code.