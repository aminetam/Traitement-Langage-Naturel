import re
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
#Scraping de notre data depuis pandas
df=pd.read_csv("C:/users/medam/Documents/manual_testing.csv")
df = df.drop(["title", "subject","date"], axis = 1)
df = df.sample(frac = 1)
df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)
#Enlever la ponctualisation de notre texte
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
df["text"] = df["text"].apply(wordopt)

x = df["text"]
y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
#Deviser notre texte en mot
vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)
#Classification de notre texte
#Logistic Regression Methode
LR = LogisticRegression()
LR.fit(xv_train,y_train)
pred_lr=LR.predict(xv_test)
LR.score(xv_test, y_test)
classification_report(y_test, pred_lr)
#Decision Tree Methode
DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)
pred_dt = DT.predict(xv_test)
DT.score(xv_test, y_test)
classification_report(y_test, pred_dt)


#Notre Output soit fake news ou good news
def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Good News"

#Fonction test prend comme parametre notre news
def manual_testing(news):
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    #Deviser notre texte en mot
    new_xv_test = vectorization.transform(new_x_test)
    #Classifier notre texte
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)


    return print("\n\nResultat With Logistic Regression Methode: {}\nResultat With Decision Tree Methode: {} ".format(
        output_lable(pred_LR[0]),output_lable(pred_DT[0])))




manual_testing("21st Century Wire says As 21WIRE reported earlier this week, the unlikely  mishap  of two US Naval vessels straying into Iranian waters "
               "  just hours before the President s State of the Union speech, followed by the usual parade of arch-neocons coming on TV in real time to "
               "declare the incident as  an act of aggression  by Iran against the United States   is no mere coincidence.24 hours after the incident, the"
               " Iranians returned all 11 US sailors, unharmed and in good spirits. The only remaining casualty from this event was an incident of a common "
               "condition in Washington known as  Pre-Traumatic Stress Disorder    suffered by a certain US Senator was mortified by the uneventful outcome"
               " which followed Daniel McAdams Ron Paul Institute  The two US Navy riverine command boats intercepted in Iranian territorial waters yesterday"
               " were sent on their way along with the crew of 10 US sailors after brief detention on Iranian soil.According to news reports, the well-armed "
               "warships either suffered mechanical or navigational difficulties which caused them to enter Iranian territory (although it may well have been "
               "a game of cat-and-mouse to test the Iranian response). The US sailors were apparently treated well, enjoyed what appeared a decent meal in "
               "relaxed surroundings, and in the end apologized for the mistake and praised their treatment by the Iranians. Thanks to President Obama s "
               "policy shift on Iran toward engagement and away from isolationism, Secretary of State John Kerry was able to telephone his Iranian counterpart"
               " Mohammad Zarif and quickly defuse what just months ago would have been a far more serious situation.This should be a good-news story about "
               "the value of diplomacy and reducing tensions with adversaries, but Sen. John McCain (R-AZ) was having none of it. That Kerry expressed his"
               " appreciation to the Iranians for swiftly releasing the American sailors only showed the Obama Administration s  craven desire to preserve "
               "the dangerous Iranian nuclear deal at all costs evidently knows no limit,  said McCain in a press release.McCain was furious that  Obama "
               "administration officials seem to be falling over themselves to offer praise for Iran s graciousness  and was outraged that the Iranians "
               "dared interfere with the actions of US military vessels operating in Iranian waters.In the world of John McCain, only the United States "
               "has the right to national sovereignty. The US military has the right to act anywhere and everywhere and the rest of the world dare not "
               "raise a question.According to McCain,  sovereign immune naval vessels are exempt from detention, boarding, or search. Their crews are not"
               " subject to detention or arrest. Imagine the tune McCain would have been singing if a well-armed Iranian naval vessel had been spotted "
               "in US territorial waters off the coast of New York. Would he have so rigorously condemned any US interference in the actions of Iran "
               "s sovereign naval vessels?Leave it to some clever Twitterers to post an example of the difference between US and Iranian detention.Copyright"
               "   2016 by RonPaul Institute. Permission to reprint in whole or in part is gladly granted, provided full credit and a live link are "
               "given.READ MORE JOHN MCCAIN NEWS AT: 21st Century Wire McPain Files")