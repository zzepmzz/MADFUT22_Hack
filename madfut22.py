#! /usr/bin/env python3

import numpy as np
import sys
import re
import base64

def xor(a, b):
    xored = []
    for i in range(len(a)):
        xored_value = a[i%len(a)] ^ b[i%len(b)]
        xored.append(chr(xored_value))
    return ''.join(xored)

def get_ids_cracked():
    try:
        input_f = open('ids.txt','r')
    except FileNotFoundError:
        print ('ERROR: File ids.txt does not exist')
        sys.exit(1)

    try:
        input_ftotw = open('ids_totw.txt','r')
    except FileNotFoundError:
        print ('ERROR: File ids_totw.txt does not exist')
        sys.exit(1)

    # 1: valencia, 2: buffon, 3: motta, 4: vardy86, 5: vardy92, 6: vardy95, 7: batistuta, 8: silva92, 9: silva93, 10: silva95
    extra = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    id_str = '{'
    for id in extra:
      id_str += '"id'
      id_str += str(id).zfill(3)
      id_str += '":100,'

    for line in input_f:
        id_str += '"id'
        id_str += str(line[:-1])
        id_str += '":100,'

    # In MADFUT22, FUTCHAMP TOTW always end in 00
    for line in input_ftotw:
        id_str += '"id'
        id_str += str(line[:-1])
        id_str += '00'
        id_str += '":100,'

    id_str = id_str[:-1]
    id_str += '}'

    return id_str

if(len(sys.argv) != 2):
    print("ERROR: Need one arg")
    print("Use:",sys.argv[0],"file")
    sys.exit(1)

try:
    input_f = open(sys.argv[1],'r')
except FileNotFoundError:
    print ("ERROR: File '",sys.argv[1],"' does not exist")
    sys.exit(1)

regex_item = re.compile(r'\s*<string\s+name="LwA4">.*')

# XOR key is 0x46644b
xor_key = bytearray([0x46, 0x64, 0x4b])

for line in input_f:
    if regex_item.match(line):
      #print("Found players")
      ids = get_ids_cracked()
      sys.stdout.write('    <string name="LwA4">')
      sys.stdout.write(base64.b64encode(str.encode(xor(str.encode(ids), xor_key))).decode("utf-8"))
      sys.stdout.write('</string>\n')
    else:
      sys.stdout.write(line)
