from datetime import datetime
from math import ceil

class Util:

    labels = []
    values = []
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    def __init__(self):
        pass

    @classmethod
    def rotate(cls, l, n):
        return l[-n:] + l[:-n]

    @classmethod
    def sort_by_months(cls):
        f = open("Timestamps.txt", "r")
        timestamps = []
        for datapoint in f:
            parts = datapoint.split()
            timestamps.append(parts[0])

        date = datetime.fromtimestamp(float(timestamps[0]) / 1000.0)
        current_month = date.month
        count = 0
        total_messages = 0
        for timestamp in timestamps:
            total_messages += 1
            date = datetime.fromtimestamp(float(timestamp)/1000.0)
            month = date.month
            if current_month != month:
                current_month = month
                count += 1
                date_as_string = cls.months[month-1] + ", " + str(date.year)
                cls.labels.append(date_as_string)
                cls.values.append(total_messages)
        cls.labels = cls.rotate(cls.labels, 1)

    @classmethod
    def get_labels(cls):
        return cls.labels

    @classmethod
    def get_values(cls):
        return cls.values

    @classmethod
    def get_upper_bound(cls):
        max_value = float(max(cls.values))
        rounding_digit = len(str(max_value)) - 4
        upper_board = ceil(max_value / (10 ** rounding_digit)) * (10 ** rounding_digit)
        return upper_board
