import sys
import csv
import glob
import json


def load_stage_file(data, filename):
    print "loading", filename
    with open(filename) as handle:
        # We store it outside the loop for riders with the same
        # time as a previous rider.
        current_time = ""
        for line in handle:
            #print line
            tokens = line.split()
            pos = tokens.pop(0)
            country = next((x for x in tokens if x.startswith("(")), "")
            country_index = tokens.index(country)
            name = tokens[0:country_index]
            team = tokens[country_index+1:]

            if team[-1].find(':') != -1:
                current_time = team.pop()
            if int(pos) == 1:
                current_time = "0:0:0"

            name = " ".join(name)
            team = " ".join(team)
            time = [int(x) for x in current_time.split(":")]
            time = 3600*time[0] + 60*time[1] + time[2]

            if name not in data:
                data[name] = {"country":country, "team": team, "time": [time]}
            else:
                data[name]["time"].append(time)

def rider_key(x):
    """Generates a value for rider sorting."""
    #It is equal to the number of stagest ridden minus the last gap.
    return 1000000*len(x[-1]) - x[-1][-1]

def main(argv=None):

    if argv is None:
        argv = sys.argv[:]

    # FIXME do not hardcode glob pattern. Get it from command line.
    files = sorted(glob.glob("data/giro_2016/giro_*.txt"))
    try:
        number = int(argv[1])
    except Exception, e:
        number = sys.maxint

    data = {} # Key cyclist name. Values: (Country, Team, List of stage diffs)

    for filename in files:
        load_stage_file(data, filename)

    ordered_data = [] # [(cyclist, times)] # from last to next

    for current_name in data:
        current_times = data[current_name]["time"]
        current_team = data[current_name]["team"]
        current_country = data[current_name]["country"]
        current_stages = len(current_times)

        ordered_data.append((current_name, current_team, current_country, current_times))

    ordered_data.sort(key=rider_key)

    print "Total riders: ", len(ordered_data)

    # FIXME Could be a method.
    json_data = {}
    teams = []
    i = 0
    for name, team, country, times in ordered_data[::-1]:
        i += 1
        if i > number:
            break

        # times = data[name]["time"]
        cyclist_data = {}

        cyclist_data["name"] = name
        cyclist_data["team"] = team
        cyclist_data["country"] = country
        cyclist_data["time"] = []
        cyclist_data["pos"] = i

        if team not in teams:
            teams.append(team)

        for value in times:
            cyclist_data["time"].append(value)

        json_data[name] = cyclist_data


    print(sorted(teams))
    print(len(teams))

    teams_dict = {}
    for team in teams:
        teams_dict[team] = {"color":"0x000000"}


    with open("data/output.json", "w") as handle:
        handle.write(json.dumps(json_data))

    # with open("data/teamsraw.json", "w") as handle:
    #     handle.write(json.dumps(teams_dict))

if __name__ == '__main__':
    main()

