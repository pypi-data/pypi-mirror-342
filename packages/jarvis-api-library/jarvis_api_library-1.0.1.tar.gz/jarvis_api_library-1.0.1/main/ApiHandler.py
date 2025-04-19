import requests
import os
import json

class RequestPuller:
  def __init__(self):
    pass
  
  def test_init(self):
    print("RequestPuller initialized successfully.")
    pass 
  
  def GET(url, filePath):
    response = requests.get(url)
    with open(filePath, "w+") as f:
      json.dump(response.json(), f, indent=4)