from timeit import default_timer as timer
import matplotlib.pylab as plt
import seaborn as sns
from numpy import linspace
from statistics import mean
from os.path import dirname, realpath, join


LOCATION = join(dirname(realpath(__file__)), "data")


class Data:
    def __init__(self, title):
        self.title = title
        self.data = []
        # 1 data
        # 0 no.

    def formatted(self):
        formatted_data = []
        for i in range(0, len(self.data)):
            formatted_data.append([])
            for j in range(0, len(self.data[0])):
                formatted_data[i].append(j[1])

        return formatted_data

    def add(self, data):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[0])):
                total = self.data[i][j][0] + data[i][j][0]
                self.data[i][j][1] = (
                    self.data[i][j][0]*self.data[i][j][1] + data[i][j][1]*data[i][j][0])/total
                self.data[i][j][0] = total


def record_time(program):
    k = 2
    times = []

    for i in range(1, 3):
        times.append([])
        for j in range(1, 3):
            temp_times = []
            for _ in range(0, k):
                start = timer()
                program.run(i, j, 'XQ6J57B', verbosity=0)
                temp_times.append(timer()-start)
            avg_time = mean(temp_times)
            times[i-1].append([k, (avg_time)/(i*j)])

    return times


def save_data(data, title):
    file_loc = join(LOCATION, "threadVprocess", "%s.txt" % title)
    with shelve.open(file_loc) as db:
        db[title] = dumps(user)


def read_data(title):
    file_loc = join(LOCATION, "threadVprocess", "%s.txt" % title)
    with shelve.open(file_loc) as db:
        return loads(db[title])


def plot(data):
    ticks = linspace(0.5, len(data)-0.5, len(data))
    tick_labels = linspace(1, len(data), len(data))
    ax = sns.heatmap(data, linewidth=0.5)
    plt.xticks(ticks, tick_labels)
    plt.yticks(ticks, tick_labels)
    plt.show()


def run():
    processed_time = Data("processed")
    import processed
    processed_times.data = record_time(processed)
    del processed
    print(processed_times.data)

    print(processed_times)
    plot(processed_times)
    print("Done!")


if __name__ == "__main__":
    run()
# [[16.613458280000003, 9.84598059], [9.255524329999995, 5.584326045000003]]
