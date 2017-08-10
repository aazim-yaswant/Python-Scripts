from slacker import Slacker
import os
import json

token="TOKEN_HERE"

def doTestAuth(slack):
    testAuth = slack.auth.test().body
    print("Succesfully authenticated")
    return testAuth

def getUserMap(slack):
	users = slack.users.list().body['members']
	userIdNameMap = {}
	for user in users:
		userIdNameMap[user['id']] = user['name']
	print("found {0} users ".format(len(users)))
	return userIdNameMap

def getHistory(pageableObject, channelId, pageSize = 100):
	messages = []
	lastTimestamp = None
	while(True):
		response = pageableObject.history(
		channel = channelId,
		latest  = lastTimestamp,
		oldest  = 0,
		count   = pageSize
		).body

		messages.extend(response['messages'])

		if (response['has_more'] == True):
			lastTimestamp = messages[-1]['ts'] # -1 means last element in a list
		else:
		    break
	return messages

def getDirectMessages(slack, ownerId, userIdNameMap):
	dms = slack.im.list().body['ims']
	parentDir = "direct_messages"
	try:
		os.makedirs(parentDir)
	except:
		print_message('direct_messages/artrix.json')
		exit()
	print("\nfound direct messages (1:1) with the following users:")
	for dm in dms:
		print(userIdNameMap.get(dm['user'], dm['user'] + " (name unknown)"))

	for dm in dms:
		name = userIdNameMap.get(dm['user'], dm['user'] + " (name unknown)")
		print("getting history for direct messages with {0}".format(name))
		fileName = "{parent}/{file}.json".format(parent = parentDir, file = name)
		messages = getHistory(slack.im, dm['id'])
		channelInfo = {'members': [dm['user'], ownerId]}
		with open(fileName, 'w') as outFile:
			print("writing {0} records to {1}".format(len(messages), fileName))
			json.dump({'channel_info': channelInfo, 'messages': messages}, outFile, indent=4)
	return

def print_message(file):
	data=json.load(open(file))
	important=list(data.items()[1])[1]
	for i in range(len(important)):
		print(list(data.items()[1])[1][i]["text"])
	return
slack=Slacker(token)

testAuth=doTestAuth(slack)
userIdNameMap = getUserMap(slack)
getDirectMessages(slack, testAuth['user_id'], userIdNameMap)
print_message('direct_messages/artrix.json')
