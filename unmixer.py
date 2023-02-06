import MersenneTwister
import base64
import random

class unmixer:
    def __init__(self):
        self.W, self.N, self.M, self.R = 32, 624, 397, 31
        self.A = 0x9908B0DF
        self.U, self.D = 11, 0xFFFFFFFF
        self.S, self.B = 7, 0x9D2C5680
        self.T, self.C = 15, 0xEFC60000
        self.L = 18
        self.F = 1812433253

        self.mt = MersenneTwister.MersenneTwister(0)
        self.mt.index = 0

    def int_bits(self, num):
        return int(0xFFFFFFFF & num)

    def bit_ls(self, data, start, stop):
        # Shifts a particular string of bits left by their length
        # Given where the bits start and stop locations, shift the bits left
        # start and stop refer to how many bits away from lsb 

        # Build a string of 1's that will be used to select bits to shift
        # so for start = 1 and stop = 8, we want:
        # 0000 0000 0000 0000 0000 0000 0000 1111 1110
        # We'll build this, then '&' it with data and shift it left by (stop-start)
        length = stop-start
        shifter = 0
        for i in range(length):
            intermed = shifter << 1
            shifter = intermed | 1
        shifter = shifter << start

        cut = data & shifter
        shifted = cut << length
        return shifted

    def bit_rs(self, data, start, stop):
        # Same as ls but shifting righ
        # start and stop now refer to how many bits away from msb
        length = stop-start
        shifter = 0
        for i in range(length):
            intermed = shifter >> 1
            shifter = intermed | 0x80000000
        shifter = shifter >> start

        cut = data & shifter
        shifted = cut >> length
        return shifted

    def test(self, y):
        print("\n(mix)    y: {} - {}".format(hex(y), bin(y)))
        # Mix
        yOrg = y
        y = y ^ ((y >> self.U))
        print("(mix)   s1: {} - {}".format(hex(y), bin(y)))
        y = y ^ ((y << self.S) & self.B)
        print("(mix)   s2: {} - {}".format(hex(y), bin(y)))
        y = y ^ ((y << self.T) & self.C)
        print("(mix)   s3: {} - {}".format(hex(y), bin(y)))
        y = y ^ (y >> self.L)
        print("(mix)   s4: {} - {}".format(hex(y), bin(y)))
        mixed = self.int_bits(y)
        mix64 = base64.b64encode(int.to_bytes(mixed, 4, "big"))
        #print("\nMIXED: {} - {}\nBASE64: {}\n".format(mixed, mix64))
        un64 = int.from_bytes(base64.b64decode(mix64), "big")
        # Notation comes from my drawing/notes where I wrote everything out in steps
        # First get s4, the output of extract number (i.e. after the fourth step)
        s4 = un64
        unmixed = self.unmix_y(s4)

        if(yOrg != unmixed):
            return 1
        return 0

    def unmix_y(self, s4):
        # Next get s3 by reversing s3 ^ (s3 >> self.L)
        s3 = s4 ^ (s4 >> self.L)

        # Get s2 by reversing s2 ^ ((s2 << self.T) & self.C)
        s2_lower = (s3 & 0xFFFF) ^ 0
        s2_30_LSBs = self.bit_ls(s3, 0, self.T)
        s2_30_LSBs = (s3 ^ (s2_30_LSBs & self.C)) & 0x3FFF0000
        s2_30_LSBs = s2_30_LSBs ^ (s3 & 0x3FFF)
        s2_2_MSBs = self.bit_ls(s3, self.T, 2*self.T) & 0xC0000000
        s2_2_MSBs = (s3 ^ (s2_2_MSBs & self.C)) & 0xC0000000
        s2 = s2_2_MSBs | s2_30_LSBs | s2_lower

        # Get s1 by reversing s1 ^ ((s1 << self.S) & self.B)
        s1_lower = s2 & 0x7F
        s1a = (s2 ^ (self.bit_ls(s2, 0, self.S) & self.B)) & 0x3F80
        s1b = (s2 ^ (self.bit_ls(s1a, self.S, 2*self.S) & self.B)) & 0x1FC000
        s1c = (s2 ^ (self.bit_ls(s1b, 2*self.S, 3*self.S) & self.B)) & 0xFE00000
        s1d = (s2 ^ (self.bit_ls(s1c, 3*self.S, 4*self.S) & self.B)) & 0xF0000000
        s1 = s1d | s1c | s1b | s1a | s1_lower

        # Now get y by reversing y ^ (y >> self.U)
        y1 = s1 & 0xFFE00000
        y2 = (s1 ^ self.bit_rs(y1, 0, self.U)) & 0x1FFC00
        y3 = (s1 ^ self.bit_rs(y2, self.U, 2*self.U)) & 0x3FF
        y = y1 | y2 | y3
        # print("(unmix) s4: {} - {}".format(hex(s4), bin(s4)))
        # print("(unmix) s3: {} - {}".format(hex(s3), bin(s3)))
        # print("(unmix) s2: {} - {}".format(hex(s2), bin(s2)))
        # print("(unmix) s1: {} - {}".format(hex(s1), bin(s1)))
        # print("(unmix)  y: {} - {}".format(hex(y), bin(y)))
        return y

    def crack_it(self, victim_tokens):
        # Takes in an array of outputs from victim's MT algorithm, in order
        # Recreates victims initial state of MT array and uses it to predict next value
        # Process each token one at a time
        for i in range(78):
            for j in range(8):
                token_piece = victim_tokens[i][j]
                self.mt.MT[(i*8)+j] = self.unmix_y(token_piece)
        

    def split_nums(self, token_strings):
        # Takes in list of strings, each string containing 8 ints separated by colons (which represents one token)
        # Returns a 2D array with each element being a list containing the 8 ints for each unique token
        tokens = [0] * 78
        for i in range(78):
            strings = token_strings[i].split(':')
            ints = [0] * 8
            for j in range(8):
                ints[j] = int(strings[j])
            tokens[i] = ints
        return tokens


