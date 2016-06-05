import tweepy
import couchdb
import json
from textblob import TextBlob
import threading
from datetime import datetime

#This class is used to make authorization through access token, access token secret, consumer key and consumer secret from Twitter to have right to send requests
class clientKeys:
	def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret,clientId):
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.clientId = clientId

	def OAuth(self):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		#Set the value of "wait on rate limit" to True so that when rate limit is reached, then a token will wait for 15 min to continue to make requests
		api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		return api

#This class is used to provide functions for saving tweets, adding new fields to a tweet.
class functions:
#This function is used to save tweets in a database
	def save_tweets(self,json_str,db,kind):
		#To avoid duplication, change the document ID to tweet ID
		json_str['_id'] = json_str['id_str']
		try: 
			db.save(json_str)
		except Exception,e:
			#If a duplicated tweet exists, then handle this tweet in following two different ways.
			if kind == "followerTimeline":
				return "break"
			else: 
				return "continue"

#This function is used to add a time field with value "before" or "after" for a tweet
	def setTime(self,tweet, date):
		monthDic = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
		time = tweet['created_at']
		wordList = time.split( )
		month = monthDic.get(wordList[1])
		day = int(wordList[2])
		year = int(wordList[5])
		if datetime(year,month,day) > date:
			tweet['timeTag'] = 'after'
		else: tweet['timeTag'] = 'before'
		return tweet
#This function is used to add a sentiment field with score of polarity and subjectivity for a tweet
	def sentiment(self,tweet):
		text = tweet['text']
		testimonial = TextBlob(text)
		polarityValue = testimonial.sentiment.polarity
		subjectivityValue = testimonial.sentiment.subjectivity
		tweet['polarity'] = polarityValue
		tweet['subjectivity'] = subjectivityValue
		return tweet

#This class is used to retrieve tweets that a specific user posted
class getUserTimeline(threading.Thread):
	def __init__(self,db,api,listOfCompany,typeIn):
		threading.Thread.__init__(self)
		self.db = db
		self.api = api
		self.listOfCompany = listOfCompany
		self.type = typeIn
	def run(self):
		f = functions()
		#a user is one of the companies
		if self.type == "screenName":
			for each in self.listOfCompany:
				companyName = each[0]
				Cyear = int(each[1].split( )[0])
				Cmonth = int(each[1].split( )[1])
				Cday = int(each[1].split( )[2])
				#get the date of joinging B Corp for a company
				date = datetime(Cyear,Cmonth,Cday)
				try:
					#This function is used to retrieve tweets via user timeline
					tweets = tweepy.Cursor(self.api.user_timeline, screen_name = companyName,lang='en').items()
					#process retrieved tweets
					for tweet in tweets:
						json_str = json.loads(json.dumps(tweet._json))
						json_str['company'] = companyName
						json_str = f.setTime(json_str,date)
						didSentimentTweet = f.sentiment(json_str)
						#save the tweet in database
						f.save_tweets(didSentimentTweet,self.db,"companyTimeline")
				except tweepy.TweepError as e:
					print("company user timeline error : " + str(e))
					continue
			print "company user timeline over"
		#a user is one of the followers
		else:
			for each in self.listOfCompany:
				companyInfo = each[0]
				followerIds = each[1:len(each)]
				companyName = companyInfo[0]
				Cyear = int(companyInfo[1].split( )[0])
				Cmonth = int(companyInfo[1].split( )[1])
				Cday = int(companyInfo[1].split( )[2])
				#get the date of joinging B Corp for a company
				date = datetime(Cyear,Cmonth,Cday)
				accountName = companyInfo[2]
				#Retrieve tweets posted by each of followers
				for followerId in followerIds:
					try:
						tweets = tweepy.Cursor(self.api.user_timeline, user_id = followerId,lang='en').items()
						#process retrieved tweets
						for tweet in tweets:
							json_str = json.loads(json.dumps(tweet._json))
							text = json_str['text']
							#If the content of a tweet contains relevant information about the company, then process it and save it
							if companyName.lower() in text.lower() or accountName.lower() in text.lower():
								json_str['company'] = companyName
								json_str = f.setTime(json_str,date)
								didSentimentTweet = f.sentiment(json_str)
								#save the tweet in database
								saveType = f.save_tweets(didSentimentTweet,self.db,"followerTimeline")
								#stop retrieving tweets from this user
								if saveType == "break":
									break
					except tweepy.TweepError as e:
						print("followers user timeline error : " + str(e))
						continue

#This class is used to search relevant tweets for all companies from Twitter
class search(threading.Thread):
	def __init__(self,db,api,listOfCompany):
		threading.Thread.__init__(self)
		self.db = db
		self.api = api
		self.listOfCompany = listOfCompany
 	def run(self):
 		f = functions()
		for each in self.listOfCompany:
			Cyear = int(each[1].split( )[0])
			Cmonth = int(each[1].split( )[1])
			Cday = int(each[1].split( )[2])
			#get the date of joinging B Corp for a company
			date = datetime(Cyear,Cmonth,Cday)
			companyName = each[0]
			accountName = each[2]
			try:
				#send requests to Twitter
				tweets = tweepy.Cursor(self.api.search,q=companyName + ' OR ' + accountName,lang='en',result_type='recent',until='2016-04-25').items()
				#process retrieved tweets
				for tweet in tweets:
					json_str = json.loads(json.dumps(tweet._json))
					if companyName.lower() in json_str['text'].lower() or accountName.lower() in json_str['text'].lower():
						json_str['company'] = companyName
						json_str = f.setTime(json_str,date)
						didSentimentTweet = f.sentiment(json_str)
						#save the tweet in database
						f.save_tweets(didSentimentTweet,self.db,"search")
			except tweepy.TweepError as e:
				print("search error : " + str(e))


