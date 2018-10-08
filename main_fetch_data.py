import time
import fbchat
import os

import matplotlib.pyplot as plt
from datetime import datetime

all_messages = []
months = {'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December'}


def make_plot():
    with open("timestamps.txt") as f:
        lines = f.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[1] for line in lines]

    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_title('Accumulated messages over time')
    ax1.set_xlabel('Timestamps ')
    ax1.set_ylabel('Total Messages')

    ax1.plot(x, y, c='r', label='the data')

    plt.show()


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

    for date in timestamp_data:
        print(str(date) + ": " + str(timestamp_data[date]))


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


def sort_by_months():
    f = open("Timestamps.txt", "r")
    timestamps = []
    for datapoint in f:
        parts = datapoint.split()
        timestamps.append(parts[0])


def main():
    global all_messages
    target = raw_input("Whose messages? ")

    client = fbchat.Client(os.environ['fb_username'], os.environ['fb_password'])
    user = client.searchForUsers(target)[0]

    uid = user.uid
    user_name = user.name

    messages = client.fetchThreadMessages(user.uid, limit=10000)

    all_messages += messages

    while len(messages) == 10000:
        timestamp = messages[len(messages) - 1].timestamp
        messages = client.fetchThreadMessages(user.uid, limit=10000, before=timestamp)

        all_messages += messages

    fetch_timestamp_data()
    messages_to_file(uid, user_name)
    timestamps_to_file()
    sort_by_months()
    make_plot()


if __name__ == "__main__":
    main()