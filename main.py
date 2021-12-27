#!/usr/bin/env python
__author__ = "Big Black Bear Coder / Andreas Nagel / KEH IT"
__copyright__ = "Copyright 2021, Image Junk Snooper"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Big Black Bear Coder"
__email__ = "anagel@keh.com"
__status__ = "Development"
__package__ = "image_junk_snooper"
__github__ = "https://github.com/arnagel/image_junk_snooper.git"

# Imports
import sys
import getopt
import json
import csv
import os
from datetime import datetime
import time
import functools
import re
import pprint

# global var
in_data = './input_data/'
out_data = './output_data/'
review_data = './review_data/'
log_data = './log_data/'
input_file = ''
output_file = ''
log_file = 'log_run_data'
tmp_file = 'tmp_file'
csv_ext = '.csv'
json_ext = '.json'
in_data_header = ''
start_milli_sec = 0

cnt_lst_images_label = 0
cnt_lst_images = 0
total_files_in = 0
total_json_failed = 0
total_json_repair_failed = 0
total_duplicates = 0
total_missing_repair_values = 0

log_abbrv = {
    'ipf': 'Input File Name',
    'opf': 'Output File Name',
    'tfi': 'Total Records to check',
    'tjf': 'Total JSON Convert Failed',
    'tjv': 'Total JSON Values Converted',
    'tjrf': 'Total JSON Repair Failed',
    'td': 'Total Image Duplicates',
    'tmrv': 'Total Missing Values Repaired',
    'tdcf': 'Total File Date Convert Failures',
    'rip': 'Total Images Removed With Parentheses',
    'llb': 'Image Labels Lists Padded',
    'ilb': 'Images  Padded',
    'imau': 'Images Missing All URLS',
    'tcis': 'Total Cleaned Items Saved',
    'msg': 'Message(s)',
    'trt': 'Total Run Time',
    'ril': 'Total Images Removed with Shortcut.lnk',
    'lol': 'Total final items in the combined output list'}
log_sum = {'tfi': 0, 'tjf': 0, 'tjrf': 0, 'td': 0, 'tmrv': 0, 'tdcf': 0, 'rip': 0, 'llb': 0, 'ilb': 0, 'imau': 0,
           'ipf': '', 'opf': '', 'tjv': 0, 'msg': '', 'rdlbl': 0, 'r01lbl': 0, 'reptlbl': 0, 'ralphalbl': 0,
           'tcis': 0, 'trt': 0, 'ril': 0, 'lol': 0}


