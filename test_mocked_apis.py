import json
import requests

# GET (original api: http://jsonplaceholder.typicode.com/ => http://mock-pawelste.c9users.io/r1RqbY/ (MOCKED))
headers = {'Content-type': 'application/json'}
res = requests.get("http://localhost:8000/TsjR2n/", headers=headers)
print(res.json())
print(res.status_code)

# ## POST (original api: https://flask-app-pawelste.c9users.io/ => http://mock-pawelste.c9users.io/GoEcMu/ (MOCKED))
# headers = {'Content-type': 'application/json'}
# data = {'key': 'value'}
# res = requests.post('http://mock-pawelste.c9users.io/GoEcMu/restapis/?format=json', data=data, headers=headers)
# print(res.json())
# print(res.status_code)
#
# ## PATCH (original api: https://flask-app-pawelste.c9users.io/ => http://mock-pawelste.c9users.io/GoEcMu/ (MOCKED))
# headers = {'Content-type': 'application/json'}
# data = {'key': 'value'}
# res = requests.patch('http://mock-pawelste.c9users.io/wjQPAM/restapis/?format=json', data=data, headers=headers)
# print(res.json())
# print(res.status_code)
#
# ## PUT (original api: https://flask-app-pawelste.c9users.io/ => http://mock-pawelste.c9users.io/GoEcMu/ (MOCKED))
# headers = {'Content-type': 'application/json'}
# data = {'key': 'value'}
# res = requests.put('http://mock-pawelste.c9users.io/wjQPAM/restapis/?format=json', data=data, headers=headers)
# print(res.json())
# print(res.status_code)
#
# # GET (Bledny endpoint)
# headers = {'Content-type': 'application/json'}
# res = requests.get("http://mock-pawelste.c9users.io/r1RqbY/asdasdasd/?format=json", headers=headers)
# print(res.json())
# print(res.status_code)