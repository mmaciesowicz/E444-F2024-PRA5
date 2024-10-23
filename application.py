from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
import pickle
from flask import Flask, render_template, request

def load_model():
    ###### model loading #####
    loaded_model = None
    with open('basic_classifier.pkl', 'rb') as fid: 
        loaded_model = pickle.load(fid)

    vectorizer = None
    with open('count_vectorizer.pkl', 'rb') as vd:
        vectorizer = pickle.load(vd)
    return loaded_model, vectorizer


loaded_model, vectorizer = load_model()

application = Flask(__name__)
@application.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    
    if request.method == 'POST':
        # get sentence input from user
        sentence = request.form['sentence']
        
        # get prediction
        prediction = loaded_model.predict(vectorizer.transform([sentence]))[0]
        # output will be 'FAKE' if fake, 'REAL' if real

    return render_template('index.html', prediction=prediction)


if __name__ == "__main__":
    application.run()