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
csv_ext = '.csv'
csv_obj = ''
total_files_in = 0


def main(args):
    get_args(args)
    print('Input file is: ', input_file)
    print('Output file is: ', output_file)
    read_csv(in_data + input_file + csv_ext)
    print("Total Incoming Files: {}".format(total_files_in))


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


def read_csv(csv_file):
    global total_files_in
    from csv import reader
    # open file in read mode
    with open(csv_file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            total_files_in = total_files_in + 1
            # row variable is a list that represents a row in csv
            print(row)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
