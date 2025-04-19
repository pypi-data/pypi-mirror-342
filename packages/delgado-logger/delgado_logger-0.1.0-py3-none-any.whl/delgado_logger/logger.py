from inspect import currentframe
from time import strftime, localtime
from os import SEEK_END, SEEK_CUR, listdir, remove, path
from csv import writer as csv_writer
from re import compile as re_compile
from traceback import extract_stack

LOGFILE = "log.txt"
END_SCRIPT = "\n-------------\\  End of Script  /--------------\n\n"
START_SCRIPT = "-------------/ Start of Script \\--------------"


def line_number():
    return currentframe().f_back.f_lineno


def now_date():
    return str(strftime("%m/%d/%Y"))


def date_filename():
    return str(strftime("%Y.%m.%d"))


def now_time():
    return strftime("%I:%M:%S %p %Z", localtime())


def write_to_logfile(log_text: str, log_filename=None):
    if log_filename is None:
        log_filename = LOGFILE
    logfile = open(log_filename, "a")
    stack = extract_stack()
    filename, line_no, function_name, code = stack[-2]
    filename = filename.split("/")[-1].split("\\")[-1]
    if log_text != "":
        log = f"[{now_date()} {now_time()}, {filename}: {line_no}] {log_text} "
    elif log_text == START_SCRIPT:
        log = log_text
    elif log_text == "":
        log = ""
    logfile.write("\n" + log)
    logfile.close()
    print(log)


def error_handler(error: str, line_num: int):
    stack = extract_stack()
    filename, line_no, function_name, code = stack[-2]
    filename = filename.split("/")[-1].split("\\")[-1]
    e = f"  Error [File: {filename} Line: {line_num}] - {error}"
    write_to_logfile(e)
    return e


def engage():
    stack = extract_stack()
    filename, line_no, function_name, code = stack[-2]
    filename = filename.split("/")[-1].split("\\")[-1]
    write_to_logfile(f"Starting Script: {filename}")


def end_of_line():
    stack = extract_stack()
    filename, line_no, function_name, code = stack[-2]
    filename = filename.split("/")[-1].split("\\")[-1]
    write_to_logfile(f"Ending Script: {filename}")


def create_new_output_file(filename: str):
    write_to_logfile('Creating File: "' + filename + '"')
    with open(filename, "w", newline="\n") as file:
        csv_writer(file)


def write_to_file(filename: str, entry: list):
    log_text = f'Writing Data to: "{filename}"'
    if log_text not in last_line_of_file(LOGFILE):
        write_to_logfile(log_text)
    with open(filename, "a", newline="\n") as append_file:
        writer = csv_writer(append_file)
        try:
            writer.writerow(entry)
        except UnicodeEncodeError:
            writer.writerow(["UnicodeEncodeError"])


def last_line_of_file(filename: str):
    with open(filename, "rb") as f:
        try:
            f.seek(-2, SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return str(last_line)


def print_value_info(value):
    stack = extract_stack()
    filename, line_no, function_name, code = stack[-2]
    filename = filename.split("/")[-1].split("\\")[-1]
    vars_name = re_compile(r"\((.*?)\).*$").search(code).groups()[0]
    print(
        f"{vars_name}:\n Type: {type(value)}\n Value = {value}\n Line: {line_no}\n Filename: {filename}"
    )


def remove_old_files(file_extension, directory):
    file_extension = f".{file_extension}"
    file_list = [f for f in listdir(directory) if f.endswith(file_extension)]
    for file in file_list:
        remove(path.join(directory, file))
