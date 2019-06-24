#python3
#usage: 
# python3 categorize.py | sort -u | uniq

#https://medium.com/velotio-perspectives/real-time-text-classification-using-kafka-and-scikit-learn-c2875ad80b3c
#https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# classification and categorization
# from a txt file

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train')

text_clf = Pipeline([
     ('vect', CountVectorizer()),
     ('tfidf', TfidfTransformer()),
     ('clf', MultinomialNB()),
])


from sklearn.model_selection import GridSearchCV
parameters = {
     'vect__ngram_range': [(1, 1), (1, 2)],
     'tfidf__use_idf': (True, False),
     'clf__alpha': (1e-2, 1e-3),
}

gs_clf = GridSearchCV(text_clf, parameters, cv=5, iid=False, n_jobs=-1)

gs_clf = gs_clf.fit(twenty_train.data[:400], twenty_train.target[:400])


with open('cv.txt', 'r') as f:
    docs_new = f.readlines()

output1 = twenty_train.target_names[gs_clf.predict(docs_new)[0]]
output2 = twenty_train.target_names[gs_clf.predict(docs_new)[1]]
output3 = twenty_train.target_names[gs_clf.predict(docs_new)[2]]
#output4 = twenty_train.target_names[gs_clf.predict(docs_new)[3]]
#output5 = twenty_train.target_names[gs_clf.predict(docs_new)[4]]
#output6 = twenty_train.target_names[gs_clf.predict(docs_new)[5]]
#output7 = twenty_train.target_names[gs_clf.predict(docs_new)[6]]

print(">> [ "+output1 + " ]")
print(">> [ "+output2 + " ]")
print(">> [ "+output3 + " ]")
#print(">> [ "+output4 + " ]")
#print(">> [ "+output5 + " ]")
#print(">> [ "+output6 + " ]")
#print(">> [ "+output7 + " ]")

categoriesAll = output1 + "\n" + output2 + "\n" + output3

with open('coreCategory.txt', 'a') as the_file:
    the_file.write(str(categoriesAll))
