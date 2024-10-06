from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <html>
            <body>
                <h1>Welcome to LUTFoodVoting</h1>
                <img src="/picture" alt="Food Picture">
            </body>
        </html>
    '''

@app.route('/picture')
def picture():
    return send_file('C:\Users\fb200\OneDrive\Uni Koblenz\Hackathon\LUTFoodVoting\pictures\Screenshot 2024-10-05 121135.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)