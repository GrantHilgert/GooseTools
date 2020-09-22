#Untitled Goose Game Asset deconstruction
major=0
minor=1

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar

init()
#open asset file from command line
asset_file = open(sys.argv[1], "r")

YAML_LINE = asset_file.readlines()

asset_name='NA'
index_count='NA'
vertex_count='NA'
index_buffer='NA'
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
        index_buffer=str(line.split(":", maxsplit=1)[1].strip())
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


bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2)
csv_file = open("vertex_test_csv_data.csv", "w")
byte_count=0
block_count=0
count=0
for byte in vertex_buffer:              
    bar.update(count)
    csv_file.write(str(byte))
    byte_count+=1
    block_count+=1
    if byte_count == 4:
        csv_file.write(",")
        byte_count=0
    if block_count == (vertex_buffer_block_size*2):
        csv_file.write("\n")
        block_count=0
    count+=1
print("Ending Byte Count: " + str(byte_count))
print("Ending Block Count: " + str(block_count))
print("Ending Write Count: " + str(count))
csv_file.close               





print("Script Complete")
asset_file.close



                
