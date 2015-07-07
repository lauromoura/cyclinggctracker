import sys
import csv
import glob
import json

longest_stage = 0


# FIXME Implement this.
# Color table for team:
def color_for_team(name):
    pass

def load_stage_file(data, filename):
    global longest_stage
    print "loading", filename
    longest_stage += 1
    with open(filename) as handle:
        current_time = -1
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
            time = map(int, current_time.split(":"))
            time = 3600*time[0] + 60*time[1] + time[2]

            if name not in data:
                data[name] = {"country":country, "team": team, "time": [time]}
            else:
                data[name]["time"].append(time)



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


    # FIXME - Kinda ugly and could be a method.
    # FIXME - Also for partial giro results seems to be missing Nibali (leader) times.
    ordered_data = [] # [(cyclist, times)] # from last to next

    for current_name in data:
        # print "Testing ", current_name, " list size:", len(ordered_data)
        current_times = data[current_name]["time"]
        current_team = data[current_name]["team"]
        current_country = data[current_name]["country"]
        current_stages = len(current_times)

        if not ordered_data:
            ordered_data.append((current_name, current_team, current_country, current_times))
            continue

        for name_in, team_in, country_in, times_in in ordered_data:
            if len(times_in) < current_stages:
                # print current_name, " has ridden ore stages than ", name_in
                continue # Current rider has ridden more stages. Keep going.
            elif len(times_in) == current_stages:
                # check if current rider is behind in the classification
                if times_in[-1] < current_times[-1]:
                    index = ordered_data.index((name_in, team_in, country_in, times_in))
                    ordered_data.insert(index, (current_name, current_team, current_country, current_times))
                    break
                else:
                    continue
            else: #Current rider has ridden less stages and must be inserted
                index = ordered_data.index((name_in, team_in, country_in, times_in))
                ordered_data.insert(index, (current_name, current_team, current_country, current_times))
                break
        else:
            ordered_data.append((current_name, current_team, current_country, current_times))

    #for i in ordered_data:
    #    print i[0]
    #print "sorted"
    #for i in sorted([i[0] for i in ordered_data]):
    #    print i
    print len(ordered_data)


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

        if team not in teams:
            teams.append(team)

        for stage, value in enumerate(times):
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

    # with open("output.csv", "wb") as handle:
    #     csvwriter = csv.writer(handle)
    #     headers = tuple(map((lambda x: "stage %d" % x), range(longest_stage)))
    #     csvwriter.writerow(("Name",)+ headers)
    #     for i, v in enumerate(sorted(data.keys())):
    #         print i, v
    #         print "%s,%s" % (v, ",".join(map(str, data[v]["time"])))
    #         csvwriter.writerow((v,) + tuple(data[v]["time"]))


if __name__ == '__main__':
    main()

