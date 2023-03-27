import json
import pandas as pd
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

with open('data.json', 'r') as f:
    data = json.load(f)

# -------------------------------------------------

# Count the number of reviews per company


def countReviews():
    for company in data:
        name = company["Name"]

        count = 0
        for review in company["Reviews"]:
            count += 1

        print("%s : %s" % (name, count))

# ---------------------------------------------------


def dataClean(company_name):
    new_data = []
    for company in data:
        name = company["Name"]
        if (name == company_name):
            for review in company["Reviews"]:
                star_rating = review["Star_Rating"]
                if (float(star_rating) < 3):
                    sentiment = "bad"
                elif (float(star_rating) == 3):
                    sentiment = "neutral"
                elif (float(star_rating) > 3):
                    sentiment = "good"
                culture = ""
                if ("culture" in review["Pros"]):
                    culture = "good_culture"
                elif ("culture" in review["Cons"]):
                    culture = "bad_culture"
                elif ("culture" in review["Pros"] and "culture" in review["Cons"]):
                    culture = "mixed_culture"
                tokens = word_tokenize(review["Pros"])
                stop_words = set(stopwords.words('english'))
                filtered_tokens = [
                    word for word in tokens if word.lower() not in stop_words]
                filtered_text = ' '.join(filtered_tokens)
                filtered_text = re.sub(r'[^\w\s]', '', filtered_text)

                new_data.append({
                    "Name": name,
                    "Star Rating": star_rating,
                    "Sentiment": sentiment,
                    "Culture": culture,
                    "Filtered Pros": filtered_text
                })
    df = pd.DataFrame(new_data)
    df.to_csv(company_name + ".csv", index=False)


dataClean("NCS")
dataClean("IBM")
dataClean("Microsoft")
dataClean("ByteDance")
dataClean("SAP")
