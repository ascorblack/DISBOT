from pymongo import MongoClient

cluster = MongoClient("*")
pref = cluster.DBOT.PREF
bal = cluster.DBOT.BALANCE
owners = cluster.DBOT.OWNERS
ecoemoji = cluster.DBOT.EMOJI
welcch = cluster.DBOT.WELCCH
exitch = cluster.DBOT.EXITCH
newschan = cluster.DBOT.NEWSCHANNEL
lastnews = cluster.DBOT.LASTNEWS
