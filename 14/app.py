from functools import lru_cache
from pathlib import Path
import joblib
from flask import Flask,render_template,request
from clean import clean_review

app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=128*1024
@lru_cache(maxsize=1)
def model():
    return joblib.load(Path(__file__).with_name("sentiment.joblib"))

@app.route("/",methods=["GET","POST"])
@app.post("/predict")
def home():
    text=request.form.get("review","")
    result=None
    if request.method=="POST":
        cleaned=clean_review(text)
        if not cleaned:
            return render_template("index.html",text=text,error="Введіть текст відгуку."),400
        try:
            prediction=model().predict([cleaned])[0]
        except FileNotFoundError:
            return render_template("index.html",text=text,error="Спочатку навчіть модель командою з README."),503
        result={"positive":"Позитивний","negative":"Негативний"}[prediction]
    return render_template("index.html",text=text,result=result)
