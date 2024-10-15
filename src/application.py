from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
import pickle



###### model loading #####
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid: 
    loaded_model = pickle.load(fid)

vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)
######################
# how to use model to predict
prediction = loaded_model.predict(vectorizer.transform(['This is fake news']))[0]

# output will be 'FAKE' if fake, 'REAL' if real|

# if __name__ == '__main__':
#     application.run()