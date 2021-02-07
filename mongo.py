from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbdbot:752113crjhgc@dbot.xvrkg.mongodb.net/DBOT?retryWrites=true&w=majority")
pref = cluster.DBOT.PREF
bal = cluster.DBOT.BALANCE
owners = cluster.DBOT.OWNERS
ecoemoji = cluster.DBOT.EMOJI
welcch = cluster.DBOT.WELCCH
exitch = cluster.DBOT.EXITCH
newschan = cluster.DBOT.NEWSCHANNEL
lastnews = cluster.DBOT.LASTNEWS