def main(args):
    global log_sum
    get_run_time(time.time(), False)
    get_args(args)
    log_sum['ipf'] = input_file
    log_sum['opf'] = output_file
    # open the input file and read the content
    lst_input_rows = read_csv(in_data + input_file + csv_ext)

    print(f"Input List: {lst_input_rows}")

    # get the value from the row.
    dir_value = get_value_column(lst_input_rows)
    # filter all values with duplicates, return a list with the duplicates
    lst_dups = filter_duplicates(dir_value)
    # No duplicates, everything is okay
    if log_sum['td'] < 1:
        log_sum['msg'] += '/ No duplicates found, end the process'
        sys.exit()
    # save the duplicates for later review
    file_name = review_data + 'review_' + log_sum['ipf']
    save_json(lst_dups, file_name)
    lst_final_cleaned = []
    # Loop over the list
    for idx, item in enumerate(lst_dups):
        # Clean up base, small, and thumbnail image links.
        lst_dups[idx]['base_image'] = remove_image_with_lnk_ext(item['base_image'])
        lst_dups[idx]['small_image'] = remove_image_with_lnk_ext(item['small_image'])
        lst_dups[idx]['thumbnail_image'] = remove_image_with_lnk_ext(item['thumbnail_image'])
        # remove label duplicates
        lst_clean_add_img_lbl = remove_duplicates(item['additional_images_label'].split(','))
        lst_clean_add_img_lbl = remove_label_01(lst_clean_add_img_lbl)
        lst_clean_add_img_lbl = remove_label_empty(lst_clean_add_img_lbl)
        lst_clean_add_img_lbl = remove_label_alpha(lst_clean_add_img_lbl)
        lst_clean_add_img_lbl = sorted(lst_clean_add_img_lbl, key=int)
        # Convert the list into a comma-delimited string and return to value object'
        item['additional_images_label'] = ",".join(lst_clean_add_img_lbl)
        # Clean the images in additional_images
        lst_clean_add_img = remove_duplicates(item['additional_images'].split(','))
        lst_clean_add_img = remove_image_01(lst_clean_add_img)
        lst_clean_add_img = remove_image_media(lst_clean_add_img)
        lst_clean_add_img = remove_image_parentheses(lst_clean_add_img)
        lst_clean_add_img = remove_image_date(lst_clean_add_img)
        lst_clean_add_img = split_img_diff_skus(lst_clean_add_img)

        if isinstance(lst_clean_add_img, list):
            if len(lst_clean_add_img) < 1:
                continue
        for element in lst_clean_add_img:
            if isinstance(element, list):
                img_lbl_lst = pad_images_to_label_count(element, lst_clean_add_img_lbl)
            else:
                img_lbl_lst = pad_images_to_label_count(lst_clean_add_img, lst_clean_add_img_lbl)

        unique_img_lst = img_lbl_lst[0]
        unique_lbl_lst = img_lbl_lst[1]

        item['additional_images'] = ",".join(unique_img_lst)
        item['additional_images_label'] = ",".join(unique_lbl_lst)
        lst_final_cleaned.append(item)

    lst_final = add_value_column(lst_input_rows, lst_final_cleaned)
    log_sum['tcis'] = len(lst_final)
    lst_final = combine_input_clean_output(lst_input_rows, lst_final)
    save_csv(lst_final, out_data + output_file, in_data_header)
    log_sum['trt'] = get_run_time(time.time(), True)
    handle_log_sum()


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
    # We need to do this, because some of the change_log exports are to big for the memory
    max_int = sys.maxsize
    while True:
        # decrease the max_int value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int / 10)

    global log_sum
    global in_data_header
    # open file in read mode
    with open(csv_file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        in_data_header = next(csv_reader)
        # Iterate over each row in the csv using reader object
        csv_rows = []
        for row in csv_reader:
            csv_rows.append(row)
            log_sum['tfi'] = log_sum['tfi'] + 1

    return csv_rows


def get_value_column(rows):
    global log_sum
    # Get only the value[4] label for filtering
    lst_value_column = []
    for row in rows:
        try:
            lst_value_column.append(json.loads(row[4]))
            log_sum['tjv'] = log_sum['tjv'] + 1
        except json.decoder.JSONDecodeError:
            log_sum['tjf'] = log_sum['tjf'] + 1
            continue

    return lst_value_column


def add_value_column(input_rows, cleaned_rows):
    lst_final = []
    for c_row in cleaned_rows:
        c_sku = c_row['sku']
        set_of_elem = []
        for i_row in input_rows:
            if int(i_row[2]) in set_of_elem:
                continue
            set_of_elem.append(int(i_row[2]))
            if int(i_row[2]) == c_sku:
                x_row = i_row
                x_row[4] = c_row  # replace origin value column content with the cleaned content
                x_row[0] = None  # remove the record id, create new one when import into table
                x_row[5] = None  # remove the record date, create a new date when import into table
                lst_final.append(x_row)

    return lst_final


def filter_duplicates(rows):
    global log_sum
    lst_dups = []
    for row in rows:
        if check_if_duplicates(row["additional_images_label"].split(',')):
            log_sum['td'] = log_sum['td'] + 1
            lst_dups.append(row)

    if len(lst_dups) < 1:
        return False

    return lst_dups


def check_if_duplicates(lst_img):
    """ Check if given list contains any duplicates """
    set_of_elems = set()
    for elem in lst_img:
        if elem in set_of_elems:
            return True
        else:
            set_of_elems.add(elem)
    return False


def save_json(rows, filename):
    file_exists = True
    cnt = 0
    final_file_name = ''
    while file_exists:
        final_file_name = filename + '_' + str(cnt) + json_ext
        file_exists = os.path.isfile(final_file_name)
        cnt = cnt + 1

    with open(final_file_name, 'w') as outfile:
        for row in rows:
            json.dump(row, outfile)


def save_csv(rows, filename, headers):
    file_exists = True
    cnt = 0
    final_file_name = ''
    while file_exists:
        final_file_name = filename + '_' + str(cnt) + csv_ext
        file_exists = os.path.isfile(final_file_name)
        cnt = cnt + 1

    # writing to csv file
    with open(final_file_name, 'a', newline="") as csv_file:
        # creating a csv writer object
        csv_writer = csv.writer(csv_file)
        if headers:
            # use the header from the original img data file.
            csv_writer.writerow(in_data_header)
        # writing the data rows
        for row in rows:
            csv_writer.writerow(row)


def repair_additional_images(origin_lst, lbl_lst):
    unique_lst = remove_duplicates(origin_lst)
    unique_lst = remove_image_01(unique_lst)
    unique_lst = remove_image_media(unique_lst)
    unique_lst = remove_image_parentheses(unique_lst)
    if isinstance(unique_lst, list):
        if len(unique_lst) < 1:
            return False
    else:
        return False
    unique_lst = remove_image_date(unique_lst)
    unique_lst = split_img_diff_skus(unique_lst)

    if isinstance(unique_lst, list):
        if len(unique_lst) < 1:
            sys.exit(10)

    for element in unique_lst:
        if isinstance(element, list):
            img_lbl_lst = pad_images_to_label_count(element, lbl_lst)
        else:
            img_lbl_lst = pad_images_to_label_count(unique_lst, lbl_lst)

    unique_img_lst = img_lbl_lst[0]
    unique_lbl_lst = img_lbl_lst[1]
    return unique_img_lst


def repair_additional_images_label(origin_lst):
    global cnt_lst_images_label
    unique_lst = remove_duplicates(origin_lst)
    unique_lst = remove_label_01(unique_lst)
    unique_lst = remove_label_empty(unique_lst)
    unique_lst = remove_label_alpha(unique_lst)
    unique_lst = sorted(unique_lst, key=int)

    return unique_lst


def remove_duplicates(lst):
    """ If given list contains any duplicates, remove and return cleaned list """
    global log_sum
    set_of_elems = []
    for elem in lst:
        if elem not in set_of_elems:
            set_of_elems.append(elem)
        else:
            log_sum['rdlbl'] = log_sum['rdlbl'] + 1

    return set_of_elems


def remove_label_01(lst):
    global log_sum
    if "01" in lst:
        log_sum['r01lbl'] = log_sum['r01lbl'] + 1
        lst.remove("01")
    return lst


def remove_label_empty(lst):
    global log_sum
    if "" in lst:
        log_sum['reptlbl'] = log_sum['reptlbl'] + 1
        lst.remove("")
    return lst


def remove_label_alpha(lst):
    global log_sum
    clean_lst = []
    for x in lst:
        if not x.startswith("Image") \
                and not x.startswith("Top") \
                and not x.startswith("Bottom") \
                and not x.startswith("Right") \
                and not x.startswith("Left") \
                and not x.startswith("Model") \
                and not x.startswith("Main"):
            clean_lst.append(x)
        else:
            log_sum['ralphalbl'] = log_sum['ralphalbl'] + 1
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
    clean_lst = []

    for idx, val in enumerate(lst):
        # split the string to get the date
        x_lst = val.split("/")
        # idx 5 is the date
        try:
            # try to convert the date string into a date object
            x_date = datetime.strptime(x_lst[5], '%Y-%m-%d').date()
        except ValueError:
            # the conversation failed, must be a mal-formatted date or missing date
            log_sum['tdcf'] = log_sum['tdcf'] + 1
            continue
        # if the date object is not in the list, then add it to the list
        if x_date not in date_obj_lst:
            date_obj_lst.add(x_date)

    # get the newest date from the date_obj_lst
    if len(date_obj_lst) > 0:
        newest_date_obj = functools.reduce(compare_lst, date_obj_lst)
        # convert date object to string
        newest_date_str = newest_date_obj.strftime('%Y-%m-%d')
        for val_1 in lst:
            if val_1.find(newest_date_str) != -1:
                clean_lst.append(val_1)

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


def remove_image_with_lnk_ext(img):
    global log_sum
    res = re.search(r'- Shortcut.lnk', img)
    if res:
        log_sum['ril'] += 1
        pprint.pprint(img)
        img = img.replace(" - Shortcut.lnk", ".jpg", 1)
        pprint.pprint(img)
    return img


def pad_images_to_label_count(img_lst, lbl_lst):
    global log_sum
    clean_img_lst = []
    clean_lbl_lst = []
    cnt_lbl_lst = len(lbl_lst)
    cnt_img_lst = len(img_lst)

    # Both list need to have items with numbers in this sequence: 02, 03, 04, 05, 06, 07, 08
    if cnt_img_lst == cnt_lbl_lst:
        # if the list count are equal, nothing to do
        return [img_lst, lbl_lst]

    if cnt_lbl_lst < 7:
        # if we have less then 7 labels, we need to bolster
        for x in range(2, 9):
            y = "0" + str(x)
            try:
                lbl_lst.index(y)
            except ValueError:
                lbl_lst.append(y)
        log_sum['llb'] = log_sum['llb'] + 1

    if 0 < cnt_img_lst < 7:
        # if we have less then 7 images, we need to bolster
        for x in range(0, len(lbl_lst)):
            x_first = img_lst[0]
            x_lst = x_first.split("_")

            if len(x_lst) > 2:
                x_ext = x_lst[2].split(".")
            else:
                x_ext = x_lst[1].split(".")

            clean_img_lst.append(x_lst[0] + '_' + str(x) + '.' + x_ext[1])
        log_sum['ilb'] = log_sum['ilb'] + 1
    else:
        log_sum['imau'] = log_sum['imau'] + 1
        return [img_lst, lbl_lst]

    return [clean_img_lst, clean_lbl_lst]


def split_img_diff_skus(img_lst):
    clean_lst = []
    clean_img_lst = []
    clean_split_lst = []
    if len(img_lst) > 0:
        x_lst = img_lst[0].split('-')
        y_lst = x_lst[-1].split('_')
        if len(y_lst) > 0:
            sku_model = y_lst[0]
        else:
            return img_lst
    else:
        return img_lst

    for img_url in img_lst:
        if img_url.find(sku_model) == -1:
            clean_split_lst.append(img_url)
        else:
            clean_img_lst.append(img_url)

    if len(clean_split_lst) > 0:
        clean_lst.append(clean_img_lst)
        clean_lst.append(clean_split_lst)
        return clean_lst

    return clean_img_lst


def compare_lst(a, b):
    if a > b:
        return a
    else:
        return b


def get_run_time(ti, end):
    global start_milli_sec
    if not end:
        start_milli_sec = ti
    else:
        return '{:.2f}'.format((ti - start_milli_sec))


def handle_log_sum():
    # save log sum to file
    # print log sum to screen
    cnt = 1
    lst_save = []
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    file_name = log_data + log_file + date_time
    for key, value in log_abbrv.items():
        print("{}.) {}: {}".format(cnt, value, log_sum[key]))
        cnt += 1
        lst_save.append(value + ': ' + str(log_sum[key]))

    lst_out = [",".join(lst_save)]
    save_json(lst_out, file_name)


def combine_input_clean_output(lst_input, lst_clean) -> list:
    lst_out = []
    for idx, img_rec in enumerate(lst_input):
        ref_key = int(img_rec[2])  # get the ref key from the image record
        flag = 0  # set/rest flag
        for idx_clean, img_rec_clean in enumerate(lst_clean):
            # print(f"Img Rec Clean: {img_rec_clean}")
            ref_key_clean = int(img_rec_clean[2])  # get the ref key from the image record
            if ref_key == ref_key_clean:
                flag = 1 # if the input record is in the clean list set flag
        if flag == 0:  # if the input record is not in the clean list add to the output
            img_rec[0] = None
            img_rec[5] = None
            lst_out.append(img_rec)
    lst_out.extend(lst_clean)
    print(f"List input Len: {len(lst_input)}")
    print(f"List clean Len: {len(lst_clean)}")
    print(f"List out Len: {len(lst_out)}")
    log_sum['lol'] = len(lst_out)
    return lst_out


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
