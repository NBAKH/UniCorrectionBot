#!/usr/bin/python
# -*- coding: UTF-8 -*-
from twython import Twython
import time
import re
twitter = Twython()

APP_KEY = "APP_KEY"
APP_SECRET = "APP_SECRET"
OAUTH_TOKEN = "OAUTH_TOKEN"
OAUTH_TOKEN_SECRET = "OAUTH_TOKEN_SECRET"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

banned_words = ["elev", "elever", "eleven", "eleverne", "skole", "skoler", "skolen", "skolerne", "lærer", "lærere", "læreren", "lærerene"]
approved_words = ["studerende","studerende", "den studerende", "de studerende", "universitet", "universiteter", "universitetet", "universiteterne", "underviser", "undervisere", "underviseren", "underviserne"]
hashtags = ["#austudieliv", "#aarhusuni", "#yourniversity", "#youruniversity", "#aarhusuniversity", "#Koefoed_BOT", "#KoefoedBot"]
cache = []

def my_timeline():
    print('Fetching timeline')
    my_timeline = twitter.get_home_timeline()
    print('######This is my timeline######')
    for tweet in my_timeline:
        print(tweet['text'])

def get_other_timeline(user_name):
    try:
        user_timeline = twitter.get_user_timeline(screen_name= user_name)
        print("######This Lone's timeline######")
        for tweet in user_timeline:
            print(tweet['text'])
    except TwythonError as e:
        print(e)

def startup():
    print('Starting Koefoed_BOT')
    print('_______________________________\n\n')
    try:
        for tags in hashtags:
            search = twitter.search(q=tags ,count=5)   #**supply whatever query you want here**
            tweets = search['statuses']
            print('######This is the hashtag stream######')
            for tweet in tweets:
                print(tweet['id_str'], '\n', tweet['text'], '\n\n\n')
                tweet_text = tweet['text']
                isMatch = any(string in tweet_text for string in banned_words)
                if tweet['id_str'] not in cache and isMatch:
                    cache.append(tweet['id_str'])
                    print("Added to cache",'\n')
                else:
                    print("already in cache")
            print('_______________________________')
            for ids in cache:
                print(ids)
    except Exception as e:
        print(e)

def search_for_hash():
    print('Fetching hashtags')
    try:
        for tags in hashtags:
            search = twitter.search(q=tags ,count=5)   #**supply whatever query you want here**
            tweets = search['statuses']
            print('######Searching for matches in '+tags+"######")
            for tweet in tweets:
                answer_generate01 = []
                answer_generate02 = []
                tweet_text = tweet['text'].lower()
                #searching tweet text
                for index in range(len(banned_words)):
                    #print(banned_words[index])
                    #if(banned_words[index] in sentence):
                    if tweet['id_str'] not in cache:
                        if re.search(r'\b'+banned_words[index]+r'\b', tweet_text):
                            print(tweet['id_str'], '\n', tweet['text'], '\n')
                            print("det virker")
                            answer_generate01.append(approved_words[index])
                            answer_generate02.append(banned_words[index])
                if tweet['id_str'] not in cache:
                        cache.append(tweet['id_str'])
                #what to print
                name = tweet["user"]["screen_name"]
                #twitter.update_status(status="@%s Ups, du skrev elev, skole eller lærer. Mente du studerende, universitet eller underviser?" %(name,), in_reply_to_status_id=tweet['id_str'])
                for index in range(len(answer_generate01)):
                    print(index)
                if(len(answer_generate01)==0):
                    d=1
                    #print("Nothing to comment on")
                elif(len(answer_generate01)==1):
                    twitter.update_status(status="Hov @%s, du skrev %s, mente du %s?" %(name, answer_generate02[0], answer_generate01[0]), in_reply_to_status_id=tweet['id_str'])
                    #print("Hov @%s, du skrev %s, mente du %s?" %(name, answer_generate02[0], answer_generate01[0]))
                elif(len(answer_generate01)==2):
                    twitter.update_status(status="Hov @%s, du skrev %s og %s, mente du %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate01[0], answer_generate01[1]), in_reply_to_status_id=tweet['id_str'])
                    #print("Hov @%s, du skrev %s og %s, mente du %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate01[0], answer_generate01[1])
                elif(len(answer_generate01)==3):
                    twitter.update_status(status="Hov @%s, du skrev %s, %s og %s mente du %s, %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate02[2], answer_generate01[0], answer_generate01[1], answer_generate01[2]), in_reply_to_status_id=tweet['id_str'])
                    #print("Hov @%s, du skrev %s, %s og %s mente du %s, %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate02[2], answer_generate01[0], answer_generate01[1], answer_generate01[2]))
                elif(len(answer_generate01)==4):
                    twitter.update_status(status="Hov @%s, du skrev %s, %s, %s og %s, mente du %s, %s, %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate02[2], answer_generate02[3], answer_generate01[0], answer_generate01[1], answer_generate01[2], answer_generate01[3]), in_reply_to_status_id=tweet['id_str'])
                    print("Hov @%s, du skrev %s, %s, %s og %s, mente du %s, %s, %s og %s?" %(name, answer_generate02[0], answer_generate02[1], answer_generate02[2], answer_generate02[3], answer_generate01[0], answer_generate01[1], answer_generate01[2], answer_generate01[3]))
                elif(len(answer_generate01)>=5):
                    twitter.update_status(status="%s, husk at man er studerende, når man går universitet" %(name), in_reply_to_status_id=tweet['id_str'])
            print('#################################################')
    except TwythonError as e:
        print(e)

def library_for_old_tweets(input_file):
    document = open('old_tweets.txt', 'r')
    print("Successfully opened")
    check_value = True
    for line in document:
        print(line)
        id_string = str(line)
        isMatch = any(string in id_string for string in str(input_file))
        print(isMatch)
        if isMatch == True:
            check_value = False
    document.close()
    if check_value == True:
        with open('old_tweets.txt', 'a') as write_doc:
            write_doc.write(str(input_file) + "\n")
            print("this is a new tweet")
            return False
    else:
        return True

startup()
while True:
    search_for_hash()
    print("Going to sleep")
    time.sleep(60)

