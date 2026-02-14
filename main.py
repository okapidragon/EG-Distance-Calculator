import math
from word2number import w2n
from num2words import num2words
global usernamelist, locationlist, distancelist, coordinatelist
eliminated = w2n.word_to_num(input('How many people are getting eliminated this round? '))
roundnumber = w2n.word_to_num(input('Which round number is this? '))
usernamelist = []
locationlist = []
distancelist = []
coordinatelist = []
SLcoordinates = input('Secret location coordinates: ')
SLdecimalplaces = len(str(SLcoordinates).replace("-", ""))/2
def latitudeify(coordinates):
    split_text = coordinates.split(",", 1)
    return split_text[0].strip() if len(split_text) > 1 else coordinates
def longitudeify(coordinates):
    parts = coordinates.split(",", 1)
    if len(parts) > 1:
        return parts[1].strip()
    else:
        return ""
def roundend():
    scoreboard = sorted(zip(usernamelist, locationlist, distancelist, coordinatelist), key=lambda x: x[2])
    eliminatedscoreboard = sorted(scoreboard[-eliminated:], key=lambda x: x[0])
    set_scoreboard = set(eliminatedscoreboard)
    noneliminatedscoreboard = sorted([item for item in scoreboard if item not in set_scoreboard], key=lambda x: x[0])
    print(f"""
Round end message:


These {num2words(eliminated)} people are unfortunately eliminated:""")
    for username, location, distance, coords in eliminatedscoreboard:
        print(f"@{username} - {location} ({coords})")
    print(f"""
These {num2words(len(noneliminatedscoreboard))} people are still in:""")
    for username, location, distance, coords in noneliminatedscoreboard:
        print(f"@{username} - {location} ({coords})")
    print(f"""



Game end message:

Round {word2number(roundnumber)}:
""")
    if roundnumber == 1:
        for username, location, distance, coords in scoreboard:
            print(f"@{username} - {location} ({coords}) **{distance} km**")
    if roundnumber != 1:
        for username, location, distance, coords in scoreboard:
            print(f"{username} - {location} ({coords}) **{distance} km**")
SLlatitude = latitudeify(SLcoordinates)
SLlongitude = longitudeify(SLcoordinates)
def EGgame1():
    def roundend():
        scoreboard = sorted(zip(usernamelist, locationlist, distancelist, coordinatelist), key=lambda x: x[2])
        eliminatedscoreboard = sorted(scoreboard[-eliminated:], key=lambda x: x[0])
        set_scoreboard = set(eliminatedscoreboard)
        noneliminatedscoreboard = sorted([item for item in scoreboard if item not in set_scoreboard], key=lambda x: x[0])
        print(f"""
Round end message:


These {num2words(eliminated)} people are unfortunately eliminated:""")
        for username, location, distance, coords in eliminatedscoreboard:
            print(f"@{username} - {location} ({coords})")
        print(f"""
These {num2words(len(noneliminatedscoreboard))} people are still in:""")
        for username, location, distance, coords in noneliminatedscoreboard:
            print(f"@{username} - {location} ({coords})")
        print("""



Game end message:

Round {word2number(roundnumber)}:
""")
        if roundnumber == 1:
            for username, location, distance, coords in scoreboard:
                print(f"@{username} - {location} ({coords}) **{distance} km**")
        if roundnumber != 1:
            for username, location, distance, coords in scoreboard:
                print(f"{username} - {location} ({coords}) **{distance} km**")
    username = input('Username: ')
    if username.lower() == "end":
        roundend()
        return
    location = input('Guessed location: ')
    guesscoordinates = str(input('Guess coordinates: '))
    guesslatitude = latitudeify(guesscoordinates)
    guesslongitude = longitudeify(guesscoordinates)
    if guesscoordinates.lower() != "end":
        distancekm = round((math.acos(math.sin(math.radians(float(guesslatitude))) * math.sin(math.radians(float(SLlatitude))) + math.cos(math.radians(float(guesslatitude))) * math.cos(math.radians(float(SLlatitude))) * math.cos(math.radians(float(guesslongitude) - float(SLlongitude)))) * 6371), 2)
    usernamelist.append(username)
    locationlist.append(location)
    distancelist.append(distancekm)
    coordinatelist.append(guesscoordinates)
    EGgame1()
EGgame1()
