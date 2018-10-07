import matplotlib.pyplot as plt


if __name__ == '__main__':

    with open("timestamps.txt") as f:
        lines = f.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[1] for line in lines]

    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_title("Love Nerds Data")
    ax1.set_xlabel('timestamps ')
    ax1.set_ylabel('total messages')

    ax1.plot(x,y, c='r', label='the data')

    leg = ax1.legend()

    plt.show()
