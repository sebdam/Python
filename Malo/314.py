import argparse

from number_translator_functions import *

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        prog='NumberTranslator',
        description='Translate number from format to another format',
        epilog='Enjoy')
    
    parser.add_argument('number') # first one is the original number
    parser.add_argument('-f', '--format', required=True, choices=['B', 'b', '0b', 'O', 'o', '0o', 'D', 'd', '0d', 'X', 'x', '0x']) # destination format
    
    args = parser.parse_args()
    #print(args.number, args.format, read_number_format(args.number))

    ret = translate(args.number, args.format)
    print(ret)
