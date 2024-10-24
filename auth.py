from pywebostv.connection import *
import os
import time
import json


def save_to_json(data):
  try:
    with open('/data/store.json', 'w') as f:
      json.dump(data, f)
  except Exception as e:
    print(e)
    
def load_from_json():
  try:
    with open('/data/store.json', 'r') as f:
      return json.load(f)
  except Exception as e:
    return {}
  
def get_client():
  store = load_from_json()
  smarttv_ip = os.getenv("SMARTTV_IP")
  client = WebOSClient(smarttv_ip, secure=True)

  client.connect()
  for status in client.register(store):
      if status == WebOSClient.PROMPTED:
          print("Please accept the connect on the TV!")
      elif status == WebOSClient.REGISTERED:
          print("Registration successful!")

  save_to_json(store)
  return client
