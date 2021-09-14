# @title:   Image Junk Sniffer
# @author:  Andreas Nagel / KEH IT
# @date:    09/07/2021

# Imports
import sys
import getopt
import json
import csv
import os
from datetime import datetime
import functools
import re

# global var
in_data = './input_data/'
out_data = './output_data/'
tmp_data = './tmp_data/'
input_file = ''
output_file = ''
tmp_file = 'tmp_file'
csv_ext = '.csv'
in_data_header = ''
cnt_lst_images_label = 0
cnt_lst_images = 0

total_files_in = 0
total_json_failed = 0
total_json_repair_failed = 0
total_duplicates = 0
total_missing_repair_values = 0
log_abbrv = {'tfi': 'Total Files In',
             'tjf': 'Total JSON Failed',
             'tjrf': 'Total JSON Repair Failed',
             'td': 'Total Duplicates',
             'tmrv': 'Total Missing Repair Values',
             'tdcf': 'Total Date Convert Failures',
             'rip': 'Total images remove with parentheses'}
log_sum = {'tfi': 0, 'tjf': 0, 'tjrf': 0, 'td': 0, 'tmrv': 0, 'tdcf': 0, 'rip': 0}


def main(args):
    get_args(args)
    print('Input file is: ', input_file)
    print('Output file is: ', output_file)
    read_csv(in_data + input_file + csv_ext, "overview")
    if log_sum['tfi'] > 0:
        # name of csv file
        filename = tmp_data + tmp_file + csv_ext
        read_csv(filename, 'repair')

    # print(*log_sum, sep="\n")
    print(log_sum)


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
    global log_sum
    global in_data_header
    # open file in read mode
    with open(csv_file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        in_data_header = next(csv_reader)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            log_sum['tfi'] = log_sum['tfi'] + 1
            # row variable is a list that represents a row in csv
            # print(row)
            if level == 'overview':
                filter_overview(row)
            elif level == 'repair':
                repair_img_data(row)


def filter_overview(row):
    global log_sum
    # Get only the value[4] label for filtering
    # print("Additional Images Label:{}".format(row[4]))
    try:
        j_value = json.loads(row[4])
    except json.decoder.JSONDecodeError:
        log_sum['tjf'] = log_sum['tjf'] + 1
        return

    j_add_img_lbl = j_value["additional_images_label"]
    # print("Add Img Label: {}".format(j_add_img_lbl))
    add_img_lbl_list = j_add_img_lbl.split(",")
    print("Add Img Label List: {}".format(add_img_lbl_list))
    if check_if_duplicates(add_img_lbl_list):
        log_sum['td'] = log_sum['td'] + 1
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
    global log_sum
    # value is item [4]
    try:
        origin = json.loads(row[4])
    except IndexError:
        log_sum['tmrv'] = log_sum['tmrv'] + 1
        return
    except json.decoder.JSONDecodeError:
        log_sum['tjrf'] = log_sum['tjrf'] + 1
        return
    # JSON ITEMS: sku, base_image, base_image_label, small_image, small_image_label, thumbnail_image
    # thumbnail_image_label, additional_images, additional_images_label
    add_img_lbl = origin['additional_images_label'].split(",")
    lst_add_img_lbl = repair_additional_images_label(add_img_lbl)
    print("Final Cleaned Additional Images Labels :")
    print(lst_add_img_lbl)
    add_img = origin['additional_images'].split(",")
    lst_add_img = repair_additional_images(add_img, lst_add_img_lbl)
    print("Final Cleaned Additional Images:")
    print(*lst_add_img, sep="\n")
    print("\n#---------End of process-------#\n\n\n")


def repair_additional_images(origin_lst, lbl_lst):
    # print("Repair Additional Images Origin List:")
    # print(*origin_lst, sep="\n")
    unique_lst = remove_duplicates(origin_lst)
    # print("Repair Additional Images Removed Duplicates #1: {}".format(unique_lst))
    unique_lst = remove_image_01(unique_lst)
    # print("Repair Additional Images Removed 01 images #2: {}".format(unique_lst))
    unique_lst = remove_image_media(unique_lst)
    # print("Repair Additional Images Removed media images #3:")
    # print(*unique_lst, sep="\n")
    unique_lst = remove_image_parentheses(unique_lst)
    # print("Repair Additional Images Removed parentheses images #4:")
    # print(*unique_lst, sep="\n")
    unique_lst = remove_image_date(unique_lst)
    # print("Repair Additional Images Removed date images #5:")
    # print(*unique_lst, sep="\n")
    unique_lst = match_images_to_label_count(unique_lst, lbl_lst)
    # print("Repair Additional Images Removed date images #5:")
    # print(*unique_lst, sep="\n")
    return unique_lst


def repair_additional_images_label(origin_lst):
    global cnt_lst_images_label
    # print("Repair Origin List: {}".format(origin_lst))
    unique_lst = remove_duplicates(origin_lst)
    # print("Repair Cleaned List #1: {}".format(unique_lst))
    unique_lst = remove_label_01(unique_lst)
    # print("Repair Cleaned List #2: {}".format(unique_lst))
    unique_lst = remove_label_empty(unique_lst)
    # print("Repair Cleaned List #3: {}".format(unique_lst))
    unique_lst = remove_label_alpha(unique_lst)
    # print("Repair Cleaned List #4: {}".format(unique_lst))
    unique_lst = sorted(unique_lst, key=int)
    # print("Repair Cleaned List #5: {}".format(unique_lst))

    return unique_lst


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


def remove_label_alpha(lst):
    clean_lst = set()
    for x in lst:
        if not x.startswith("Image") \
                and not x.startswith("Top") \
                and not x.startswith("Bottom") \
                and not x.startswith("Right") \
                and not x.startswith("Left") \
                and not x.startswith("Model"):
            clean_lst.add(x)
    return clean_lst


def remove_image_01(lst):
    clean_lst = set()

    for idx, val in enumerate(lst):
        x_lst = val.split("_")
        if len(x_lst) > 1 and not x_lst[1].startswith("01"):
            clean_lst.add(val)

    return clean_lst


def remove_image_media(lst):
    clean_lst = set()

    for idx, val in enumerate(lst):
        x_lst = val.split("_")
        if len(x_lst) > 0:
            try:
                x_lst[0].index("media")
            except ValueError:
                clean_lst.add(val)

    return clean_lst


def remove_image_date(lst):
    global log_sum
    date_obj_lst = set()
    clean_lst = set()

    for idx, val in enumerate(lst):
        # split the string to get the date
        x_lst = val.split("/")
        # idx 5 is the date
        try:
            # try to convert the date string into a date object
            x_date = datetime.strptime(x_lst[5], '%Y-%m-%d').date()
            # print("date object: {}".format(x_date))
        except ValueError:
            # the conversation failed, must be a mal-formatted date or missing date
            log_sum['tdcf'] = log_sum['tdcf'] + 1
            continue
        # if the date object is not in the list, then add it to the list
        if x_date not in date_obj_lst:
            date_obj_lst.add(x_date)

    # print("All diff dates found: {}".format(date_obj_lst))
    # get the newest date from the date_obj_lst
    if len(date_obj_lst) > 0:
        newest_date_obj = functools.reduce(compare_lst, date_obj_lst)
        # print("Newest Date Obj: {}".format(newest_date_obj))
        # convert date object to string
        newest_date_str = newest_date_obj.strftime('%Y-%m-%d')
        # print("Newest Date String: {}".format(newest_date_str))
        for val_1 in lst:
            if val_1.find(newest_date_str) != -1:
                clean_lst.add(val_1)

    return clean_lst


def remove_image_parentheses(lst):
    global log_sum
    clean_lst = set()

    for idx, val in enumerate(lst):
        res = re.search(r'\(', val)
        if res:
            log_sum['rip'] = log_sum['rip'] + 1
        else:
            clean_lst.add(val)

    return clean_lst


def match_images_to_label_count(img_lst, lbl_lst):
    global log_sum
    clean_lst = set()
    clean_lbl_lst = set()
    cnt_lbl_lst = len(lbl_lst)
    cnt_img_lst = len(img_lst)
    seq_lst = ['02', '03', '04', '05', '06', '07', '08']
    # Both list need to have items with numbers in this sequence: 02, 03, 04, 05, 06, 07, 08
    if cnt_img_lst == cnt_lbl_lst:
        # if the list count are equal, nothing to do
        return [img_lst, lbl_lst]
    if cnt_img_lst < 7:
        # if we have less then 7 images, we need to bolster
        for seq in seq_lst:
            pass

    if cnt_lbl_lst < 7:
        # if we have less then 7 labels, we need to bolster
        for seq in seq_lst:
            try:
                lbl_lst.index(seq)
            except ValueError:
                clean_lbl_lst.add(seq)

    return [clean_lst, clean_lbl_lst]


def compare_lst(a, b):
    if a > b:
        return a
    else:
        return b


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
