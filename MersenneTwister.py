# First define constants to be used throughout Algo
W, N, M, R = 32, 624, 397, 31
A = int("9908B0DF", 16)
U, D = 11, int("FFFFFFFF", 16)
S, B = 7, int("9D2C5680", 16)
T, C = 15, int("EFC60000", 16)
L = 18
F = 1812433253

# returns lowest x bits of num
def lowest_bits(num, x):
    return num & int("F" * int((x/4)), 16)
    
def seed_MT(MT, seed):
    index = N
    MT[0] = seed
    for i in range (1, N, 1):
        intermed = (F * (MT[i-1] ^ (MT[i-1] >> (W-2)) + i))
        MT[i] = lowest_bits(intermed, W) # Lowest W bits of intermediate var

def twist(MT, upper_mask, lower_mask):
    for i in range(N):
        xUpper = (MT[i] & upper_mask)
        xLower = MT[(i+1) % N] & lower_mask
        # x = xUpper concatenated with xLower
        x = (xUpper << R) | xLower

        xA = x >> 1
        if((x % 2) != 0):
            xA = xA ^ A
        
        MT[i] = MT[(i + M) % N] ^ xA
    return 0 # Return new index

def extract_number(MT, index):
    if(index >= N):
        if(index > N):
            print("Error: Generator was never seeded")
        index = twist()

    y = MT[index]
    y = y ^ ((y >> U) & D)
    y = y ^ ((y << S) & B)
    y = y ^ ((y << T) & C)
    y = y ^ (y >> 1)

    index += 1
    return lowest_bits(y, W)


def MersenneTwister(seed):
    MT = [0] * N
    index = N+1
    lower_mask = (1 << R) - 1
    upper_mask = lowest_bits(~lower_mask, W) # Take lowest W bits of not lower mask

    seed_MT(MT, seed)

def main():
    seed = 57
    print(MersenneTwister(seed))

if __name__ == '__main__':
    main()
