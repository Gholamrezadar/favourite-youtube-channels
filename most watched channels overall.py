import json
import re
import time

# parameters
N = 99999  # how many of the latest videos to check
M = 1000   # how many channels to list in the output. default: top 1000 channels of all time.

with open("watch-history.json", 'r', encoding="utf8") as f:
    # measuring time
    a = time.time_ns()

    # loading data
    data = json.load(f)
    # how many videos have you watched
    print(len(data), " videos watched")
    N = min(N,len(data))

    # measuring time
    b = time.time_ns()

    # main process
    channels = {}
    for video in data[:N]:
        # for deleted videos and other exceptions
        if "subtitles" not in video:
            continue

        channel_name = video["subtitles"][0]["name"]
        
        if channel_name in channels:
            channels[channel_name] += 1
        else:
            channels[channel_name] = 1

    # sort channels by views
    sorted_channels = {k: v for k, v in sorted(
        channels.items(), key=lambda item: item[1], reverse=True)}
    
    # measuring time
    print("loading took", int((b-a)/1000000), "ms")
    print("sorting took", int((time.time_ns()-b)/1000000), "ms")

    print()

    print("searching last", N, "videos")

    # print channels
    # all_results = [(k, v) for k, v in sorted_channels.items()]


    for i,item in enumerate(list(sorted_channels.items())[:M]):
        name, view = item
        print(i+1,"-", name, view)
    # [print(item[0],item[1]) for item in all_results[100]]
