# @title:   Image Junk Sniffer
# @author:  Andreas Nagel / KEH IT
# @date:    09/07/2021

# Imports
import sys
import getopt
import csv

# global var
in_data = './input_data/'
out_data = './output_data/'
input_file = ''
output_file = ''
csv_ext = 'csv'
csv_obj = ''


def main(args):
    get_args(args)


def get_args(argv):
    global input_file
    global output_file

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file)
    print('Output file is "', output_file)


def open_csv():
    pass


def read_csv():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
