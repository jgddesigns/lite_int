import random
import unicodedata



class LiteInt:

    symbols = None
    symbol_map = None

    def __init__(self):

        if LiteInt.symbols is None:
            LiteInt.symbols = self.build_symbols()
            LiteInt.symbol_map = {ch: i for i, ch in enumerate(LiteInt.symbols)}

        self.symbols = LiteInt.symbols
        self.symbol_map = LiteInt.symbol_map

        self.symbols = self.build_symbols()
        self.symbol_map =  {ch: i for i, ch in enumerate(self.symbols)}

        self.max_value = 141705

        self.max_slice = 6

        self.original_string = ""

        self.encoded_string = ""

        self.decoded_string = ""

        self.test_size = 4000

        



        self.quick_test()



    # Creates the master list of symbols used to map the data to. Up to six numbers can be turned into 1, using a slice from the original string as a symbol's position in the 141,705 length array . 
    #
    # @return, symbols (list): A list of all symbols used to map the encoding data to. 
    def build_symbols(self):
        symbols = []

        for codepoint in range(0x110000):
            ch = chr(codepoint)
            cat = unicodedata.category(ch)

            if cat in {
                "Cc", "Cf", "Cs", "Co", "Cn",
                "Mn", "Me", "Sk"
            }:
                continue

            if not ch.isprintable():
                continue

            symbols.append(ch)

        self.symbols = symbols

        return symbols


    # Returns a test string. 
    #
    # @return, num (string): A test string based on the current class variable, test_size. 
    def get_data(self):
        num = ""
        while len(num) < self.test_size: 
            num = num + str(random.randint(0, 9))
        return num


    # Compresses an integer into a smaller integer by assigning slices of the number to single symbols from a list of known printable symbols. Checks for the max possible value, and if over, reduces the slice size by 1 then re-checks the size until a symbol can be assigned. 
    #
    # @param, data (integer): An integer number of any length. If not passed, a test integer will be created.
    # @return, self.encoding_string: The full string of the processed encoding. 
    def encode(self, data=None):
        data = data if data else self.get_data()
        while data[0] == "0":
            self.decoded_string = self.decoded_string + "0"
            data = data[1:]
        self.original_string = data
        code = []

        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(data)

        while len(data) > 0:
            length = self.max_slice if len(data) >= self.max_slice else len(data) 
            while length >= 0 and len(data) > 0:
                if int(data[:length]) >= self.max_value:
                    length -= 1
                    continue
                else:
                    code.append(self.symbols[int(data[:length])])
                    data = data[length:]
                    length = 5

        self.encoded_string = "".join(code)

        return self.encoded_string
    

    # Retrieves a symbol's position in the master list. Used to build the decoded string.
    #
    # @param, symbol (string): A single character from the encoded array. 
    # @return (string): The string of the index where the current symbol is stored.  
    def get_number(self, symbol):
        return f"{self.symbol_map[symbol[0]]:05d}"


    # Takes an encoded array and decodes it using the master list. A decoded string is built using each symbol's position in the list.
    #
    # @param, print_on (boolean): Whether or not print statements detailing the decoding results should be printed in the terminal.
    # @return (string): The string of the decoded values.
    def decode(self, code):
        num = ""
        for ch in code:
            num += f"{self.symbol_map[ch]:05d}"
        self.decoded_string = num
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(self.encoded_string)
        return num


    # Compares the original string against the decoded string to see if they match. 
    #
    # @return (boolean): True if a match, False otherwise.
    def compare_data(self):
        return self.original_string == self.decoded_string
    

    # Runs multiple tests to ensure encoding and decoding is successful.  
    #
    # @param (boolean): True if a match, False otherwise.
    # @param (boolean): True if a match, False otherwise.
    # @return (boolean): True if a match, False otherwise.
    def multi_test(self, rounds, test_size=100000):
        passed = 0
        for _ in range(rounds):
            passed += 1 if self.test_run([test_size]) else 0

        print(f"\n\nTested a {test_size} character string {rounds} times. {passed} out of {rounds} matching.")


    def quick_test(self):
        self.encode()
        self.decode(self.encoded_string)
        print(f"\n\n\nTesting a {self.test_size} length integer.")
        print(f"\nIs it a match? {self.compare_data()}\n")


    def test_run(self, sizes=[50000, 50000, 50000, 100000, 100000, 100000], print_on=False):
        self.print_on = print_on
        for test_size in sizes:
            self.test_size = test_size
            self.encode()
            self.decode(self.encoded_string)
            data_match = self.compare_data()
            self.print_on = True
            print(f"\n\nTest Size: {self.test_size} characters") if self.print_on == True else None
            print(f"\nComparison of original vs decoded strings: {str(data_match)}") if self.print_on == True else None
            compression_string = f"{round(((len(self.original_string)-len(self.encoded_string))/len(self.original_string)) * 100)}%" if data_match == True else "None"
            print(f"\nCompression Achieved: {compression_string}") if self.print_on == True else None
            self.print_on = False

            return data_match


LiteInt()