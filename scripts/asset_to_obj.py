#GooseTools Asset to .Obj Converter
major=0
minor=3

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
from string import *

init()

print("Untitled Goose Game Asset to OBJ converter")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")




#open asset file from command line
asset_file = open(sys.argv[1], "r")

YAML_LINE = asset_file.readlines()

asset_name='NA'
index_count='NA'
vertex_count='NA'
index_buffer=''
vertex_buffer='NA'
vertex_buffer_size='NA'
vertex_buffer_block_size='NA'

count=0
#comb through file, line by line
print("Reading File...")
for line in YAML_LINE: 
    #print("Line{}: {}".format(count, line.strip()))
    if "m_Name:" in line:
        asset_name=str(line.split(":", maxsplit=1)[1].strip())
    if "m_VertexCount:" in line:
        vertex_count=int(line.split(":", maxsplit=1)[1].strip())
    if "indexCount" in line:
        index_count=int(line.split(":", maxsplit=1)[1].strip())
    if "m_IndexBuffer:" in line:
        index_buffer+=str(line.split(":", maxsplit=1)[1].strip())
    if "m_DataSize:" in line:
        vertex_buffer_size=int(line.split(":", maxsplit=1)[1].strip())
    if "_typelessdata:" in line:
        vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())
    count+=1

print("Extracted Header")
print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)
vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
print("Raw Buffers")
print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)



binary_file = open("temp_obj.obj", "w")
bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2+len(index_buffer)+vertex_count*24)
progress_bar_count=0
byte_count=0



byte_count=0
block_count=0
skip_count=1
count=0

normal_buffer=""
binary_file.write("g " + str(asset_name) + "\n")
binary_file.write("v ")
cycles=0
hex_string=''
for byte in vertex_buffer:
    #binary_file.write("Byte: " + str(byte_count) + " block: " + str(block_count)+ " skip: "+str(skip_count)+"\n")
    byte_count+=1
    block_count+=1
    cycles+=1
    #Vertex Data 
    if skip_count < 4:
        hex_string+=str(byte)
        if byte_count == 8:
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(hex_string))).strip('(),')),7)))
            binary_file.write(" ")
            hex_string=''
            byte_count=0
            skip_count+=1
            
    elif skip_count > 6 and skip_count < 13:
        normal_buffer+=str(byte)
        if byte_count == 4:
            #binary_file.write("\n")
            byte_count=0
            skip_count+=1            
    else:
        if byte_count == 4:
            #binary_file.write("\n")
            byte_count=0
            skip_count+=1
        if block_count == (vertex_buffer_block_size*2):
            #binary_file.write("\n")
            binary_file.write("\n")
            if cycles < len(vertex_buffer):
                binary_file.write("v ")
            block_count=0
            skip_count=1
            

    count+=1
    progress_bar_count+=1
    bar.update(progress_bar_count)
print("Ending Byte Count: " + str(byte_count))
print("Ending Block Count: " + str(block_count))
print("Ending Write Count: " + str(count))



cycles=0
byte_count=0
hex_string=''
binary_file.write("vn ")
for byte in normal_buffer:

    progress_bar_count+=1
    bar.update(progress_bar_count)
    cycles+=1
    byte_count+=1
    block_count+=1
    hex_string+=str(byte)
    #binary_file.write(str(byte))
    if byte_count == 8:
        #print(str(hex_string))
        binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(hex_string))).strip('(),')),7)))
        binary_file.write(" ")
        hex_string=''
        byte_count=0
    if block_count == 24:
        #binary_file.write("\n")
        block_count=0
        binary_file.write("\n")
        if cycles < len(normal_buffer):
            binary_file.write("vn ")





binary_file.write("g " + str(asset_name) + "_0\n")



#ver 0.3: Index Buffer is aranged LSB:MSB
#ver 0.1: Face objects strings are reveresed how they appear in the data stream 
#Index Buffer 
index_buffer_count=0
byte_cou=nt=0
pos_a_r=''
pos_b_r=''
pos_c_r=''

