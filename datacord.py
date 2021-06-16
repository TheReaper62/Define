
'''
1 June 2021
This is the module needed to communicate with Datacord Databases
There are currently no virtually no limits set on requests frequency
Requires the python json module and requests module
'''

import requests,json,ast
BASEURL = "https://DataCord.fishballnooodle.repl.co"
auth = {"client-name":"Define"}

def ToDatabase(key,value):
    req_obj = {
        "KEY" : f"Define-{key}",
        "VALUE" : value,
        "checksum": "Moderation χ"
    }
    resp = requests.post(BASEURL+f"/ToDatabase",json=json.dumps(req_obj),headers=auth)
    print(f"\n\n{resp.text}\n\n")
    if resp.text=="Action Complete":
        return True
    return json.loads(resp.text)


def FromDatabase(key):
    resp = requests.get(BASEURL+f"/FromDatabase?KEY=Define-{key}",headers=auth)
    print(f"\n\n{resp.text}\n\n")
    if resp.text == "KeyError":
        raise KeyError
    return ast.literal_eval(resp.text)

def ReturnDatabase():
    resp = requests.post(BASEURL+f"/ReturnDatabase",headers=auth)
    print(f"\n\n{resp.text}\n\n")
    return ast.literal_eval(resp.text)

def FromFileSystem(key):
    resp = requests.get(BASEURL+f"/FromFileSystem?KEY=Define-{key}",headers=auth)
    print(f"\n\n{resp.text}\n\n")
    if resp.text == "KeyError":
        raise KeyError
    return ast.literal_eval(resp.text)
