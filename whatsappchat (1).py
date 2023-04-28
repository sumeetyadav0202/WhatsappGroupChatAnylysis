# -*- coding: utf-8 -*-
"""whatsAppChat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LEp5Tmw-vNOUrOvmbvWaspMSuiC5FrP1
"""

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
!pip install emoji
import emoji

from google.colab import drive

drive.mount('/content/gdrive')

#Load the text file into a Pandas DataFrame
with open('/content/gdrive/MyDrive/whatsappChatAnylysis/WhatsApp Chat with Communic Module Sept22😎 (2).txt', 'r', encoding='utf8') as file:
    data = file.readlines()

dataset = data[1:]
cleaned_data = []
for line in dataset:
    # Check, whether it is a new line or not
    # If the following characters are in the line -> assumption it is NOT a new line
    if '/' in line and ':' in line and ',' in line and '-' in line:
        # grab the info and cut it out
        date = line.split(",")[0]
        line2 = line[len(date):]
        time = line2.split("-")[0][2:]
        line3 = line2[len(time):]
        name = line3.split(":")[0][4:]
        line4 = line3[len(name):]
        message = line4[6:-1] # strip newline charactor
        cleaned_data.append([date, time, name, message])

    # else, assumption -> new line. Append new line to previous 'message'
    else:
        new = cleaned_data[-1][-1] + " " + line
        cleaned_data[-1][-1] = new

# Create the DataFrame
df = pd.DataFrame(cleaned_data, columns = ['Date', 'Time', 'Name', 'Message'])
# Define words to be deleted from 'Message' column
delete_words = ['media', 'omitted', 'message', 'deleted']

# Replace words with empty string in 'Message' column
for word in delete_words:
    df['Message'] = df['Message'].str.replace(word, '')

# Print updated DataFrame
print(df)

df

"""## 1.Top 5 active members of this group:"""

import matplotlib.pyplot as plt

# Count the number of messages sent by each person and return the top 5 active members
active_members = df['Name'].value_counts().nlargest(5)

# Define a list of colors for the bars
colors = ['red', 'blue', 'green', 'orange', 'purple']

# Create a bar plot of the top 5 active members based on the number of messages they sent
plt.bar(active_members.index, active_members.values, color=colors)
plt.xlabel('Name')
plt.ylabel('Number of Messages')
plt.title('Top 5 Active Members')
plt.xticks(rotation=45) # rotate x-axis labels by 45 degrees
plt.show()

"""## 2.Top 5 emojis used:"""

import emoji
from collections import Counter
# Define a function to count the emojis in a given message
def count_emojis(text):
    return len([char for char in text if char in emoji.EMOJI_DATA])

# Create a Counter object to count the total number of each emoji in the dataframe
emoji_counter = Counter()
for message in df["Message"]:
    emoji_counter.update([char for char in message if char in emoji.EMOJI_DATA])

# Get the top 5 emojis and their counts
top_emoji = emoji_counter.most_common(10)

# Print the total number of emojis in the dataframe
#print("Total Emojis:", sum(emoji_counter.values()))

# Print the dataframe with the emoji count for each message
# df["Emoji Count"] = df["Message"].apply(count_emojis)
# print(df[["Date", "Time", "Name", "Message", "Emoji Count"]])

# Print the top 5 emojis and their counts
print("Top 10 Emojis:")
for emoji, count in top_emoji:
    print(f"{emoji}: {count}")

"""##3.top five person who have send most emojis"""

import emoji

# Create a dictionary to store the count of emojis for each person
person_emoji_count = {}

# Loop through the messages and update the emoji count for each person
for index, row in df.iterrows():
    person = row["Name"]
    emojis = [char for char in row["Message"] if emoji.is_emoji(char)]
    if person in person_emoji_count:
        person_emoji_count[person] += len(emojis)
    else:
        person_emoji_count[person] = len(emojis)

