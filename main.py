# @title:   Image Junk Sniffer
# @author:  Andreas Nagel / KEH IT
# @date:    09/07/2021

# Imports
import sys
import getopt
import json
import csv
import os

# global var
in_data = './input_data/'
out_data = './output_data/'
tmp_data = './tmp_data/'
input_file = ''
output_file = ''
tmp_file = 'tmp_file'
csv_ext = '.csv'
in_data_header = ''
total_files_in = 0
total_json_failed = 0
total_json_repair_failed = 0
total_duplicates = 0
total_missing_repair_values = 0


def main(args):
    get_args(args)
    print('Input file is: ', input_file)
    print('Output file is: ', output_file)
    read_csv(in_data + input_file + csv_ext, "overview")
    if total_duplicates > 0:
        # name of csv file
        filename = tmp_data + tmp_file + csv_ext
        read_csv(filename, 'repair')

    print("Total Incoming Files: {}".format(total_files_in))
    print("Total Json Failed: {}".format(total_json_failed))
    print("Total Duplicates: {}".format(total_duplicates))
    print("Total Repair Json Failed: {}".format(total_json_repair_failed))
    print("Total Repair Missing Values: {}".format(total_missing_repair_values))


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


def read_csv(csv_file, level):
    global total_files_in
    global in_data_header
    # open file in read mode
    with open(csv_file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        in_data_header = next(csv_reader)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            total_files_in = total_files_in + 1
            # row variable is a list that represents a row in csv
            # print(row)
            if level == 'overview':
                filter_overview(row)
            elif level == 'repair':
                repair_img_data(row)


def filter_overview(row):
    global total_json_failed
    global total_duplicates
    # Get only the value[4] label for filtering
    # print("Additional Images Label:{}".format(row[4]))
    try:
        j_value = json.loads(row[4])
    except json.decoder.JSONDecodeError:
        total_json_failed = total_json_failed + 1
        return

    j_add_img_lbl = j_value["additional_images_label"]
    # print("Add Img Label: {}".format(j_add_img_lbl))
    add_img_lbl_list = j_add_img_lbl.split(",")
    print("Add Img Label List: {}".format(add_img_lbl_list))
    if check_if_duplicates(add_img_lbl_list):
        total_duplicates = total_duplicates + 1
        print("Duplicates in List: {}".format("YES"))
        # name of csv file
        filename = tmp_data + tmp_file + csv_ext
        save_tmp_csv(row, filename)


def check_if_duplicates(lst_img):
    """ Check if given list contains any duplicates """
    set_of_elems = set()
    for elem in lst_img:
        if elem in set_of_elems:
            return True
        else:
            set_of_elems.add(elem)
    return False


def save_tmp_csv(row, filename):
    file_exists = os.path.isfile(filename)
    # writing to csv file
    with open(filename, 'a', newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        if not file_exists:
            # use the header from the original img data file.
            csvwriter.writerow(in_data_header)

        # writing the data rows
        csvwriter.writerow(row)


def repair_img_data(row):
    global total_json_repair_failed
    global total_missing_repair_values
    # value is item [4]
    try:
        origin = json.loads(row[4])
    except IndexError:
        total_missing_repair_values = total_missing_repair_values + 1
        return
    except json.decoder.JSONDecodeError:
        total_json_repair_failed = total_json_repair_failed + 1
        return
    # JSON ITEMS: sku, base_image, base_image_label, small_image, small_image_label, thumbnail_image
    # thumbnail_image_label, additional_images, additional_images_label
    # add_img = origin['additional_images'].split(",")
    add_img_lbl = origin['additional_images_label'].split(",")
    repair_additional_images_label(add_img_lbl)


def repair_additional_images(lst):
    pass


def repair_additional_images_label(origin_lst):
    print("Repair Origin List: {}".format(origin_lst))
    unique_lst = remove_duplicates(origin_lst)
    print("Repair Cleaned List #1: {}".format(unique_lst))
    unique_lst = remove_label_01(unique_lst)
    print("Repair Cleaned List #2: {}".format(unique_lst))
    unique_lst = remove_label_empty(unique_lst)
    print("Repair Cleaned List #3: {}".format(unique_lst))
    unique_lst = remove_label_image_x(unique_lst)
    print("Repair Cleaned List #4: {}".format(unique_lst))
    sorted(unique_lst, key=int)
    print("Repair Cleaned List #5: {}".format(unique_lst))


def remove_duplicates(lst):
    """ If given list contains any duplicates, remove and return cleaned list """
    set_of_elems = set()
    for elem in lst:
        if elem not in set_of_elems:
            set_of_elems.add(elem)

    return set_of_elems


def remove_label_01(lst):
    if "01" in lst:
        lst.remove("01")
    return lst


def remove_label_empty(lst):
    if "" in lst:
        lst.remove("")
    return lst


def remove_label_image_x(lst):
    for x in lst:
        if x.startswith("Image"):
            lst.remove(x)
    return lst


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
