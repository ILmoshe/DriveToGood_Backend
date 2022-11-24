# server.py
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import socketio

app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio)

app.mount("/ws", sio_app)


@sio.event
async def connect(sid, environ, auth):
    print("connect ", sid)
    await sio.emit("insure_connection", f"{sid}", room=sid)


@sio.event
async def join(sid, data):
    print(f"sid:{sid}\ndata:{data}")
    sio.enter_room(sid, room=data["room"])
    await sio.emit("join_response", 'JOINED ROOM SUCsESSFULY')


@sio.event
async def my_message(sid, data):
    print(data)
    await sio.emit('my_message', data, room=data["room"], skip_sid=sid)


@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")


if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 8001}
    kwargs.update({"reload": True})
    uvicorn.run("socketIO:app", **kwargs)