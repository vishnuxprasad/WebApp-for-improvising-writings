from flask import Flask, render_template, request, jsonify
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

app = Flask(__name__)
app.debug = True
model_name = 'deep-learning-analytics/GrammarCorrector'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name).to(torch_device)

@app.route('/')
def home():
    return render_template('grammar-check-fe.html')

@app.route('/api/correct_grammar', methods=['POST'])
def api_correct_grammar():
    input_text = request.form.get('input_text')
    if not input_text:
        return jsonify({'error': 'Input text is empty'})

    num_return_sequences = 1  # Change this as needed

    # Perform grammar correction using the model
    batch = tokenizer(
        [input_text],
        truncation=True,
        padding='max_length',
        max_length=64,
        return_tensors="pt"
    ).to(torch_device)
    translated = model.generate(
        **batch,
        max_length=64,
        num_beams=4,
        num_return_sequences=num_return_sequences,
        temperature=1.5
    )
    corrected_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return jsonify({'corrected_text': corrected_text[0]})

if __name__ == '__main__':
    app.run()