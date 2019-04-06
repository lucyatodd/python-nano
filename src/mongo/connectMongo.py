import pymongo
import configparser

config = configparser.RawConfigParser()
config.read("config.properties")

user = config.get('DatabaseSection','mongo.user') 
password = config.get('DatabaseSection','mongo.password')
host = config.get('DatabaseSection','mongo.host')
database = config.get('DatabaseSection','mongo.database')

details = f"{user} {password} {host} {database}"
print("details ", details)

connectionStr = f"mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true"
client = pymongo.MongoClient(connectionStr)
db = client.explore

topics = db.topics.find({"subject": "algebra"}, {"_id": 0, "special": 1})
#for topic in topics:
#   print('TOPIC ', topic)
#   print('SPECIAL ', topic["special"])
#   print('NOTATION ', topic["special"]["notation"])

firstT = db.topics.find_one({"subject": "algebra"}, {"_id": 0, "special": 1})
#print('TOPIC ', firstT)
#print('SPECIAL ', firstT["special"])
#print('NOTATION ', firstT["special"]["notation"])

firstRef = db.topics.find_one({"special.notation": "yes"})
print('1st REF ', firstRef)

subjects = db.subjects.find()
# for subject in subjects:
   # print('SUBJECT = ', subject)

users = db.users.find({"name": "paul"})
# for user in users:
   # print('USER:PASSWORD = ', user["password"])

client.close()
