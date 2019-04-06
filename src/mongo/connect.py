import pymongo
client = pymongo.MongoClient("mongodb+srv://toddpa:f1gar0@lucyalex-aws-plymk.mongodb.net/explore?retryWrites=true")
db = client.explore

topics = db.topics.find()

for topic in topics:
   print('topic ', topic)

subjects = db.subjects.find()

for subject in subjects:
   print('topic ', subject)

client.close()