# Sort the dictionary by the count of emojis in descending order and print the top 5 persons
top_persons = sorted(person_emoji_count.items(), key=lambda x: x[1], reverse=True)[:8]
print("Top 5 persons who sent the most emojis:")
for person, count in top_persons:
    print(f"{person}: {count}")

# Define a list of colors for the bars
# colors = ['red', 'blue', 'green', 'orange', 'purple','grey',]

# Create a bar plot of the top 5 persons based on the count of emojis they sent
plt.bar([x[0] for x in top_persons], [x[1] for x in top_persons])
plt.xlabel('Person')
plt.ylabel('Number of Emojis')
plt.title('Top 5 Persons by Emoji Count')
plt.xticks(rotation=45) # rotate x-axis labels by 45 degrees
plt.show()

"""## 4.Top 10 days on which the group was most active:"""

# # Convert the 'Date' column to datetime format
# df['Date'] = pd.to_datetime(df['Date'])

# Group the DataFrame by 'Date' and count the number of messages
msg_count = df.groupby('Date')['Message'].count()

# Find the top 5 days based on the message count
top_10 = msg_count.nlargest(10)

# Print the result
# print(top_5)

# Create a bar plot of the top 10 days based on the message count
plt.bar(top_10.index, top_10.values, width=0.6)
plt.xlabel('Date')
plt.ylabel('Number of Messages')
plt.title('Top 10 Days by Message Count')
plt.xticks(rotation=45) # rotate x-axis labels by 45 degrees
plt.show()

"""## Word frequency anylysis"""

all_messages = " ".join(df['Message'])
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
all_messages = re.sub(r'[^a-zA-Z0-9\s]', '', all_messages.lower())
from nltk.tokenize import word_tokenize
tokens = word_tokenize(all_messages)
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if not word in stop_words]
from collections import Counter
word_freq = Counter(filtered_tokens)
freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])
freq_df.index.name = 'Word'
freq_df.reset_index(inplace=True)
freq_df = freq_df.sort_values('Frequency', ascending=False)
# print(freq_df.iloc[1:21])
# Calculate the total number of words
total_words = sum(freq_df['Frequency'])

# Calculate the percentage of total words accounted for by each of the top 20 words
top_words = freq_df.iloc[1:21]
top_words['Percentage'] = top_words['Frequency'] / total_words * 100

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(top_words['Percentage'], labels=top_words['Word'], autopct='%1.1f%%')
plt.title('Top 20 Words by Percentage of Total Words')
plt.show()

"""## Topic Modeling"""

import gensim
from gensim import corpora

# tokenize messages
messages = [msg.lower().split() for msg in df['Message']]

# create a dictionary
dictionary = corpora.Dictionary(messages)

# create a corpus
corpus = [dictionary.doc2bow(msg) for msg in messages]

# perform LDA topic modeling
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=10,
                                           random_state=42,
                                           passes=10,
                                           per_word_topics=True)

# print the topics
for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))



from textblob import TextBlob
import re

# Open the WhatsApp chat log file
with open("/content/gdrive/MyDrive/whatsappChatAnylysis/WhatsApp Chat with Communic Module Sept22😎 (2).txt", "r", encoding="utf-8") as f:
    chatlog = f.read()

# Split the chat log into individual messages
messages = re.findall(r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [AP]M) - (.*?): (.*)", chatlog)

# Iterate over each message in the chat log
for timestamp, sender, message in messages:
    # Create a TextBlob object for the message
    blob = TextBlob(message)
    
    # Iterate over each sentence in the message
    for sentence in blob.sentences:
        # Calculate the polarity and subjectivity of the sentence
        polarity, subjectivity = sentence.sentiment
        
        # If the sentence is sufficiently negative and subjective, flag it as potential plagiarism
        if polarity < -0.5 and subjectivity > 0.5:
            print(f"Potential plagiarism detected: {sentence} (sent by {sender} on {timestamp})")
        else:
          print("no plagiarism detected")