import pymongo
import certifi

con_str = "mongodb+srv://FSDI:test1234@cluster0.s1z43ix.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database('Cluster0')