import tweepy
import couchdb
import json
from textblob import TextBlob
import threading
from datetime import datetime

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
		api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		return api

class functions:

	def save_tweets(self,json_str,db,kind):
		json_str['_id'] = json_str['id_str']
		try: 
			db.save(json_str)
		except Exception,e:
			#print "dupicated save"
			if kind == "followerTimeline":
				return "break"
			else: 
				return "continue"


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

	def sentiment(self,tweet):
		text = tweet['text']
		testimonial = TextBlob(text)
		polarityValue = testimonial.sentiment.polarity
		subjectivityValue = testimonial.sentiment.subjectivity
		tweet['polarity'] = polarityValue
		tweet['subjectivity'] = subjectivityValue
		return tweet

	def getTweetsfromDB(self, attitude, company, timeTag):
		map_fun = '''function(doc) { 
			if (doc.sentiment == %s && doc.timeTag == %s && doc.company == %s)
				emit(doc.timeTag, null);}''' % (attitude, timeTag, company)
		FilterList = db.query(map_fun)
		return len(FilterList)

class getUserTimeline(threading.Thread):
	def __init__(self,db,api,listOfCompany,typeIn):
		threading.Thread.__init__(self)
		self.db = db
		self.api = api
		self.listOfCompany = listOfCompany
		self.type = typeIn
	def run(self):
		f = functions()
		if self.type == "screenName":
			for each in self.listOfCompany:
				companyName = each[0]
				Cyear = int(each[1].split( )[0])
				Cmonth = int(each[1].split( )[1])
				Cday = int(each[1].split( )[2])
				date = datetime(Cyear,Cmonth,Cday)
				try:
					tweets = tweepy.Cursor(self.api.user_timeline, screen_name = companyName,lang='en').items()
					for tweet in tweets:
						json_str = json.loads(json.dumps(tweet._json))
						json_str['company'] = companyName
						json_str = f.setTime(json_str,date)
						didSentimentTweet = f.sentiment(json_str)
						f.save_tweets(didSentimentTweet,self.db,"companyTimeline")
				except tweepy.TweepError as e:
					print("company user timeline error : " + str(e))
					continue
			print "company user timeline over"
		else:
			for each in self.listOfCompany:
				companyInfo = each[0]
				followerIds = each[1:len(each)]
				companyName = companyInfo[0]
				Cyear = int(companyInfo[1].split( )[0])
				Cmonth = int(companyInfo[1].split( )[1])
				Cday = int(companyInfo[1].split( )[2])
				date = datetime(Cyear,Cmonth,Cday)
				accountName = companyInfo[2]
				print "name: ",companyName
				for followerId in followerIds:
					try:
						print followerId
						tweets = tweepy.Cursor(self.api.user_timeline, user_id = followerId,lang='en').items()
						for tweet in tweets:
							json_str = json.loads(json.dumps(tweet._json))
							text = json_str['text']
							if companyName.lower() in text.lower() or accountName.lower() in text.lower():
								print "*********************************************"
								json_str['company'] = companyName
								json_str = f.setTime(json_str,date)
								didSentimentTweet = f.sentiment(json_str)
								saveType = f.save_tweets(didSentimentTweet,self.db,"followerTimeline")
								if saveType == "break":
									break
					except tweepy.TweepError as e:
						print("followers user timeline error : " + str(e))
						continue
			print "over"

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
			date = datetime(Cyear,Cmonth,Cday)
			companyName = each[0]
			accountName = each[2]
			print "search: ",companyName
			try:
				tweets = tweepy.Cursor(self.api.search,q=companyName + ' OR ' + accountName,lang='en',result_type='recent',until='2016-04-25').items()
				for tweet in tweets:
					json_str = json.loads(json.dumps(tweet._json))
					if companyName.lower() in json_str['text'].lower() or accountName.lower() in json_str['text'].lower():
						json_str['company'] = companyName
						json_str = f.setTime(json_str,date)
						didSentimentTweet = f.sentiment(json_str)
						f.save_tweets(didSentimentTweet,self.db,"search")
			except tweepy.TweepError as e:
				print("search error : " + str(e))


