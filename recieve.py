import socket
from slack_sdk import WebClient
import json
import re
from slack_sdk.errors import SlackApiError
from send import token # a stupid way of obfuscating my user token

SLACK_BOT_TOKEN = token

client = WebClient(token=SLACK_BOT_TOKEN)

user_cache = {}


try:
    response = client.conversations_list(types="private_channel")
    user_private_channels = {channel["id"]: channel["name"] for channel in response["channels"]}

except SlackApiError as e:
    print(f"Error: {e.response['error']}")



def get_username(user_id):
    if user_id in user_cache:
        return user_cache[user_id] 

    try:
        response = client.users_info(user=user_id)
        username = response["user"]["name"]
        user_cache[user_id] = username
        return username
    except SlackApiError as e:
        print(f"Error fetching username for {user_id}: {e.response['error']}")
        return "Unknown"

def get_messages(cid):
    try:
        response = client.conversations_history(channel=cid)
        # messages = [[get_username(i["user"])+": "+i["text"],"thread_ts" in i.keys()] for i in response["messages"]]
        messages = []
        for i in response["messages"]:
            try:
                messages.append([get_username(i["user"])+": "+i["text"],"thread_ts" in i.keys()])
            except:
                print(i,"OOPSOOPSOOPOSOPOPS")
        msgs = []

        for i,j in messages:
            if "<" in i and ">" in i and "@" in i:
                a = re.split(r'[<>]+',i)
                for j in a:
                    if "@" in j:
                        a[a.index(j)] = get_username(j.replace("@",''))
                i = ''.join(a)
            if j:
                i += "                    Unfurl Thread                    "
            msgs.append(''.join(i))
        return msgs
    except SlackApiError as e:
        print(f"Error: {e}")

def get_thread(cid,index):
    respons = client.conversations_history(channel=cid)
    if "thread_ts" in respons["messages"][index].keys():
        print('thread found')
    else:
        return ""
    response = client.conversations_replies(channel=cid,ts = respons["messages"][index]["thread_ts"])

    messages = [get_username(i["user"])+": "+i["text"] for i in response["messages"]]
    msgs = []
    for i in messages:
        if "<" in i and ">" in i and "@" in i:
            a = re.split(r'[<>]+',i)
            for j in a:
                if "@" in j:
                    a[a.index(j)] = get_username(j.replace("@",''))
            i = ''.join(a)
        msgs.append(''.join(i))
    print(' '.join(msgs))
    return ' '.join(msgs)


def send_to_slack(message,channel = "C086M5DM8F7"):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message,
            as_user=True  
        )
        print(" Message sent to Slack!")
    except Exception as e:
        print("Slack Error:", e)

HOST = "0.0.0.0" 
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server listening on:{PORT}...")
channel = None
conns = []
new = False
while True:
    conn, addr = server.accept()
    print(f"Connection received")
    data = conn.recv(1024)
    if data:
        message = data.decode()
        if len(message.split("oshawottsarecute42")) > 1:
            channel = message.split("oshawottsarecute42")[1]
            messages = get_messages(channel)
            print(f"channel set :D, channel name = {channel}")
        elif message == "youreallyshouldnotbewritingthis":
            print("initial connection made, sending private channel data to sprig client")
            json_data = json.dumps(user_private_channels)
            conn.sendall(json_data.encode("utf_8"))
            print("sent channels!")
        elif len(message.split("lemmereadpls"))>1:
            print("read request recieved")
            num = int(message.split("lemmereadpls")[1])
            conn.sendall(messages[num].encode("utf_8"))
            print("sent messages!")
        elif len(message.split("threadpls"))>1:
            print("thread request recieved")
            num = int(message.split("threadpls")[1])
            conn.sendall(get_thread(channel,num).encode("utf_8"))
        else:
            print("Received:", message)
            send_to_slack(message,channel = channel)

    conn.close()
