"""Варіант 2. Тренування з IMDB Dataset.csv або ZIP з цим файлом."""
import argparse
from pathlib import Path
import re
import json
from html import unescape
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from clean import clean_review

def train(source,out):
    data=pd.read_csv(source,usecols=["review","sentiment"]).dropna()
    data["review"]=data.review.map(clean_review)
    data=data[data.review.ne("") & data.sentiment.isin(["positive","negative"])]
    # Прибрано дублікати до розбиття, а також тексти з суперечливими мітками.
    data=data.groupby("review").filter(lambda rows: rows.sentiment.nunique()==1).drop_duplicates("review")
    x_train,x_test,y_train,y_test=train_test_split(data.review,data.sentiment,test_size=0.20,
                                                  stratify=data.sentiment,random_state=42)
    pipe=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=70000,sublinear_tf=True)),
                   ("model",LogisticRegression(max_iter=500,random_state=42))])
    pipe.fit(x_train,y_train)
    pred=pipe.predict(x_test)
    labels=["negative","positive"]
    report={"train":len(x_train),"test":len(x_test),"labels":labels,
            "confusion_matrix":confusion_matrix(y_test,pred,labels=labels).tolist(),
            "metrics":classification_report(y_test,pred,output_dict=True)}
    out.mkdir(parents=True,exist_ok=True)
    joblib.dump(pipe,out/"sentiment.joblib",compress=3)
    (out/"metrics.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    print(classification_report(y_test,pred))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("dataset",type=Path)
    parser.add_argument("--out",type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    train(args.dataset,args.out)
