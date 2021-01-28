from pymongo import MongoClient
import os


cluster = MongoClient(os.getenv("MONGODB_URI", 'mongodb://127.0.0.1:27017/DBOT'))
pref = cluster.DBOT.PREF
bal = cluster.DBOT.BALANCE
owners = cluster.DBOT.OWNERS
ecoemoji = cluster.DBOT.EMOJI
welcch = cluster.DBOT.WELCCH
exitch = cluster.DBOT.EXITCH