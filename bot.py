import sys
import tweepy
import time

api = authenticate(c_key, c_secret_key, a_token, a_secret_token)

def bot():
	userID = input("userID to mock: ")
	
	while True:
		mock(api)

def mock(api):
	tweets = api.user_timeline(screen_name=userID, count=200, include_rts=False, tweet_mode='extended')

	for tweet in tweets:
		if tweet.full_text in seen:
			continue

		mock_text = mock(tweet.full_text)
		api.update_status(status=mock_text, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

		print("Mocking")
		print("Mocked text: " + mock_text)

		store_seen_id()
		time.sleep(1)

	with open("seen.txt", "w") as saver:
		for tweet in seen:
			saver.write(tweet.full_text)

	print("Saved.")

def store_seen_id(userID, id):
	filename = userID + ".txt"

	with open(filename, "w") as writer:
		writer.write(id)

def retrieve_seen_id(userID, count):
	ids = []

	filename = userID + ".txt"
	with open(filename, "r") as reader:
		for i, row in enumerate(reader):
			if i < count:
				ids.append(row)
			else:
				break
	return ids




def authenticate(c_key, c_secret_key, a_token, a_secret_token):
	print("Authenticating...")
	with open("auth_assets.json", "r") as file:
		keys = json.loads(file.read())
		c_key = keys['ConsumerKey']
		c_secret_key = keys['ConsumerSecretKey']
		a_token = keys['APIKey']
		auth = tweepy.OAuthHandler(c_key, c_secret_key).set_access_token(a_token, a_secret_token)
		api = tweepy.API(auth)
	print("Authentication successful.")
	return api

def timer(s):
	for i in range(s, 0, -1):
		print(("\r"  + str(i) + " seconds left until next call"), end="", flush=True)
		time.sleep(1)
	print("\r")


def read(file):
	seen = []
	for row in file:
		seen.append(row)
	return seen

def mock_text(stringi):
	result = ""
	for i, char in enumerate(string):
		if i % 2 == 0:
			result += char.upper()
		else:
			result += char.lower()
	return result

bot()
