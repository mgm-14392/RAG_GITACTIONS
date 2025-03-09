from flask import Flask, request, render_template_string
from rag_mistral import RAGSystem
import os

app = Flask(__name__)

rag_system = RAGSystem()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        answer = rag_system.ask_question(question)
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Ask a Question</title>
                <style>
                    /* Add custom CSS to style the input box */
                    .question-input {
                        width: 80%; /* Adjust the width as needed */
                        height: 100px; /* Adjust the height as needed */
                        font-size: 16px; /* Adjust the font size as needed */
                        padding: 10px; /* Add padding for better appearance */
                        box-sizing: border-box; /* Ensure padding is included in width/height */
                    }
                    .submit-button {
                        margin-top: 10px; /* Add some space between input and button */
                        padding: 10px 20px; /* Add padding to the button */
                        font-size: 16px; /* Adjust the font size as needed */
                    }
                </style>
            </head>
            <body>
                <h1>Ask a Question</h1>
                <form method="post">
                    <textarea class="question-input" name="question" placeholder="Enter your question here..."></textarea>
                    <br>
                    <input class="submit-button" type="submit" value="Ask">
                </form>
                <h2>Answer:</h2>
                <p>{{ answer }}</p>
            </body>
            </html>
        ''', answer=answer)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ask a Question</title>
            <style>
                /* Add custom CSS to style the input box */
                .question-input {
                    width: 80%; /* Adjust the width as needed */
                    height: 100px; /* Adjust the height as needed */
                    font-size: 16px; /* Adjust the font size as needed */
                    padding: 10px; /* Add padding for better appearance */
                    box-sizing: border-box; /* Ensure padding is included in width/height */
                }
                .submit-button {
                    margin-top: 10px; /* Add some space between input and button */
                    padding: 10px 20px; /* Add padding to the button */
                    font-size: 16px; /* Adjust the font size as needed */
                }
            </style>
        </head>
        <body>
            <h1>Ask a Question</h1>
            <form method="post">
                <textarea class="question-input" name="question" placeholder="Enter your question here..."></textarea>
                <br>
                <input class="submit-button" type="submit" value="Ask">
            </form>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT as an environment variable
    app.run(host='0.0.0.0', port=port)