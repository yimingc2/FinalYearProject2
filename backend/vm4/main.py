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

	client19 = testTweepy.clientKeys("727131792042430464-jm5PAa5baFRUiDiAnZAOhg71T3LUL3n","4zTxOKjnZS9gvaTUx2OZ8CqhCyNi5VpMETPHNCdCB3Upn","xFzz6VMUVhLSTzJqp2a8Dc014","F6etmx9ORRP0T9tSRShTPM2bzGI95Lik7mOxrCucfwTXD0NiVX",19)
	api19 = client19.OAuth()

	client20 = testTweepy.clientKeys("727131792042430464-5SxHiiBJ2jHE3hqMIxkMMYmObG6aPEY","wc5Scl4Win5KqpZVXrSp1TN9R4dRtJhm9Wx5O1SRyFt9k","63GgwRqGd4eLIjXQhcbgJnR7W","D0h7cIFtEAsk1oPQ9kZJmLw1StXZ79MPm7etl4rHbXcrm1PJfu",20)
	api20 = client20.OAuth()

	client21 = testTweepy.clientKeys("727131792042430464-QaPXJ2IxFAecrehN1P5PcBbvn7VYLmG","fPmGUCScPAZ8Vk3hZQHTrA9nrn6psRTLxXlRO5KeaTvmw","vl5SjNl7gjxfoLY6hAraPUka8","liXZwyO9DgAzcaKyAONnsJUFG7NrwJWNEBaVGrX46qnuIz3uXT",21)
	api21 = client21.OAuth()

	client22 = testTweepy.clientKeys("2723420030-1FxAMm8pMg9xPxoNAtBdvyOXgajvllf9QNYmOaY","aIabpM8rrgFY8CTbpEUdxA0f4TTpWrEBwnkyrctcgPbTM","FPttalYsxKxC0fdv5029IMsEe","71QCg37cEmQOEz2JpuR5TOfTN8cnLsLt6TOFAn5x996poQkG8K",22)
	api22 = client22.OAuth()

	client23 = testTweepy.clientKeys("2723420030-NRTtNrkYwBbGcrvZh5x3Epp8e1ZxwHJE3nAPm8W","QQB7dpIUX9sJubJ2yg8boy47puDWlPgKbCDIcxhL9s182","ZH8QIX0sy5agILRwURBKhVvIM","fNbzyvX7T8gZRYsZ9bZ9pO3XecngYKG6xA0ctPQmpUlKOqq6Qb",23)
	api23 = client23.OAuth()

	client24 = testTweepy.clientKeys("2723420030-f10SElof172GNPlsmvblyUb0G2ksIaMTaem6Nmd","xDLWpxyjFc3ZPZXJSTp6SZjly2hdOccUHeXl7gr3f37gf","JJfBFxvNN4RMKJwSzI92fmd3l","Bv1G95h1lIuW3PxzBNH9pE0vydL1YqlbwAqkINTTIDLTjYybSp",24)
	api24 = client24.OAuth()

	#read CSV File
	list1 = []
	with open('list5.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list1.append(row)
	list2 = []
	with open('list6.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list2.append(row)
	userTimelineCompany = []
	with open('smallData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			userTimelineCompany.append(row)
	#step1:comany post, new thread
	collectUserTimeline_thread = testTweepy.getUserTimeline(db,api19,userTimelineCompany,"screenName")
	collectUserTimeline_thread.start()
	print "company user timelime start"
	#step2:find all followers
	followersIds1 = getFollowersIds(api20,list1)
	followersIds2 = getFollowersIds(api20,list2)
	#break point
	#step3:followers post,new thread
	collectFollowersTimeline_thread1 = testTweepy.getUserTimeline(db,api21,followersIds1,"user_id")
	collectFollowersTimeline_thread1.start()
	collectFollowersTimeline_thread2 = testTweepy.getUserTimeline(db,api22,followersIds2,"user_id")
	collectFollowersTimeline_thread2.start()
	print "followers timelime start"
	#step4:search, new thread

	search_thread1 = testTweepy.search(db,api23,list1)
	search_thread1.start()
	search_thread2 = testTweepy.search(db,api24,list2)
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