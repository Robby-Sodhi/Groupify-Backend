import asyncio
import json
import websockets

USERS = set() #no duplicates

default_track = "TEMPORARY"

def track_change():
    return json.dumps({"type": "track_change", "track": default_track})


async def connection(websocket):
     global USERS, default_track
     try:
        USERS.add(websocket) #no duplicates sets cannot contain duplicates
        await websocket.send(track_change()) #send new user the current default track

        async for message in websocket:
            event = json.loads(message)
            print(event)
            if event["type"] == "track_change":
                if (event["track"] != default_track):
                 default_track = event["track"]  
                 websockets.broadcast(USERS, track_change())
            elif event["type"] == "leave":
               USERS.remove(websocket)
            else:
                print("error unsupported action")


     finally: #connection disconnected 
        USERS.remove(websocket)
        websocket.close(1000)

async def main():
    async with websockets.serve(connection, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
