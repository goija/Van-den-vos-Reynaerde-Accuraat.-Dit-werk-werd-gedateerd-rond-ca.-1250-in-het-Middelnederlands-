# signaling_server.py
import asyncio
import websockets
import json

# Houd een lijst bij van alle verbonden apparaten (peers)
connected_clients = set()

async def signaling_server(websocket, path):
    # Voeg het nieuwe apparaat (computer of mobiel) toe
    connected_clients.add(websocket)
    print(f"Nieuw apparaat verbonden. Totaal: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Bericht ontvangen type: {data.get('type')}")
            
            # Broadcast het bericht (Offer, Answer, of ICE) naar het ándere apparaat
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
                    
    except websockets.exceptions.ConnectionClosed:
        print("Verbinding verbroken.")
    finally:
        connected_clients.remove(websocket)
        print(f"Apparaat ontkoppeld. Totaal: {len(connected_clients)}")

# Start de server op alle netwerkinterfaces (0.0.0.0) op poort 8765
start_server = websockets.serve(signaling_server, "0.0.0.0", 8765)

print("Signaleringsserver draait... Wachtend op inkomende WebRTC oproepen.")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
