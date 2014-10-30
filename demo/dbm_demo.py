#!-*-encoding:utf8-*-

import dbm
db = dbm.open("bookmark",'c')
db["Log"] = "jackson.log"
print db["Log"]
db.close()