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

	client13 = testTweepy.clientKeys("137367359-xTFdQYSCcAJoPGlSyHuQAxP3ieLtGUiLN8FKiduI","QSAYSrDVRFOckQfJ5qxp4vrkPXDSIzbQKHFCTOtDJXSKx","nFhq44qf9GVoSp7DSfWtOYkI6","YXXsC47XryCaG5690Wj1rpHjHu791QEGIN7jIwimetZWX9FDph",13)
	api13 = client13.OAuth()

	client14 = testTweepy.clientKeys("3161564544-U6YLon0E6N7ZvHtfvoeHRSdlCp4NbjHGd1acrBN","FaaZcVA2847YNA2igjFjjKpQvIgVUCNlh8H3ZvP2ey0Ro","WxOvbrNAzyjy7vszxJ6OLeyol","1s7s2f4SeryTN374dGMvoSwtXM10JHOYRVEd6JcJirqFYK9BE9",14)
	api14 = client14.OAuth()

	client15 = testTweepy.clientKeys("128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA","wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr","OvFt3ix2aummG26HtS8sT1MzU","71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0",15)
	api15 = client15.OAuth()

	client16 = testTweepy.clientKeys("2401399747-HGxObwgYtp2aFO6whX0GoQwNEn4E4yxK7mkHjEn","miPNtaUNvGDct6oKWJKO9SNZYYdIAzMG2aHODnfgadwMM","tsa7I86gihfEKCRfyQ8sM3ruc","rgGJJPser76YhlljzVFvo2V5qUaoZnaGxxaC5CdyZBqsKgYEim",16)
	api16 = client16.OAuth()

	client17 = testTweepy.clientKeys("1345785727-4q81KjFTZc5oFu0eEi3uxpQxiIKQRv2qZKjpYQv","LxHj4ymGyvBrtVhTdXO1iBcskFemj4IYn6w0s9BD6K2K5","40pGYbUc8fZ5CkEsw4VTsyWqH","TIxs2MMNuSJkwAmuGWAdCOamNKtrI7VaPJelrAkPhI4kpw3pqm",17)
	api17 = client17.OAuth()

	client18 = testTweepy.clientKeys("3522828433-xdClye90mkKqwSXGMwpIvnOZsvtx5XaecCbmnMR","8D3jM1gsw0iTYKeJUvwGPqFkIbt2pweJWIDk2Gv5RZk1u","oboRwqkiL05oePIWXpRL8WJUF","IdGHjwmj3yS5U99Bb2rU1sGMBT2YKHMoIzJHvWopYb9Khxe7LQ",18)
	api18 = client18.OAuth()

	#read CSV File
	list1 = []
	with open('list3.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list1.append(row)
	list2 = []
	with open('list4.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			list2.append(row)
	userTimelineCompany = []
	with open('smallData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			userTimelineCompany.append(row)
	#step1:comany post, new thread
	collectUserTimeline_thread = testTweepy.getUserTimeline(db,api13,userTimelineCompany,"screenName")
	collectUserTimeline_thread.start()
	print "company user timelime start"
	#step2:find all followers
	followersIds1 = getFollowersIds(api14,list1)
	followersIds2 = getFollowersIds(api14,list2)
	#break point
	#step3:followers post,new thread
	collectFollowersTimeline_thread1 = testTweepy.getUserTimeline(db,api15,followersIds1,"user_id")
	collectFollowersTimeline_thread1.start()
	collectFollowersTimeline_thread2 = testTweepy.getUserTimeline(db,api16,followersIds2,"user_id")
	collectFollowersTimeline_thread2.start()
	print "followers timelime start"
	#step4:search, new thread

	search_thread1 = testTweepy.search(db,api17,list1)
	search_thread1.start()
	search_thread2 = testTweepy.search(db,api18,list2)
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