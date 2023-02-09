import MersenneTwister
import random
import time
import base64

def oracleFunc():
    time.sleep(random.randint(5, 60))
    t = int(time.time())
    print("Seed (to check if cracker was correct): {}\n".format(t))
    mt = MersenneTwister.MersenneTwister(int(t))
    time.sleep(random.randint(5, 60))
    return base64.b64encode(int.to_bytes(mt.extract_number(), 4, "big")).decode("ascii")

def guessRN(rn):
    # Takes b64 encoded output of mersenne twister and tries to guess it
    # Assumption: Test range of 2m05s to 10s before function is called, although function supports longer wait times
    # This range is chose because oracle func waits anywhere from 10s to 2min, add 5 sec to be safe
    t = int(time.time())
    start = t-125 # How far to go back before you start testing times
    stop = t-10 # When to stop testing times
    found = False
    while(found == False):
        for i in range(start, stop):
            mt = MersenneTwister.MersenneTwister(i)
            out = base64.b64encode(int.to_bytes(mt.extract_number(), 4, "big")).decode("ascii")
            if(out == rn):
                print("PRG Cracked!!! Seed: {}".format(i))
                return
        # Set new values of start and stop, going back two minutes at a time
        stop = start-1
        start = start-121
    print("No seed found... D;")

def main():
    rn = oracleFunc()
    guessRN(rn)


if __name__ == '__main__':
    main()

