import asyncio
import websockets
import json

async def fetch_notes():
    contents = []
    print("Fetching contact list from Nostr...")
    contact_list_message = json.dumps([
        "REQ",
        "contact_list_subscription",
        {
            "kinds": [3],
            "authors": ["4c5d5379a066339c88f6e101e3edb1fbaee4ede3eea35ffc6f1c664b3a4383ee"],
            "limit": 100
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

        print("Fetching notes from Nostr...")
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
                contents.append(content)
#                print('created_at=', note[2]['created_at'])
#                print('content=', content)
            if note[0] == "EOSE" and note[1] == "note_subscription":
                break
    return contents

import MeCab
from gensim.models import KeyedVectors

def compute_context_vector(contents):
    print("Loading word2vec model...")
    model = KeyedVectors.load_word2vec_format("entity_vector/entity_vector.model.bin", binary=True)
    print("Computing context vector...")
    mecab = MeCab.Tagger("-r /etc/mecabrc -Owakati")
    latest_content = contents[-1]
    x = []
    # compute similarity between the latest content and the rest (omit the latest content)
    latest_tokens = mecab.parse(latest_content).strip().split()
    #print("Tokens in latest content:", latest_tokens)
    similarities = []
    for content in contents[:-1]:
        content_tokens = mecab.parse(content).strip().split()
        similarity = model.n_similarity(latest_tokens, content_tokens)
        #print(f"Tokens in content {contents.index(content)}:", content_tokens)
        #print(f"Similarity of the latest content and {contents.index(content) + 1}th content:", similarity)
        similarities.append(similarity)
    # get the largest top 3 index
#    print("similarities:", similarities)
    sorted_similarities = sorted(similarities)
    index_similarities = sorted(range(len(similarities)), key=lambda k: similarities[k])
    n = 10
    top = [index_similarities[-i] for i in range(1, n + 1)]
    return top, sorted_similarities

contents = asyncio.run(fetch_notes())
contents = [content.replace('\n', ' ') for content in contents]
print("--------------------")
print("Latest content:", contents[-1])
print("--------------------")

top, sorted_similarities = compute_context_vector(contents)
#print related top contents with similarities
print("--------------------")
print("Latest content:", contents[-1])
for i in top:
    print("--------------------")
    print(f"Related content {i + 1} (similarity: {sorted_similarities[-1 - top.index(i)]}):", contents[i])
print("--------------------")

