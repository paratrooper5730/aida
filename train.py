"""
Training
"""
import numpy as np
import pandas as pd
import configparser
import pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

config = configparser.ConfigParser()
config.read('config.ini')

def my_split(features, labels):
    features_train = features[:-100]
    labels_train = labels[:-100]
    features_test = features[-100:]
    labels_test = labels[-100:]
    return features_train, features_test, labels_train, labels_test



if __name__ == "__main__":
    df = pd.read_csv(config['DATA']['labeled_data_file'], sep=';', index_col=False)
    print(df.shape)
    df.fillna(0, inplace=True)
    answered = np.asarray(df.Answered)
    uids = np.asarray(df.UID)
    df.drop('Answered', axis=1, inplace=True)
    df_features = df.to_dict(orient='records')
    vec = DictVectorizer()
    features = vec.fit_transform(df_features).toarray()
    pickle.dump(vec, open("vectorizer.p", "wb"))
    print("after vectorization: ", features.shape)
    features_train, features_test, labels_train, labels_test = my_split(features, answered)

    clf = RandomForestClassifier()
    clf.fit(features_train, labels_train)
    pickle.dump(clf, open("model.p", "wb"))

# compute accuracy using test data
    acc_test = clf.score(features_test, labels_test)
    print("Test Accuracy:", acc_test)

#look what it actually predicts
    predictions = clf.predict_proba(features_test)
    #np.append(predictions, labels_test)
    #print(predictions.shape)
    labels_test = labels_test[:, None]
    #print(labels_test.shape)
    test_estimations_with_answers = np.hstack((predictions, labels_test))
    print(test_estimations_with_answers)
