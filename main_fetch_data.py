import time
import fbchat
import os
import matplotlib.pyplot as plt

all_messages = []

def make_plot():
    with open("timestamps.txt") as f:
        lines = f.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[1] for line in lines]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title("Accumulated messages over time")    
    ax1.set_xlabel('Timestamps ')
    ax1.set_ylabel('Total Messages')
    ax1.plot(x,y, c='r', label='the data')
    leg = ax1.legend()
    plt.show()


def fetch_timestamp_data():
    timestamp_data = {}
    date = 0

    for message in all_messages:
        current_date = time.strftime("%D", time.localtime(int(message.timestamp)/1000 - 14400))
        if current_date != date:
            timestamp_data[current_date] = 1
            date = current_date
        else:
            timestamp_data[date] += 1

    for date in timestamp_data:
        print(str(date) + ": " + str(timestamp_data[date]))

def messages_to_file():
    f = open("Conversation.txt", "w")
    for message in all_messages:
        try:
            f.write(str(message.text) + " " + time.strftime("%D", time.localtime(int(message.timestamp)/1000 - 14400)) + "\n")
        except:
            continue
    f.close()

def timestamps_to_file():
    f = open("Timestamps.txt", "w")
    n = 0
    m = 0
    while m <= len(all_messages):
        n += 1
        m += 1
        f.write(str(all_messages[len(all_messages)-m].timestamp) + " " + str(n) + "\n")
    f.close()

if __name__ == "__main__":
    target = input("Whose messages? ")

    months = {'January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October',  'November', 'December'}

    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    client = fbchat.Client(os.environ['fb_username'], os.environ['fb_password'], user_agent=ua)
    user = client.searchForUsers(target)[0]
	
    all_messages = []
    messages = client.fetchThreadMessages(user.uid, limit=10000)

    all_messages += messages
	
    while len(messages)==10000:
        timestamp = messages[len(messages)-1].timestamp
        messages = client.fetchThreadMessages(user.uid, limit=10000, before=timestamp)

        all_messages += messages

	#print(all_messages[0].timestamp)

    fetch_timestamp_data()
    messages_to_file()
    timestamps_to_file()
    make_plot()