def main():
    # um = unmixer()
    # testval = 0xC4F8D0C2
    # failed = 0
    # um.test(0x73df8ea9)
    # while(failed == 0):
    #     testval = random.getrandbits(32)
    #     failed = um.test(testval)


    successful = 0
    tests = 10
    for x in range(tests):
        seed = int(random.random()*1000)
        mt1 = MersenneTwister.MersenneTwister(seed)

        tokens = [0] * 78
        b64_tokens = [0] * 78
        for i in range(78):
            # Generate token
            token = str(mt1.extract_number())
            for j in range(7):
                token += ":" + str(mt1.extract_number())
            b64_tokens[i] = base64.b64encode(token.encode('utf-8'))

        adv = unmixer()
        # Convert each token to int and add to a diff array
        victim_arr = [0] * 78
        for i in range(78):
            victim_arr[i] = base64.b64decode(b64_tokens[i]).decode('utf-8')
        tokens = adv.split_nums(victim_arr)

        adv.crack_it(tokens)

        neq = 0
        indices = []
        # Now see how many differ
        for i in range(mt1.N):
            if(mt1.MT[i] != adv.mt.MT[i]):
                neq += 1
                indices.append(i)
        #print("Number of MT values not equal between victim and adversary: {}".format(neq))
        #print(indices)

        for i in range(624):
            adv.mt.extract_number()
        new_token = mt1.extract_number()
        adv_guess = adv.mt.extract_number()
        if(new_token == adv_guess):
            print("\nTokens match!!!\nTest #{}".format(x+1))
            print("Victim's next token: {}\nAdversary's 'guess' token: {}\n".format(new_token, adv_guess))
            successful += 1
        
    print("Testing complete! Number of matches: {}\nNumber of Total Tests: {}\nSuccess Rate: {}%".format(successful, tests, 100*round(successful/tests, 4)))
    


if __name__ == '__main__':
    main()
