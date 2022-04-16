import requests



def addinfo(name,gender,status):
    body = {
        "id": 123,
        "name": name,
        "email": name.split(" ")[0]+"_"+name.split(" ")[1]+"@temp.com",
        "gender": gender,
        "status": status
    }

    return body

def getexpectedres(name,gender,status):

    body = {
        "name": name,
        "email": name.split(" ")[0]+"_"+name.split(" ")[1]+"@temp.com",
        "gender": gender,
        "status": status
    }

    return body

def editstatus(name,gender,status):
    body = {
        "name": name,
        "gender": gender,
        "status": status
    }

    return body

def get_usercount():

    response = requests.get('https://gorest.co.in/public-api/users/', params={'access-token': 'a2608d81deefb9d45d2ddef0f4365dc82deca66c52a74c8896ee9a20f21407b2'}, )

    json_response = response.json()

    total_count = json_response["meta"]["pagination"]["total"]

    return total_count