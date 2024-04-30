#!/usr/bin/python3
import argparse
import struct
import sys
import os
from re import match as regexmatch

def main ():
  parser = argparse.ArgumentParser(description='Convert Snap TPM-FDE recovery key to LUKS key-file.')
  parser.add_argument('-o','--outfile', dest='outfile', default='./key.out', help='Path to the raw key-file generated.')
  parser.add_argument('--stdout', dest='stdout', action='store_true', default=False, help='Print key to stdout instead of writing to a file.')
  recovery_string = parser.add_mutually_exclusive_group(required=True)
  recovery_string.add_argument('-s', '--string', dest='string', help='The Snapd TPM-FDE recovery-key string to convert.')
  recovery_string.add_argument('-i', '--infile', dest='infile', help='The path to a file containing your recovery-key string.')
  cmdline = parser.parse_args()
  
  if cmdline.string:
    vd_string = validate_string(cmdline.string)
  elif cmdline.infile:
    vd_string = validate_string(extract_key_string(cmdline.infile))
  else:
    sys.exit('Unknown error while retrieving the recovery key string')
  
  fmt_string = format_string(vd_string)

  if cmdline.stdout:
    stdout_key(fmt_string)
  else:
    write_key(fmt_string, cmdline.outfile)

def extract_key_string(path):
  if os.path.isfile(path):
    with open(path, 'r') as keyfile:
      recovery_key_string = keyfile.readline()
    return recovery_key_string
  else:
    sys.exit(f"File, {path}, not found.")

def validate_string (recovery_string):
  # Accept formatted recovery keys containing '-' characters
  s = str.replace(recovery_string,'-','')
  # Strip whitespace
  s = s.strip()
  # Validate string length
  if len(s) != 40:
    sys.exit('Recovery string is not exactly 40 digits.')
  # Validate string content
  if not regexmatch('[0-9]', s):
    sys.exit('Recovery string should only contain numbers.')
  return s

def format_string (stripped_recovery_string):
  chunk_len = int(len(stripped_recovery_string)/8)
  key_array = []
  for i in range(0, len(stripped_recovery_string), chunk_len):
    key_array.append(int(stripped_recovery_string[i : i + chunk_len]))
  return key_array

def stdout_key (key_array):
  # Write each number as UInt16 Little-Endian binary to a file
  for i in key_array:
    packed_data = struct.pack('<H', i)
    print(packed_data, end='')

def write_key (key_array, outfile):
  realpath = os.path.realpath(outfile)
  with open(realpath, 'wb') as keyfile:
    # Write each number as UInt16 Little-Endian binary to a file
    for i in key_array:
      packed_data = struct.pack('<H', i)
      keyfile.write(packed_data)
      
main()