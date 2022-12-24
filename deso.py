import requests

def get_profile(username: str):
  url = 'https://localhost:7070/api/v0/get-single-profile'
  data = {
   "Username": username,
   "PublicKeyBase58Check": "",
  }
  response = requests.post(url,  json=data)
  print(response.text)
  response_json = response.json()
  print(response_json)

get_profile('abhigya')