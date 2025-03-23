import asyncio
import json
import websockets
import json
from datetime import datetime
import MeCab
from gensim.models import KeyedVectors

async def make_pub2name(relay, limit=400):
    pub2name = {}
    print("Fetching kind 0 events to build pub2name mapping...")
    print("Initial pub2name:", pub2name)
    last_created_at = 0
    gotevent = 0
    while True:
        gotevent_cur = 0
        kind0_message = json.dumps([
            "REQ",
            "kind0_subscription",
            {
                "kinds": [0],
                "limit": limit,
                "since": last_created_at+1
            }
        ])
        async with websockets.connect(relay) as websocket:
            await websocket.send(kind0_message)
            async for message in websocket:
                response = json.loads(message)
                if response[0] == "EVENT" and response[1] == "kind0_subscription":
                    content = json.loads(response[2]['content'])
                    pubkey = response[2]['pubkey']
                    name = content.get('name', 'Unknown')
                    pub2name[pubkey] = name
                    last_created_at = max(last_created_at, response[2]['created_at'])
                    #print("--------------------")
                    #print("pub2name[", pubkey, "]=", name)
                    #print(message)
                    #print("--------------------")
                    gotevent_cur += 1
                    gotevent += 1
                if response[0] == "EOSE" and response[1] == "kind0_subscription":
                    print(f"Got {gotevent} profiles...")
                    break
            # close when empty
            if gotevent_cur == 0:
                break
    return pub2name

async def fetch_notes(relay, mainid, limit=100):
    contents = []
    created_at = []
    pubkeys = []
    print("Fetching contact list from Nostr...")
    contact_list_message = json.dumps([
        "REQ",
        "contact_list_subscription",
        {
            "kinds": [3],
            "authors": [mainid],
            "limit": 1
        }
    ])
    async with websockets.connect(relay) as websocket:
        # Send a request to get the contact list
        await websocket.send(contact_list_message)

        # Process the contact list to get pubkeys
        async for message in websocket:
            response = json.loads(message)
#            print(message)
            if response[0] == "EVENT" and response[1] == "contact_list_subscription":
                followlist = [contact[1] for contact in response[2]['tags'] if contact[0] == 'p']
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
                "authors": followlist,
                "limit": limit
            }
        ])
        await websocket.send(subscribe_message)
#        print(subscribe_message)
        
        # Receive messages
        async for message in websocket:
            #            print(message)
            note = json.loads(message)
            if note[0] == "EVENT" and note[1] == "note_subscription":
                contents.append(note[2]['content'])
                created_at.append(note[2]['created_at'])
                pubkeys.append(note[2]['pubkey'])
#                print('created_at=', note[2]['created_at'])
#                print('content=', content)
            if note[0] == "EOSE" and note[1] == "note_subscription":
                break
    return pubkeys, contents, created_at

def compute_context_vector(contents):
    print("Loading word2vec model...")
    model = KeyedVectors.load_word2vec_format("entity_vector/entity_vector.model.bin", binary=True)
    print("Computing context vector...")
    mecab = MeCab.Tagger("-r /etc/mecabrc -Owakati")
    latest_content = contents[0]
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


# main ----------------------------------------------------
async def main():
    relay = "wss://yabu.me"
    mainid = "4c5d5379a066339c88f6e101e3edb1fbaee4ede3eea35ffc6f1c664b3a4383ee"

    pub2name = await make_pub2name(relay)
    pubkeys, contents, created_at = await fetch_notes(relay, mainid)

    contents = [content.replace('\n', ' ') for content in contents]
    for i in range(len(created_at)):
        created_at[i] = datetime.fromtimestamp(created_at[i]).strftime('%Y-%m-%d %H:%M:%S')

    latest_pubkey = pubkeys[0]
    # replace the latest_pubkey with the name (if unknown, use 10 letters of pubkey)
    latest_name = pub2name.get(latest_pubkey, latest_pubkey[:10])
    #print(pub2name)
    #print("main id = ", pub2name.get(mainid, "Unknown"))
    #print("latest_pubkey = <", latest_pubkey, ">")
    #print("mainid        = <", mainid, ">")
    print("--------------------")
    print(f"Latest content: {latest_name}:{created_at[0]}:{contents[0]}")
    print("--------------------")

    top, sorted_similarities = compute_context_vector(contents)

    for i in top:
        related_pubkey = pubkeys[i]
        related_name = pub2name.get(related_pubkey, related_pubkey[:10])
        print("--------------------")
        print(f"Related content({sorted_similarities[-1 - top.index(i)]:.3f}):{related_name}:{created_at[i]}:{contents[i]}")
    print("--------------------")

asyncio.run(main())
