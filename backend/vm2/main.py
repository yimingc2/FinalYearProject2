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

	def on_data(self, tweet):
		print "find~~"
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
				print "saved find"
				return True
		

	def on_error(self, status):
		print status

def main():

	couch = couchdb.Server('http://115.146.89.12:5984/');
	try:
		db = couch.create('tweets')
	except couchdb.http.PreconditionFailed as e:
		db = couch['tweets']

	client7 = testTweepy.clientKeys("2723420030-EplcykApi32aUOGYdTmYyvUDYkwS7EuwjpdjYpN","lpWqn6zRqThENXIeZA8urnC6OjPfa3sYNBIlDWpnpVwCv","h3rvFAz5iL5CO7009iBouOtMx","lX4SOmsMcpNwF8NWWEkN5Kommjw4wBXUsVLjLFUEJLgIHyxhVl",7)
	api7 = client7.OAuth()

	client8 = testTweepy.clientKeys("2723420030-9lm4QbApyJF3HrY3tDTXO0JrN5rlL64rJZid5j3","5lwziiIzHcg5NIrIxYqsaFLiRxUbH5xbmESPXi8VbzN2v","FILYNZgZnvZSmtCDAxrmc2oIQ","88afPKrcRhe6aGgvQVj0XCj1kFR3GIvizqqsatQSXD3KaXABc8",8)
	api8 = client8.OAuth()

	client9 = testTweepy.clientKeys("2723420030-84cDhUU44DH2rbYt0cZknt7tG2aNPsO7VvktvZH","ZxtiYFWpXUXuSaoLcw8oYua4Dv5y3veWg3qoM9Snb3tSg","Jau8yUmvwR2uS4zV1Karh5GQ5","A0g0urvJnT7T4MGZJ6ejuktApcACfTu0REZVNYtIwb48yYiXVS",9)
	api9 = client9.OAuth()

	client10 = testTweepy.clientKeys("2723420030-3MxAVSEemzOc1Cy42A1L6N9iUH3E1R7dbmDq0Yy","1J52pHsceIYsoEfwddyKJzjnUti2bByApfzyvWhZA7agu","Uh1Y838oM7Ft6cgBl1nz2YWXG","PEKEgE3CPbWhHzrf0ydrjez332fG2xfXjgyV5w1qbwvujo2djx",10)
	api10 = client10.OAuth()

	client11 = testTweepy.clientKeys("2723420030-iUTktQSByfp9o5AwyOJ7N0S3aD7nHTxF8BIjBIe","OKFML39rpJZVTvVazGNuB2vRiaKe2FMUwbrs8xVzaJ06z","aOjxmM1YBnLTcrZnhBI8C9ExO","FkvJ70j54lKV9rWR8rAb469psQ0JrgcjXj5bGw6aHf0oUFtXi4",11)
	api11 = client11.OAuth()

	client12 = testTweepy.clientKeys("2723420030-TUHv3ezbftRgTFiOpuP2GDjAfpfpDRQayctJ19f","EUwnQ10xCUF5KQI9ZoXdtVlG3xWVxDqRYNPXL008t1ISp","0W9781E4BdIb0E30sfsRgpSJP","l90cvuUgqHukfcqxYbiw4Mk2E2K0sWl4dUwlLGipAtYxUsxv4b",12)
	api12 = client12.OAuth()

	#read CSV File
	list1 = []
	with open('list1.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list1.append(row)
	list2 = []
	with open('list2.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list2.append(row)
	userTimelineCompany = []
	with open('smallData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			userTimelineCompany.append(row)
	#step1:comany post, new thread
	collectUserTimeline_thread = testTweepy.getUserTimeline(db,api7,userTimelineCompany,"screenName")
	collectUserTimeline_thread.start()
	print "company user timelime start"
	#step2:find all followers
	followersIds1 = getFollowersIds(api8,list1)
	followersIds2 = getFollowersIds(api8,list2)
	#break point
	#step3:followers post,new thread
	collectFollowersTimeline_thread1 = testTweepy.getUserTimeline(db,api9,followersIds1,"user_id")
	collectFollowersTimeline_thread1.start()
	collectFollowersTimeline_thread2 = testTweepy.getUserTimeline(db,api10,followersIds2,"user_id")
	collectFollowersTimeline_thread2.start()
	print "followers timelime start"
	#step4:search, new thread

	search_thread1 = testTweepy.search(db,api11,list1)
	search_thread1.start()
	search_thread2 = testTweepy.search(db,api12,list2)
	search_thread2.start()
	print "search start"
	#step5:streaming,realtime data
	#This handles Twitter authetification and the connection to Twitter Streaming API
	# print "search ok~"
	#[[c1,a1],[c2,a2]]
	listOfCompany = list1
	listOfCompany.extend(list2)
	nameOfCompany = []
	tmp = []
	#[c1,a1,c2,a2]
	streamFilter = []
	for each in listOfCompany:
		tmp.append(each[0])
		tmp.append(each[2])
		nameOfCompany.append(tmp)
		streamFilter.append(each[0])
		streamFilter.append(each[2])
		tmp = []
	l = StdOutListener(db,nameOfCompany)
	auth = OAuthHandler('8FWIMWkMWaLKtbSyUkDcsAO8Z', 'JTPVp6izcJ73PSL4fbTaVWSFGFiJM4m0TZj1J5gSKtiuL6vaCA')
	auth.set_access_token('2723420030-WFrcjeXsVIV1AHgWZ1YhTVb7RCxmftZQB8D8IOW', 'EvAUoawFAdVPEfTjiRZY7xxAuyqNuLv4WVI86Eh797HUK')
	stream = Stream(auth, l)
	print "streaming start"

 #    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	stream.filter(track=streamFilter,languages = ["en"])
	print "main over"

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