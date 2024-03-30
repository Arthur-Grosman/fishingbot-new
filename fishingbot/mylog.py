import datetime


def my_log(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{current_time}: {msg}")

    with open('log.txt', 'a') as file:
        file.write(f"{current_time}: {msg}\n")


if __name__ == "__main__":
    my_log('running mylog.py')

my_log('Sourcing mylog.py')
