import tweepy
import time
import json
import logging

logging.basicConfig(
	filename='info.log', filemode='w', 
	level=logging.INFO, encoding='utf-8',
	format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Authenticating...")
with open("auth_assets.json", "r") as file:
	keys = json.loads(file.read())
	c_key = keys['APIKey']
	c_secret_key = keys['APISecretKey']
	a_token = keys['AccessToken']
	a_secret_token = keys['AccessTokenSecret']
	auth = tweepy.OAuthHandler(c_key, c_secret_key)
	auth.set_access_token(a_token, a_secret_token)
	api = tweepy.API(auth)
logging.info("Authentication successful")

def bot():
	userName = input("user to mock: ")

	try:
		user = api.get_user(screen_name=userName)
	except:
		raise Exception("The user does not exist, or the username is incorrect.")

	userID = user.id

	while True:
		mock_reply(userID)
		timer(15)

def mock_reply(userID):
	last_seen_id = retrieve_last_seen_id(userID)

	logging.info("Retrieving latest tweets...")
	latest_tweet = api.user_timeline(user_id=userID, count=1, include_rts=False, tweet_mode='extended')[0]
	
	if latest_tweet.full_text == '':
		logging.info("Media tweet with no text to mock")
		return

	if latest_tweet.id == last_seen_id:
		logging.info("No new tweets yet")
		return

	mock_text = mock(latest_tweet.full_text)

	logging.info("Mocking...")

	api.update_status(status=mock_text, in_reply_to_status_id=latest_tweet.id, auto_populate_reply_metadata=True)

	logging.info("Mocked tweet: %s" % latest_tweet.full_text)
	logging.info("Reply: %s" % mock_text)

	store_last_seen_id(userID, latest_tweet.id)

def store_last_seen_id(userID, tweet_id):
	with open("last_seen_ids.json", "r") as reader:
		last_seen_ids = json.load(reader) 

	last_seen_ids[userID] = tweet_id

	with open("last_seen_ids.json", "w") as writer:
		json.dump(last_seen_ids, writer, indent=4)

def retrieve_last_seen_id(userID):
	with open("last_seen_ids.json", "r") as file:
		seen_ids = json.load(file)
		if str(userID) in seen_ids:
			return int(seen_ids[str(userID)])
		else:
			return None

def timer(s):
	logging.info("Waiting %i seconds until next call" % s)
	for i in range(s, 0, -1):
		time.sleep(1)

def getPureText(string):
	words = string.split()
	result = ""
	for i, word in enumerate(words):
		if word[0] != '@' and word[0:4] != 'http':
			result += word + " "
	return result

def mock(string):
	words = getPureText(string).split()

	result = ''
	for i, word in enumerate(words):
		mocked_text = ''
		for j, char in enumerate(word):
			mocked_text += (char.lower() if j % 2 == 0 else char.upper())
		words[i] = mocked_text
	return ' '.join(words)

bot()
