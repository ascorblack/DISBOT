from pymongo import MongoClient
import os


cluster = MongoClient(os.environ.get("MONGODB_URI", 'mongodb://localhost/DBOT'))
pref = cluster.DBOT.PREF
bal = cluster.DBOT.BALANCE
owners = cluster.DBOT.OWNERS
ecoemoji = cluster.DBOT.EMOJI
welcch = cluster.DBOT.WELCCH
exitch = cluster.DBOT.EXITCH