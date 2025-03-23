import asyncio
import websockets
import json

async def fetch_notes():
    # Nostr protocol message format for contact list
    contact_list_message = json.dumps([
        "REQ",
        "contact_list_subscription",
        {
            "kinds": [3],
            "authors": ["4c5d5379a066339c88f6e101e3edb1fbaee4ede3eea35ffc6f1c664b3a4383ee"]
        }
    ])
    uri = "wss://yabu.me"
    async with websockets.connect(uri) as websocket:
        # Send a request to get the contact list
        await websocket.send(contact_list_message)

        # Process the contact list to get pubkeys
        async for message in websocket:
            response = json.loads(message)
#            print(message)
            if response[0] == "EVENT" and response[1] == "contact_list_subscription":
                pubkeys = [contact[1] for contact in response[2]['tags'] if contact[0] == 'p']
                # Close the contact list subscription
                close_message = json.dumps(["CLOSE", "contact_list_subscription"])
                await websocket.send(close_message)
                break

        # Now use these pubkeys to fetch notes
        subscribe_message = json.dumps([
            "REQ",
            "note_subscription",
            {
                "kinds": [1],
#                "authors": pubkeys
            }
        ])
        await websocket.send(subscribe_message)
#        print(subscribe_message)
        
        # Receive messages
        async for message in websocket:
#            print(message)
            note = json.loads(message)
            if note[0] == "EVENT" and note[1] == "note_subscription":
                content = note[2]['content']
                print('content=', content)
            if note[0] == "EOSE" and note[1] == "note_subscription":
                break

# Run the async function
asyncio.run(fetch_notes())
