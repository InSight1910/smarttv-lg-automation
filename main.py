from fastapi import FastAPI
import asyncio
import os
from pywebostv.controls import SystemControl, SourceControl
from wakeonlan import send_magic_packet
import time
import auth

app = FastAPI()
client = auth.get_client()

@app.get("/turn_off/{time}")
async def turn_off(time: int):
  await asyncio.sleep(time * 60)
  system = SystemControl(client)
  system.power_off()
  return {"status": "ok"}

@app.get("/turn_on")
async def turn_on():
  try:
    mac_address = os.getenv("MAC_ADDRESS")
    send_magic_packet("A4:36:C7:0A:86:9C")
    await asyncio.sleep(5)
    source = SourceControl(client)
    sources = source.list_sources() 
    selected_item = next((item for item in sources if item.label == "TV Vicente"), sources[0])
    source.set_source(selected_item)
    return {"status": "ok", "source": selected_item}
  except Exception as e:
    return {"status": "error", "message": str(e)}