#MSB
pos_a_msb=''
pos_b_msb=''
pos_c_msb=''
#LSB
pos_a_lsb=''
pos_b_lsb=''
pos_c_lsb=''




pos_a=''
pos_b=''
pos_c=''

skip_first_word=1
for byte in index_buffer:
    byte_count+=1
    index_buffer_count+=1
    #print("Byte: " + str(byte_count) + " block: " + str(block_count)+ " skip: "+str(skip_count)+"\n")
    if byte_count == 4 and skip_first_word == 0:
        skip_first_word = 1
        byte_count=0

    if skip_first_word == 1:
        if byte_count > 0 and byte_count < 5:
            #POS A
            #print("POS A: " + byte)
            if byte_count > 0 and byte_count < 3:
                pos_a_lsb+=str(byte)
            elif byte_count > 2 and byte_count < 5:
                pos_a_msb+=str(byte)
            else:
                print("INDEX BUFFER PARSE ERROR A: " + str(byte) + " Count: " + str(index_buffer_count))
        elif byte_count > 4 and byte_count < 9:
            #POS B
            #print("POS B: " + byte)
            if byte_count > 4 and byte_count < 7:
                pos_b_lsb+=str(byte)
            elif byte_count > 6 and byte_count < 9:
                pos_b_msb+=str(byte)
            else:
                print("INDEX BUFFER PARSE ERROR B: " + str(byte) + " Count: " + str(index_buffer_count))
        elif byte_count > 8 and byte_count < 13:
            #POS C
            #print("POS C: " + byte)
            if byte_count > 8 and byte_count < 11:
                pos_c_lsb+=str(byte)
            elif byte_count > 10 and byte_count < 13:
                pos_c_msb+=str(byte)
            else:
                print("INDEX BUFFER PARSE ERROR C: " + str(byte) + " Count: " + str(index_buffer_count))
        if byte_count == 12:
            byte_count=0

            #print("Index: " + str(index_buffer_count))
            #print("A MSB: " + str(pos_a_msb) + "  LSB: " + str(pos_a_lsb) + "  COMBINDED: " + str(pos_a_msb + pos_a_lsb) + "  INT: " + str(int(str(pos_a_msb + pos_a_lsb),16)))
            #print("B MSB: " + str(pos_b_msb) + "  LSB: " + str(pos_b_lsb) + "  COMBINDED: " + str(pos_b_msb + pos_a_lsb) + "  INT: " + str(int(str(pos_a_msb + pos_a_lsb),16)))
            #print("C MSB: " + str(pos_b_msb) + "  LSB: " + str(pos_b_lsb) + "  COMBINDED: " + str(pos_b_msb + pos_a_lsb) + "  INT: " + str(int(str(pos_a_msb + pos_a_lsb),16)))
            pos_a=int((pos_a_msb+pos_a_lsb),16)+1
            pos_b=int((pos_b_msb+pos_b_lsb),16)+1
            pos_c=int((pos_c_msb+pos_c_lsb),16)+1





            #invert face object order
            binary_file.write("f " +str(pos_c)+"/"+str(pos_c)+"/"+str(pos_c)+" "+str(pos_b)+"/"+str(pos_b)+"/"+str(pos_b)+" "+str(pos_a)+"/"+str(pos_a)+"/"+str(pos_a))
            binary_file.write("\n")
            #Clear Buffers
            pos_a_r=''
            pos_b_r=''
            pos_c_r=''
            #MSB
            pos_a_msb=''
            pos_b_msb=''
            pos_c_msb=''
            #LSB
            pos_a_lsb=''
            pos_b_lsb=''
            pos_c_lsb=''

    progress_bar_count+=1
    bar.update(progress_bar_count)




binary_file.close               





print("Script Complete")
asset_file.close



                

