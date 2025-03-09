from flask import Flask, request, render_template_string
from rag_mistral import RAGSystem

app = Flask(__name__)

rag_system = RAGSystem()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        answer = rag_system.ask_question(question)
        return render_template_string('''
            <h1>Ask a Question</h1>
            <form method="post">
                <input type="text" name="question">
                <input type="submit" value="Ask">
            </form>
            <h2>Answer:</h2>
            <p>{{ answer }}</p>
        ''', answer=answer)
    return render_template_string('''
        <h1>Ask a Question</h1>
        <form method="post">
            <input type="text" name="question">
            <input type="submit" value="Ask">
        </form>
    ''')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT as an environment variable
    app.run(host='0.0.0.0', port=port)