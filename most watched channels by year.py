import json
import re
import time

# parameters
N = 99999  # how many of the latest videos to check
M = 10  # top M channels per years

with open("watch-history.json", 'r', encoding="utf8") as f:
    # measuring time
    a = time.time_ns()

    # loading data
    data = json.load(f)

    # how many videos have you watched
    print(len(data), " videos watched")
    N = min(N,len(data))

    # measuring time after load
    b = time.time_ns()

    print("loading took", int((b-a)/1000000), "ms")
    print()

    # main process
    last_checked_video_number = 0
    # last checked year, init to latest videos year
    current_year = data[0]["time"][0:4]
    # optimizations improved the performance from 40 ms/year -> 15 ms/year avg
    while(last_checked_video_number < N):
        channels = {}

        n = 0
        # optimization : only go from the last years first video to the begining of time ( not from the latest video)
        for video in data[last_checked_video_number:N]:
            last_checked_video_number += 1

            # count videos in that year
            n += 1

            # for deleted videos and other exceptions
            if "subtitles" not in video:
                continue

            # handle last year where the year doesnt change anymore
            if last_checked_video_number>=N-1:
                # how many videos you have watched in that year
                print(current_year+" -", "you watched", n, "videos in", current_year)

            # ignore videos from other years
            if not video["time"].startswith(current_year):
                # how many videos you have watched in that year
                print(current_year+" -", "you watched", n, "videos in", current_year)

                # optimization : break insted of continue : stops the loop after the year changes
                current_year = video["time"][0:4]
                break

            channel_name = video["subtitles"][0]["name"]

            if channel_name in channels:
                channels[channel_name] += 1
            else:
                channels[channel_name] = 1

        # sort channels by views
        sorted_channels = {k: v for k, v in sorted(
            channels.items(), key=lambda item: item[1], reverse=True)}

        # measuring time
        temp_time = time.time_ns()
        print("sorting took", int((temp_time-b)/1000000), "ms")
        b = temp_time
        print()

        # print list of top M videos
        for i, item in enumerate(list(sorted_channels.items())[:M]):
            name, view = item
            print(i+1, "-", name, view)
        print()
