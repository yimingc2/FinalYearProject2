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
		try:
			print "find~~"
			f = testTweepy.functions()
			all_data = json.loads(tweet)
			if 'text' in all_data:
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
			else:
				print 'This does not have a text entry'
		except Exception,e:
			print "streaming exception"
		

	def on_error(self, status):
		print status

def main():

	couch = couchdb.Server('http://115.146.89.12:5984/');
	try:
		db = couch.create('tweets')
	except couchdb.http.PreconditionFailed as e:
		db = couch['tweets']

	client25 = testTweepy.clientKeys("2723420030-7Rcvp9nXIIPGWB8IsOCMkts4YHcXPom36FCtT9L","gjg5RFYRHJrU6aEMT8MvKzCTORgyc0iYrfYB0KwdtpqJB","b3mRv2HYjPoekuE0AjHVhxHFg","zY42dCT8c2PhWj4qBE7ZKTbVIIEGTRfvyRXsAZ4ZQYo6O1s673",25)
	api25 = client25.OAuth()

	client26 = testTweepy.clientKeys("2723420030-WSRBT6DX4y8yNf2FnKPQxgomXcirYscQQf7E2DF","073SmrI7FQ3NKZcRUfyOYkRBbM3Y9kh39nvkQYaBuEasq","dIZDF4GTsaua8q00hky8S9w96","w2NX30Gg6yPPtwR8GerXCkDag8MewY6GqLWHQSEqxmw59EXyjn",26)
	api26 = client26.OAuth()

	client27 = testTweepy.clientKeys("2723420030-dbLrRNNcPdDVVN9vU6gNe6ezmJIjBiFSTA4tZIK","iQDLE1UeBMsO1AAH12jxHz4eYscKbqYBCOzYPz4v8Wrm6","b9lVAy5VBbePQPsqxQvCW6bbn","C8ZMEtz6BOF8kNkotmLmJULvgyZW50r7FirDn5AJkpyjtHi61a",27)
	api27 = client27.OAuth()

	client28 = testTweepy.clientKeys("727698246571724800-pTS7vQrpXzkcZy2Xa252bA91V9eyAuX","Auw6gec17e93VNaT3RZylhEJcpZS6U2yoTRR8JgNet8Kg","wkVCCl1aXTrDXHiAqqUW5rSKs","heZKoWPP4dbCUf905gnx6pSrXugPYLOYuCLHTUtB8rMVy6SFgm",28)
	api28 = client28.OAuth()

	client29 = testTweepy.clientKeys("727698246571724800-nGxWtkrotWU82YaPjLqxqT8fYfgFq8H","9IOjOsWzfzsSG9FiTsIRCmt949bwnygAI4x5m1ne8PCar","HafWlU6lhWNSnPBZ6LOzQTTPk","cLwesptc8NELKP9vOGIjlN8j33i7EZkBmE7nJRwNOHdIck0sRg",29)
	api29 = client29.OAuth()

	client30 = testTweepy.clientKeys("727698246571724800-yaJtodv2gaAFzw5DNZSebKHYwD5RTBB","R8oqgADtOIOHhxfVtAfQIH47X4lJf9Txc1XIY093OxzwQ","RbR0qPH7aB3OPY5c1MxX1ydwV","eEL4AUFYfJb2esMCW32f228ycdvOd9lujKUBKWJyFLXF5tmFbE",24)
	api30 = client30.OAuth()

	#read CSV File
	list1 = []
	with open('list7.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list1.append(row)
	list2 = []
	with open('list8.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list2.append(row)
	userTimelineCompany = []
	with open('smallData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			userTimelineCompany.append(row)
	#step1:comany post, new thread
	collectUserTimeline_thread = testTweepy.getUserTimeline(db,api25,userTimelineCompany,"screenName")
	collectUserTimeline_thread.start()
	print "company user timelime start"
	#step2:find all followers
	followersIds1 = getFollowersIds(api26,list1)
	followersIds2 = getFollowersIds(api26,list2)
	#break point
	#step3:followers post,new thread
	collectFollowersTimeline_thread1 = testTweepy.getUserTimeline(db,api27,followersIds1,"user_id")
	collectFollowersTimeline_thread1.start()
	collectFollowersTimeline_thread2 = testTweepy.getUserTimeline(db,api28,followersIds2,"user_id")
	collectFollowersTimeline_thread2.start()
	print "followers timelime start"
	#step4:search, new thread

	search_thread1 = testTweepy.search(db,api29,list1)
	search_thread1.start()
	search_thread2 = testTweepy.search(db,api30,list2)
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