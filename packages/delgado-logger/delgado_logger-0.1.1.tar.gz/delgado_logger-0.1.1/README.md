# Delgado Logger

A human-readable, lightweight logging utility for Python. Designed for quick integration and debugging ease with time-stamped log entries and error tracking

## Features

- Timestamped logs
- Human-readable file logging
- Error logging with file and line reference
- Automatic script start/end messages
- Utility to inspect variable values
- Clean-up utility for old files

## Installation

To install via pip (once uploaded to PyPI):

```bash
pip install delgado_logger
```

## Usage

Below is a quick reference table of all available functions in the `delgado_logger` module:

| Function Name         | Description                                                 |
|-----------------------|-------------------------------------------------------------|
| `line_number()`       | Returns the current line number in the script.              |
| `now_date()`          | Returns current date in MM/DD/YYYY format.                  |
| `date_filename()`     | Returns date formatted as `YYYY.MM.DD` for filenames.       |
| `now_time()`          | Returns the current time in HH:MM:SS AM/PM TIMEZONE format. |
| `write_to_logfile(log_text, log_filename=None)` | Appends a log entry to the specified log file.              |
| `error_handler(error, line_num)` | Logs an error message with file and line number.            |
| `engage()`            | Logs the start of the script.                               |
| `end_of_line()`       | Logs the end of the script.                                 |
| `create_new_output_file(filename)` | Creates a new file and logs the action.                 |
| `write_to_file(filename, entry)` | Appends a row (`list`) to a file and logs it.           |
| `last_line_of_file(filename)` | Returns the last line from a given file.                    |
| `print_value_info(value)` | Prints type, value, line number, and filename of a variable. |
| `remove_old_files(file_extension, directory)` | Deletes files with the given extension in a directory.      |

To utilize a function in this module, you must first import it into your project
```python
import delgado_logger
```

## Examples:

### line_number()
Use:
```python
print(delgado_logger.line_number())
```
Output:
```
3
```
---
### now_date()
Use:
```python
print(delgado_logger.now_date())
```
Output:
```
04/17/2025
```
---
### now_time()
Use:
```python
print(delgado_logger.now_time())
```
Output:
```
06:52:39 PM Pacific Daylight Time
```
---
### date_filename()
This is intended for use to concatinate a filename for output.
In this example, I'm adding `.filename.ext` to the date_filename() output.
Use:
```python
print(f"{delgado_logger.date_filename()}.filename.ext")
```
Output:
```
2025.04.17.filename.ext
```
---
### write_to_logfile()
By default, this will write a specified string to `log.txt`, 
however if you specify the `log_filename` variable, you can output 
to a specific txt file instead.

Default Use:
```python
delgado_logger.write_to_logfile('Some Text Here')
```
Output:
```
[04/17/2025 07:00:21 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
```
In addition to the console output, it will append the log file,
or create the log file and add this as the first contents.

Here is an example log.txt after running my test script twice
```

[04/17/2025 07:00:21 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
[04/17/2025 07:03:17 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
```
If you would like to output your text to a different log file, modify the command like this
```python
delgado_logger.write_to_logfile('Some Text Here', log_filename='tester_log.txt')
```
---
### error_handler()
This requires you to supply the error text and line number. 
You can use the line_number() function to supply the line number dynamically.
This will both print to the terminal and output to the logfile.
Use:
```python
delgado_logger.error_handler('Some Error Text', delgado_logger.line_number())
```
Terminal Output
```
[04/17/2025 07:10:07 PM Pacific Daylight Time, logger.py: 52]   Error [File: tester.py Line: 15] - Some Error Text 
```
Example Log.txt contents after an error:
```
[04/17/2025 07:07:04 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
[04/17/2025 07:07:04 PM Pacific Daylight Time, logger.py: 52]   Error [File: tester.py Line: 15] - Some Error Text 
[04/17/2025 07:08:34 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
[04/17/2025 07:10:07 PM Pacific Daylight Time, tester.py: 11] Some Text Here 
[04/17/2025 07:10:07 PM Pacific Daylight Time, logger.py: 52]   Error [File: tester.py Line: 15] - Some Error Text 
```
---
### engage()
This will append to the log file that the file running has started. 
This will not print to the terminal that the file has started.

Use:
```python
delgado_logger.engage()
```
Output:
```
[04/17/2025 07:12:10 PM Pacific Daylight Time, logger.py: 60] Starting Script: tester.py 
```
---
### end_of_line()
Use:
```python
delgado_logger.end_of_line()
```
Output:
```
[04/18/2025 12:12:50 AM Pacific Daylight Time, logger.py: 67] Ending Script: tester.py ```
```
---
### create_new_output_file(filename)
Creates a file with a specified filename.
Use:
```python
delgado_logger.create_new_output_file('Test.txt')
```
Output:
```
[04/18/2025 12:16:05 AM Pacific Daylight Time, logger.py: 71] Creating File: "Test.txt" 
```
---
### delgado_logger.write_to_file()
This allows you to write to any txt/csv file (maybe others). 
You feed it an array, and it will be written as a single line 
with CSV formatting.
Use:
```python
some_content = ['test1', 'test2', 'test3']
delgado_logger.write_to_file('Test.txt', some_content)
```
Console Output:
```
[04/18/2025 12:24:03 AM Pacific Daylight Time, logger.py: 79] Writing Data to: "Test.txt" 
```
Test.txt File Contents:
```
test1,test2,test3
```
---
### last_line_of_file()
This will return the last line of a given txt or CSV file (may work on other formats too, but untested)

Use:
```python
print(f'{delgado_logger.last_line_of_file("Test.txt")}')
```
Output:
```
test1,test2,test3
```
---
### print_value_info()
This will print out some helpful information about a specified variable

Use:
```python
dict_example = {'tst': 'test'}
array_example = ['test1', 'test2']
string_example = 'Testing String'
int_example = 1

delgado_logger.print_value_info(dict_example)
delgado_logger.print_value_info(array_example)
delgado_logger.print_value_info(string_example)
delgado_logger.print_value_info(int_example)
```
Output:
```
dict_example:
 Type: <class 'dict'>
 Value = {'tst': 'test'}
 Line: 32
 Filename: tester.py
array_example:
 Type: <class 'list'>
 Value = ['test1', 'test2']
 Line: 33
 Filename: tester.py
string_example:
 Type: <class 'str'>
 Value = Testing String
 Line: 34
 Filename: tester.py
int_example:
 Type: <class 'int'>
 Value = 1
 Line: 35
 Filename: tester.py

Process finished with exit code 0

```
---
### remove_old_files(file_extension, directory)
This will remove all files of a given file extension within a specified directory.
No output on console or file for this, it's intended purpose is to help clean up
after testing. In this example, we're deleting all the .txt files within the `./old_files/` subdirectory

Use:
```python
delgado_logger.remove_old_files('txt', './old_files/')
```