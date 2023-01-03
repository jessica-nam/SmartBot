##### Using Flask to bring Stacky from the terminal to a locally hosted website #####
### NOTE: Due to the Flask application aspect not being essential to Stacky's functionality, 
###       app.py does not have a unittest because of the complications that arise when testing functions that need an active HTTP request   
from flask import Flask, render_template, jsonify, request
import processor


app = Flask(__name__)

app.config['SECRET_KEY'] = 'i2LovVoll'


@app.route('/', methods=["GET", "POST"])
def index():
    """ The index function is run whenever there is a request """
    return render_template('index.html', **locals())


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    """ Generate chatbot response using processor.py """
    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)

    return jsonify({"response": response })


if __name__ == '__main__':

    ### Flask app will run on port 8000
    app.run(host='0.0.0.0', port='8000', debug=True)