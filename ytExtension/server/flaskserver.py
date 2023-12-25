

#$env:FLASK_APP="flaskserver.py"

import json
from tokenize import String
from urllib import response
from flask import Flask, request, jsonify
import json
import pandas as pd 
import time
import re
import os
import googleapiclient.discovery
from textblob.blob import TextBlob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction import text 
from wordcloud import WordCloud
import numpy as np
# import util


def remove_comments(df):
  # Checks for comments which has zero length in a dataframe
  zero_length_comments = df[df["Comments"].map(len) == 0]
  # taking all the indexes of the filtered comments in a list
  zero_length_comments_index = [ind for ind in zero_length_comments.index]
  # removing those rows from dataframe whose indexes matches 
  df.drop(zero_length_comments_index, inplace = True)
  return df

def find_subjectivity_on_single_comment(text):
  return TextBlob(text).sentiment.subjectivity
   
def apply_subjectivity_on_all_comments(df):
  df['Subjectivity'] = df['Comments'].apply(find_subjectivity_on_single_comment)
  return df 

def find_polarity_of_single_comment(text):
   return  TextBlob(text).sentiment.polarity

def find_polarity_of_every_comment(df):  
  df['Polarity'] = df['Comments'].apply(find_polarity_of_single_comment)
  return df 

analysis = lambda polarity: 'Positive' if polarity > 0 else 'Neutral' if polarity == 0 else 'Negative' 

def analysis_based_on_polarity(df):
  df['Analysis'] = df['Polarity'].apply(analysis)
  return df

def generate_word_clouds(df,id):
  allWords = ' '.join([twts for twts in df['Comments']])
  wordCloud = WordCloud(stopwords = text.ENGLISH_STOP_WORDS ,width=1000, height=600, random_state=21, max_font_size=110).generate(allWords)
  plt.axis('off')
  plt.imshow(wordCloud, interpolation="bilinear")
  # plt.savefig('C:\Users\hp\Desktop\ytExtension\server\wordcl")
  # plt.figure(figsize=(0.2,0,3))
  plt.savefig("wordclouds/"+id+".png",)
  plt.clf()

def help(id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAZA6Yk6L_K1hrS9MhN2BC4AbAA-iPSz4k"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
#         pageToken='QURTSl9pMnpaVEcyM0t0bzZPbjZkQl9ZYlFPN1VROERUTkpGNnY2ZUdQY2xzSXlwNTdrTDJKcVZsVVRnUWdpQVotcmZWWWFwNUs2cXJNSWNtRzFnc0RNa2JsQVoyTkozZWw2MWRPVXhncW5LdzNVLUVyOU9FRm8zS3pXeVFHM3ZqWmxLZzE2YjAtSUNHNjFTNVMtZHp6SDRUdjlteUljSzBXeXhqOXVDZ1JZaExINm5YQ3Q0TUU4aVRTRm12Q2RPQlNTQ2lNVVhuZ2ZHeDRjbmxLNm5FNHpSZU92UUVDSXZ3UDVqNlNjOE5JQmZLUmxxTUlJTExOMm1Bd0JOWmdaWHo3eE43TnR1Y0Z4T1lJaHppeTNsRktpZHdiRzE0MW5JVXV1aWxpa2J6R25ldjBWcmtVWmxONV8xRjd4SU5DWTA1S0NRVHFkcGppeHpfUmJ1QWlUeG1sRkFPNWt3ZnF3d1IwbEtGa2dWVTBwTmxHN0xLSlBiMVBEbmhZRkN3OG5IUVlORXMxZmpjRFAyYjN1SEdPM2ZGbEpJQ0pwamprWnl5NUY2dmNCRktMRV8wNmlVX05ncGJBRTl4WkxLTUxtNFFzcll2UQ==',
        order="relevance",
        videoId= id
    )
    response = request.execute()
    return response

def cleaning_comments(comment):
  comment = re.sub("[🤣|🤭|🤣|😁|🤭|❤️|👍|🏴|😣|😠|💪|🙏|🧐|😂|😄]+",'',comment)
  comment = re.sub("[0-9]+","",comment)
  comment = re.sub("[\:|\@|\)|\*|\.|\$|\!|\?|\,|\%|\"]+"," ",comment)
  comment = re.sub("[💁|🌾|😎|♥|🤷‍♂]+","",comment)
  comment = re.sub("[\(|\-|\”|\“|\#|\!|\/|\«|\»|\&]+","",comment)
  comment = re.sub("\n"," ",comment)
  comment = re.sub('[\'|🇵🇰|\;|\！]+','',comment)
  return comment




def mainfunction(id):


    response=help(id)
    authorname = []
    comments = []
    for i in range(len(response["items"])):
        authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
        comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
    df = pd.DataFrame(comments,columns=["Comments"])
    temp=""
    if "nextPageToken" in response.keys():
         temp=response["nextPageToken"]
    while temp :
    
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAZA6Yk6L_K1hrS9MhN2BC4AbAA-iPSz4k"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="id,snippet",
            maxResults=200,
            pageToken=temp,
            order="relevance",
            videoId= id
        )
        response = request.execute()
        if "nextPageToken" in response.keys():
            temp=response["nextPageToken"]
        else:
            temp=""
        authorname = []
        comments = []
        for i in range(len(response["items"])):
            authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
            comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        df_2 = pd.DataFrame(comments,columns=["Comments"])
        
        df=df.append(df_2,ignore_index = True)
        time.sleep(0.1)

    df["Comments"]= df["Comments"].apply(cleaning_comments)
    lower = lambda comment: comment.lower()
    df['Comments'] = df['Comments'].apply(lower)
    df = remove_comments(df)
    df = apply_subjectivity_on_all_comments(df)
    df = find_polarity_of_every_comment(df)
    df = analysis_based_on_polarity(df)
    generate_word_clouds(df,id)

    neutral,positive,negative=df["Analysis"].value_counts()
    y = np.array([neutral,positive,negative])
    labels=['Neutral','Positive','Negative']

    plt.pie(y,labels=labels,wedgeprops={'edgecolor':'black'},autopct='%1.1f%%')
    # plt.figure(figsize=(0.2,0,3))
    plt.savefig("piecharts/"+id+".png")
    plt.clf()
    # img1 = image.open("piecharts/"+id+".png")
    # img1.resize((160, 240), image.ANTIALIAS)
    # img2 = image.open("wordclouds/"+id+".png")
    # img2.resize((160, 240), image.ANTIALIAS)

    return jsonify(neutral=neutral,positive=positive,negative=negative)




app = Flask(__name__)
app.debug=True

@app.route('/test', methods=['GET'])
def test():
    a=request.args.get('url')
    return mainfunction(a)
    

if __name__ == "__main__":
    # print("Starting Python Flask Server For Home Price Prediction...")
    # util.load_saved_artifacts()``
    app.run(debug=True)