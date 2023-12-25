
import pandas as pd 
import re
import os
import googleapiclient.discovery

# getting all the comments 

def help(id):
    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAZA6Yk6L_K1hrS9MhN2BC4AbAA-iPSz4k"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        order="relevance",
        videoId= id
    )
    response = request.execute()
    return response

response=help("ihz5F7eMSpw")

# Storing data in data_frame

def create_df_author_comments():
  authorname = []
  comments = []
  for i in range(len(response["items"])):
    authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
    comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
  df_1 = pd.DataFrame(comments, index = authorname,columns=["Comments"])
  return df_1 
df_1 = create_df_author_comments()
print(df_1)



# cleaning
def cleaning_comments(comment):
  comment = re.sub("[🤣|🤭|🤣|😁|🤭|❤️|👍|🏴|😣|😠|💪|🙏]+",'',comment)
  comment = re.sub("[0-9]+","",comment)
  comment = re.sub("[\:|\@|\)|\*|\.|\$|\!|\?|\,|\%|\"]+"," ",comment)
  comment = re.sub("[💁|🌾|😎|♥|🤷‍♂]+","",comment)
  comment = re.sub("[\(|\-|\”|\“|\#|\!|\/|\«|\»|\&]+","",comment)
  comment = re.sub("\n"," ",comment)
  comment = re.sub('[\'|🇵🇰|\;|\！]+','',comment)
  return comment


df_1["Comments"]= df_1["Comments"].apply(cleaning_comments)


# converting to lower case
lower = lambda comment: comment.lower()
df_1['Comments'] = df_1['Comments'].apply(lower)
print(df_1)
