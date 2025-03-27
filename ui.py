from flask import Flask, request, render_template_string
from rag_mistral import RAGSystem
import os

app = Flask(__name__)

rag_system = RAGSystem()

# List of your book image filenames
BOOK_IMAGES = [
    "book1.jpg", "book2.jpg", "book3.jpg", "book4.jpg",
    "book5.jpg", "book6.jpg", "book7.jpg", "book8.jpg"
]

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
                <title>How can I help you organize your grocery list ? </title>
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
                    .books-grid {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 20px;
                        margin-top: 40px;
                        width: 80%;
                        margin-left: auto;
                        margin-right: auto;
                    }
                    .book-image {
                        width: 100%;
                        height: auto;
                        border-radius: 5px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }
                    .books-header {
                        margin-top: 40px;
                        text-align: center;
                        width: 80%;
                        margin-left: auto;
                        margin-right: auto;
                    }
                </style>
            </head>
            <body>
                <h1>How can I help you organize your grocery list ? </h1>
                <form method="post">
                    <textarea class="question-input" name="question" placeholder="Enter your question here..."></textarea>
                    <br>
                    <input class="submit-button" type="submit" value="Ask">
                </form>
                <h2>Answer:</h2>
                <p>{{ answer }}</p>
                
                <div class="books-header">
                    <h2>I know recipes from these books:</h2>
                </div>
                <div class="books-grid">
                    {% for image in book_images %}
                        <div class="book-item">
                            <img src="{{ url_for('static', filename=image) }}" alt="{{ image }}" class="book-image">
                        </div>
                    {% endfor %}
                </div>
            </body>
            </html>
        ''', answer=answer, book_images=BOOK_IMAGES)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>How can I help you organize your grocery list ? </title>
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
                .books-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-top: 40px;
                    width: 80%;
                    margin-left: auto;
                    margin-right: auto;
                }
                .book-image {
                    width: 100%;
                    height: auto;
                    border-radius: 5px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                .books-header {
                    margin-top: 40px;
                    text-align: center;
                    width: 80%;
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>
        </head>
        <body>
            <h1>How can I help you organize your grocery list ? </h1>
            <form method="post">
                <textarea class="question-input" name="question" placeholder="Enter your question here..."></textarea>
                <br>
                <input class="submit-button" type="submit" value="Ask">
            </form>
            
            <div class="books-header">
                <h2>I know recipes from these books:</h2>
            </div>
            <div class="books-grid">
                {% for image in book_images %}
                    <div class="book-item">
                        <img src="{{ url_for('static', filename=image) }}" alt="{{ image }}" class="book-image">
                    </div>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', book_images=BOOK_IMAGES)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT as an environment variable
    app.run(host='0.0.0.0', port=port)