import os
import json
def read():
    dbUser=os.getenv('DBUSER')
    dbPw=os.getenv('DBPW')
    print(dbUser,dbPw)
    creds={
        'localhost':{
            "user":dbUser,
            "password":dbPw,
        }
    }
    return creds