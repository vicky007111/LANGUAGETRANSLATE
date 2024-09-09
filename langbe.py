from flask import Flask, request, jsonify
from googletrans import Translator

app=Flask(__name__)
translator=Translator()

def enq(item,queue):
    queue.append(item)

def deq(queue):
    if len(queue)== 0:
        return None
    return queue.pop(0)

@app.route('/translate', methods=['POST'])
def translate_text():
    data=request.json
    text=data['text']  # Get the input text
    target_lang=data['lang']  # Get the target language code

    input_queue = []
    output_queue = []

    # Split the text into sentences using '.' as the delimiter, and keep the periods
    sentences = [sentence.strip()+ '.' for sentence in text.split('.') if sentence]

    # Enqueue each sentence into the input queue
    for sentence in sentences:
        enq(sentence, input_queue)

    # Dequeue each sentence, translate it, and enqueue the translated sentence into the output queue
    while len(input_queue)>0:
        translated=deq(input_queue)
        if translated:
            translated_sentence = translator.translate(translated, dest=target_lang).text
            enq(translated_sentence, output_queue)

    # Dequeue all translated sentences and combine them into a single string
    translated_text =' '.join([deq(output_queue) for _ in range(len(output_queue))])

    if translated_text:
        return jsonify({'translatedText': translated_text})
    else:
        return jsonify({'error': 'Translation failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
