import time
import fbchat
import os

all_messages = []


def fetch_timestamp_data():
    timestamp_data = {}
    date = 0

    for message in all_messages:
        current_date = time.strftime("%D", time.localtime(int(message.timestamp) / 1000 - 14400))
        if current_date != date:
            timestamp_data[current_date] = 1
            date = current_date
        else:
            timestamp_data[date] += 1


def messages_to_file(uid, user_name):
    f = open("Conversation.txt", "w")
    for message in all_messages:
        try:
            if message.author == uid:
                name = user_name
            else:
                name = "Ajay Fewell"
            f.write(name + ": " + str(message.text) + " " + time.strftime("%D", time.localtime(
                int(message.timestamp) / 1000 - 14400)) + "\n")
        except:
            continue
    f.close()


def timestamps_to_file():
    f = open("Timestamps.txt", "w")
    message_count = 0
    while message_count <= len(all_messages):
        message_count += 1
        f.write(str(all_messages[len(all_messages) - message_count].timestamp) + " " + str(message_count) + "\n")
    f.close()


def main():
    global all_messages
    target = raw_input("Whose messages? ")

    client = fbchat.Client(os.environ['fb_username'], os.environ['fb_password'])
    user = client.searchForUsers(target)[0]
    uid = user.uid
    user_name = user.name

    messages_chunk = client.fetchThreadMessages(user.uid, limit=10000)
    all_messages += messages_chunk

    while len(messages_chunk) == 10000:
        timestamp = messages_chunk[len(messages_chunk) - 1].timestamp
        messages_chunk = client.fetchThreadMessages(user.uid, limit=10000, before=timestamp)
        all_messages += messages_chunk

    messages_to_file(uid, user_name)
    timestamps_to_file()


if __name__ == "__main__":
    main()
