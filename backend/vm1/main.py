import threading
import couchdb
import testTweepy
import tweepy
import json
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import csv
import time
import os

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	def __init__(self,db,nameOfCompany):
		self.db = db
		self.nameOfCompany = nameOfCompany
#This method is called when a new tweet is found
	def on_data(self, tweet):
		f = testTweepy.functions()
		all_data = json.loads(tweet)
		text = all_data['text']
		for each in self.nameOfCompany:
			if each[0].lower() in text.lower() or each[1].lower() in text.lower():
				companyName = each[0]
				all_data['company'] = companyName
				all_data['timeTag'] = 'after'
				didSentimentTweet = f.sentiment(all_data)
				f.save_tweets(didSentimentTweet,self.db,"stream")
				return True
		

	def on_error(self, status):
		print status

def main():
#Create a database "tweets" in CouchDB, if it already exists, then get this database.
	couch = couchdb.Server()
	try:
		db = couch.create('tweets')
	except couchdb.http.PreconditionFailed as e:
		db = couch['tweets']
#Acquire authorization from Twiiter and create 6 tokens for querying through access tokens, access token secret, consumer key, consumer secret
	client1 = testTweepy.clientKeys("2723420030-Z0LJ1sfonzSQogAM25oKmozVnJBZwDoVDawC2gA","n2eyv44dYCgUX063M13VKqqWtNgAfYHl9W0g1lFBL0TAv","h6ULJQTi8lb7mlS8eY52OxCIs","0yKrZii3zQQETvgzL31ob53hLMdQAUGelYTKYvY5yq0JKIhy1R",1)
	api1 = client1.OAuth()

	client2 = testTweepy.clientKeys("2723420030-2lR2cPY92h8YWP9wjMPFCRfiWEVi35VMoi2NsT7","ZHMNdF5iHTKKMYZaArcOJWPKnFD8IxafPp1kZQ2XLJz47","RRUNpOEH6SoPP97l2YGHl0dQu","9IEq0XWSDJ1Pt9rnMEfeKilznSS4mayYoWM8djyzM9DLPjw7Rh",2)
	api2 = client2.OAuth()

	client3 = testTweepy.clientKeys("2723420030-78QBg5F4msLFiPPkSCNPLZB7453bmd9UL4eK0Le","i0joZvz2s0xXFcT0BM43s7FPABfqZY9mwM861Vw73zad6","By8V2Yj8I7QTlMtYlTrLKgk4B","tK3WyeSN8VQv7uTgHltA8m5yGhaFaUIM1LALXKj3Fil5iMjZ94",3)
	api3 = client3.OAuth()

	client4 = testTweepy.clientKeys("2723420030-hX3dtFJHtnj53kLOpTESpXzj4gyaoeXD2mX1EL8","qwiX45pLgjFcGEDmbJXWtbVxg2nBrT0OcVRBfEJcyjfCt","dNWIbuMo2OcDShfAAocfvvcv0","Nj2gssyqGXvilTFNvTNqOLiIvGKuL1oQc53RDSsb7zM5kRW947",4)
	api4 = client4.OAuth()

	client5 = testTweepy.clientKeys("2723420030-vMSM6RDSGBmotIjRA3lafZTit23pBleSuqRvGmA","X5jmlJs9jbFvgHegRU8pVPOJ4Ld4w4JLGz7pq5Guzg6MJ","HqsxFgMwds7tIiYN71VrPV7D8","m83kWRShTvOgCOSRpJaz7SE7fBv5XCaeo142p1w3aD14HKfpEy",5)
	api5 = client5.OAuth()

	client6 = testTweepy.clientKeys("2723420030-WFrcjeXsVIV1AHgWZ1YhTVb7RCxmftZQB8D8IOW","EvAUoawFAdVPEfTjiRZY7xxAuyqNuLv4WVI86Eh797HUK","8FWIMWkMWaLKtbSyUkDcsAO8Z","JTPVp6izcJ73PSL4fbTaVWSFGFiJM4m0TZj1J5gSKtiuL6vaCA",6)
	api6 = client6.OAuth()

	#read CSV File which contains information of all companies
	listOfCompany = []
	with open('smallData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			listOfCompany.append(row)
	#step1: create a new thread for retrieving tweets that all companies posted
	collectUserTimeline_thread = testTweepy.getUserTimeline(db,api1,listOfCompany,"screenName")
	collectUserTimeline_thread.start()
	print "company user timelime start"
	#step2:find all followers for all companies
	followersIds = getFollowersIds(api2,listOfCompany)

	#step3: create a new thread for retrieving tweets that all followers of all companies posted and mentioned the corresponding company
	collectFollowersTimeline_thread = testTweepy.getUserTimeline(db,api3,followersIds,"user_id")
	collectFollowersTimeline_thread.start()
	print "followers timelime start"

	#step4: create a new thread for searching all relevant tweets for all companies
	search_thread = testTweepy.search(db,api6,listOfCompany)
	search_thread.start()
	print "search start"

	#step5: use streaming API to retrieve live tweets
	nameOfCompany = []
	tmp = []
	streamFilter = []
	for each in listOfCompany:
		tmp.append(each[0])
		tmp.append(each[2])
		nameOfCompany.append(tmp)
		streamFilter.append(each[0])
		streamFilter.append(each[2])
		tmp = []
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener(db,nameOfCompany)
	auth = OAuthHandler('8FWIMWkMWaLKtbSyUkDcsAO8Z', 'JTPVp6izcJ73PSL4fbTaVWSFGFiJM4m0TZj1J5gSKtiuL6vaCA')
	auth.set_access_token('2723420030-WFrcjeXsVIV1AHgWZ1YhTVb7RCxmftZQB8D8IOW', 'EvAUoawFAdVPEfTjiRZY7xxAuyqNuLv4WVI86Eh797HUK')
	stream = Stream(auth, l)
	print "streaming start"

	print "main over"

#This method is used to retrieve all followers of each company
def getFollowersIds(api,listOfCompany):
	result = []
	for each in listOfCompany:
		ids = [each]
		tweets = tweepy.Cursor(api.followers_ids, screen_name=each[0]).items()
		ids.extend(tweets)
		result.append(ids)
	return result


if __name__ == "__main__":
	main()