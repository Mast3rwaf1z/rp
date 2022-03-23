import sys
import json
import random
import gui
def necromancy():
    window = None
    while True:
        current:dict = getdata()
        c = input("Enter command: ")
        w = open("summons.json", "w")
        if c == "end":
            json.dump(current, w, indent=4)
            w.close()
            sys.exit()
        elif c == "summon":
            c = input("Input summon type: ")
            if c == "z" or c == "zombie":
                c = input("Enter amount of summons: ")
                if len(current["zombies"]) > 0:
                    offset = 1
                else:
                    max = 0
                for i in current["zombies"]:
                    max = offset + int(i)
                for i in range(max, int(c)+max):
                    current["zombies"][i] = 31

            elif c == "s" or c == "skeleton":
                c = input("Enter amount of summons: ")
                if len(current["skeletons"]) > 0:
                    offset = 1
                else:
                    max = 0
                for i in current["skeletons"]:
                    max = offset + int(i)
                for i in range(max, int(c)+max):
                    current["skeletons"][i] = 22
        elif c == "hp":
            Type = input("Enter type of creature: ")
            number = input("To which creature: ")
            change = input("Enter amount of hp change: ")
            current[Type][number] = current[Type][number] + int(change)
        elif c == "reset":
            reset = {"skeletons":{},"zombies":{}}
            current = reset
        elif c == "print":
            print(json.dumps(current, indent=4))
        elif c == "print -table":
            if type(window) == type(None):
                window = gui.table(current)
                window.start()
            else:
                window.setContent(current)
            #gui.display(current)
        elif c == "roll":
            c = input("Enter the type of creature: ")
            rolls = []
            if c == "z":
                count = len(current["zombies"])
                for i in range(count):
                    rolls.append(random.randint(1,20))
                print(rolls)
            elif c == "s":
                count = len(current["skeletons"])
                for i in range(count):
                    rolls.append(random.randint(1,20))
                print(rolls)

        for i in range(len(current["zombies"])):
            try:
                if current["zombies"][str(i)] <= 0:
                    current["zombies"].pop(str(i))
            except:
                pass
        for i in range(len(current["skeletons"])):
            try:
                if current["skeletons"][str(i)] <= 0:
                    current["skeletons"].pop(str(i))
            except:
                pass
        json.dump(current, w, indent = 4)
        w.close()
        if type(window) != type(None):
            #if not window.running:
                #window = None
            #else:
            window.setContent(current)

def getdata() -> dict:
    r = open("summons.json", "r")
    try:
        d = json.load(r)
        r.close()
        return d
    except:
        print("an exception occoured")
        r.close()
        file = open("summons.json", "w")
        d = {"skeletons":{}, "zombies":{}}
        json.dump(d, file, indent=4)
        file.close()
        return d

def main():
    necromancy()

if __name__ == "__main__":
    main()
