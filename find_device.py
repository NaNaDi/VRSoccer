#!/usr/bin/python

## @file
# Contains methods to find the event string of an input device.

# import python libraries
import os
import subprocess
import sys

## Main method for the device search.
def start():

  # this device number should be returned
  _string_num = int(sys.argv[1])

  # name of input device to search is combination of command line parameters
  _name = ""

  for i in range(2, len(sys.argv)):
    _name = _name + " " + sys.argv[i]

  # remove space at the beginning
  _name = _name[2:]

  # search for event number
  print(get_event_string(_string_num, _name))

## Gets the event string of a given input device.
# @param STRING_NUM Integer saying which device occurence should be returned.
# @param DEVICE_NAME Name of the input device to find the event string for.
def get_event_string(STRING_NUM, DEVICE_NAME):

  # file containing all devices with additional information
  device_file = subprocess.Popen(["cat", "/proc/bus/input/devices"], stdout=subprocess.PIPE).communicate()[0]
  device_file = device_file.split("\n")

  # lines in the file matching the device name
  indices = []

  for _i in range(len(device_file)):
    
    _line = device_file[_i]

    if DEVICE_NAME in _line:
      indices.append(_i)

  # if no device was found or the number is too high, return an empty string
  if indices == [] or STRING_NUM > len(indices):
    return ""

  # else captue the event number X of one specific device and return /dev/input/eventX
  else:
    _event_string_start_index = device_file[indices[STRING_NUM-1]+4].find("event")
    return "/dev/input/" + device_file[indices[STRING_NUM-1]+4][_event_string_start_index:].split(" ")[0]



if __name__ == '__main__':
  start()
