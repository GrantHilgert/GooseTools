#GooseTools Asset to .Obj Converter
major=1
minor=0

import sys
import os
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
import numpy as np
from string import *
import os.path
from os import path


init()

print("GooseTools - Map Asset to OBJ Converter")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")
print("October 2020")








########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################

def get_submesh_count():
    print("get submesh_count PLACEHOLDER")



global submesh_global_name

#Stores 6 Values per Submesh: firstByte, indexCount, topology, baseVertex, firstVertex, vertexCount
global submesh_structure_array

global submesh_center_array
global submesh_extent_array



global submesh_data_array



global submesh_vertex_array
global submesh_normal_array
global submesh_index_array
global submesh_mesh_name_array










########################################################################################################################################
# READ UABE FILE
########################################################################################################################################

map_file = open(sys.argv[1], "r")
MAP_LINE = map_file.readlines()



#Submesh Data Variables
submesh_index=0
submesh_flag=0
center_flag=0
extent_flag=0
parsed_submesh_structure_array_size=0


#Vertex Data Buffer Variables
data_index=0
submesh_data_flag=0
submesh_data_flag=0
parsed_submesh_data_array_size=0


for line in MAP_LINE:


    #Get String name
    if "m_Name" in line:
        submesh_global_name=line.split("=")[1].strip()
        print("Combined Mesh Name: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)    

    #Get buffer and set size
    if "int size" in line and parsed_submesh_structure_array_size == 0:
        
        parsed_submesh_structure_array_size = int(line.split("=")[1].strip())
        submesh_structure_array = np.zeros(parsed_submesh_structure_array_size*6, dtype=int)
        submesh_center_array = np.zeros(parsed_submesh_structure_array_size*3, dtype=float)
        submesh_extent_array = np.zeros(parsed_submesh_structure_array_size*3, dtype=float)


    #Track which Submesh we are on.
    if "0 SubMesh data" in line:
        if submesh_index == 0 and submesh_flag == 1:
            submesh_index+=1
        elif submesh_index > 0 and submesh_flag == 1:
            submesh_index+=1
        elif submesh_index == 0 and submesh_flag == 0:
            submesh_flag = 1

    #for each index
    if "firstByte" in line:
      submesh_structure_array[submesh_index*6] = int(line.split("=")[1].strip())
    if "indexCount" in line:
        submesh_structure_array[submesh_index*6+1] = int(line.split("=")[1].strip())
    if "topology" in line:
      submesh_structure_array[submesh_index*6+2] = int(line.split("=")[1].strip())
    if "baseVertex" in line:
        submesh_structure_array[submesh_index*6+3] = int(line.split("=")[1].strip())
    if "firstVertex" in line:
      submesh_structure_array[submesh_index*6+4] = int(line.split("=")[1].strip())
    if "vertexCount" in line:
        submesh_structure_array[submesh_index*6+5] = int(line.split("=")[1].strip())

    if "m_Center" in line:
        center_flag=1
        extent_flag=0
    if "float x" in line and center_flag == 1:
        submesh_center_array[submesh_index*3] == float(line.split("=")[1].strip())
    if "float y" in line and center_flag == 1:
        submesh_center_array[submesh_index*3+1] == float(line.split("=")[1].strip())
    if "float z" in line and center_flag == 1:
        submesh_center_array[submesh_index*3+2] == float(line.split("=")[1].strip())

    if "m_Extent" in line:
        extent_flag=1
        center_flag=0
    if "float x" in line and center_flag == 1:
        submesh_extent_array[submesh_index*3] == float(line.split("=")[1].strip())
    if "float y" in line and center_flag == 1:
        submesh_extent_array[submesh_index*3+1] == float(line.split("=")[1].strip())
    if "float z" in line and center_flag == 1:
        submesh_extent_array[submesh_index*3+2] == float(line.split("=")[1].strip())

    if "m_IndexBuffer" in line:
        submesh_data_flag=1

    #Get buffer and set size
    if "int size" in line and parsed_submesh_data_array_size == 0 and submesh_data_flag == 1:
        parsed_submesh_data_array_size = int(line.split("=")[1].strip())
        submesh_flag = 0
        submesh_data_array = np.zeros(parsed_submesh_data_array_size, dtype=int)

 
    if "UInt8 data" in line and submesh_data_flag == 1:
        submesh_data_array[data_index] = int(line.split("=")[1].strip())
        data_index+=1





if parsed_submesh_structure_array_size == submesh_index+1:
    print("Submesh Structure: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)  
    print("Submesh Count: "+ Fore.GREEN + str(submesh_index+1) +Style.RESET_ALL)  
else:
    print("Submesh Structure Mismatch: "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)
    print("Submesh Count: "+ Fore.RED + str(submesh_index+1) +Style.RESET_ALL + " == "+ Fore.RED + str(parsed_submesh_structure_array_size) +Style.RESET_ALL )    

if parsed_submesh_data_array_size == data_index:
    print("Submesh Data: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)  
    print("Submesh Count: "+ Fore.GREEN + str(data_index) +Style.RESET_ALL)  
else:
    print("Submesh Data Size Mismatch: "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)
    print("Submesh Data Size: "+ Fore.RED + str(data_index) +Style.RESET_ALL + " == "+ Fore.RED + str(parsed_submesh_data_array_size) +Style.RESET_ALL )    











########################################################################################################################################
#CREATE OBJECT AND MATERIAL FILE
########################################################################################################################################


#Create New Object and Material File
binary_file = open(sys.argv[1].split(".")[0]+".obj", "w")
material_file = open(sys.argv[1].split(".")[0]+".mtl", "w")

#Write Object File Header
binary_file.write("# GooseTools Map Extractor V." + str(major) + "." + str(minor))
binary_file.write("\n# https://github.com/GrantHilgert/GooseTools\n")

#Write Material defintion to Object file
mtllib_file_name=sys.argv[1].split("\\")[len(sys.argv[1].split("\\"))-1].split(".")[0]
binary_file.write("mtllib " + str(mtllib_file_name) + ".mtl\n")




########################################################################################################################################
# BUILD OBJECTS
########################################################################################################################################






submesh_structure_index=0


for object_index in range(submesh_index):
    print("DEBUG - Writting index: " + str(object_index))




















































#Creates a blender friendly material name
def get_material_name(raw_material_data):

    return "ugg_material.00"+ str(material_count_index)

#Returns whether the asset is simple(i.g. Pumpkin) or has bone(i.g. Goose)
def get_asset_type(num_of_vertex, size_of_vertex_buffer):
    
    #Simple Itme without bones/UV
    if (size_of_vertex_buffer/num_of_vertex).is_integer():
        print("Model Structure: "+ Fore.YELLOW + "[SIMPLE]" +Style.RESET_ALL)
        return "simple"
    
    #Goosemesh or NPC
    else:

        #Hard code for now
        #The goose is such
        #40 Bytes * Vertex Count: Vertex + Normals + Unknown Channel
        #12 * Vertex Count: UV + COLOR
        #12 * 1: Some type of name
        #32 * Verted Count: I think bones? No decoded yet

        complex_vertex_buffer_size=40*num_of_vertex
        complex_color_buffer_size=12*num_of_vertex
        complex_bone_buffer_size=32*num_of_vertex
        complex_bone_lable_size=12

        complex_buffer_combined_size=complex_vertex_buffer_size+complex_color_buffer_size+complex_bone_buffer_size+complex_bone_lable_size
        if size_of_vertex_buffer == complex_buffer_combined_size:
            print("Model Structure: "+ Fore.YELLOW + "[COMPLEX]" +Style.RESET_ALL)        
            return "complex"
        

        #This buffer is something else and we cant decode it, throw an error.
        else:
            print("Model Structure: "+ Fore.RED + "[UNKNOWN]" +Style.RESET_ALL) 
            return "fail"



























########################################################################################################################################
#PREPROCESS ASSET
########################################################################################################################################


material_count_index=0
material_count=0
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


bind_pose_buffer=''
bind_pose_flag=0
bind_pose_complete=0

bone_name_hash=""
root_bone_name_hash=""


count=0
#comb through file, line by line
print("Reading File...")
for line in YAML_LINE: 
    #print("Line{}: {}".format(count, line.strip()))
    
    ##############BIND POSE PARSER############
        #Copy Bind Pose Data
    if "m_BindPose:" in line:
        if "m_BindPose: []" in line:
            print("Bind Pose Buffer"+ Fore.YELLOW + "[NO DATA]" +Style.RESET_ALL)           
        else:
            bind_pose_flag=1

    if "m_BoneNameHashes:" in line:
        if len(line.strip().split(":")) > 1:
            bone_name_hash=str(line.strip().split(":")[1]).strip()
            bind_pose_complete=0
            print("Bone Name Hashes: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif bind_pose_flag == 1 and len(line.split(":")) == 1:
            print("Pose Binding Data"+ Fore.RED + "[FAIL]" +Style.RESET_ALL)     

    if "m_RootBoneNameHash:" in line:
        if line.strip().split(":")[1].strip() != str(0):
            root_bone_name_hash=str(line.strip().split(":")[1]).strip()
            print("Root Bone Name Hashes: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)

        else:
            print("Root Bone Name Hashes: "+ Fore.YELLOW + "[NO DATA]" +Style.RESET_ALL)  

    
    #Name of Asset File
    if "m_Name:" in line:
        asset_name=str(line.split(":", maxsplit=1)[1].strip())
        print("Asset Name "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
    
    #Number of Vertexs
    if "m_VertexCount:" in line:
        vertex_count=int(line.split(":", maxsplit=1)[1].strip())
        print("Vertex Count"+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
    

    #index Buffer size
    if "indexCount" in line:
        index_count=int(line.split(":", maxsplit=1)[1].strip())
        print("Index Count"+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
    #Copy Index Buffer
    if "m_IndexBuffer:" in line:
        index_buffer+=str(line.split(":", maxsplit=1)[1].strip())
    
        #Vertex Buffer Size
    if "m_DataSize:" in line:
        vertex_buffer_size=int(line.split(":", maxsplit=1)[1].strip())
    
    #Copy Vertex Buffer 
    if "_typelessdata:" in line:
        vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())
    count+=1    #Copy Vertex Buffer 
    
    #Copy Bind Pose Data
    if "m_BindPose:" in line:
        



        vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())







########################################################################################################################################
#PROCESS ASSET
########################################################################################################################################

















########################################################################################################################################
#PRINT INFO
########################################################################################################################################



print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)

asset_type=get_asset_type(vertex_count,vertex_buffer_size)
if asset_type == "simple":
    vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
    print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
elif asset_type == "complex":
    complex_vertex_buffer_size=40*vertex_count
    complex_color_buffer_size=12*vertex_count
    complex_bone_buffer_size=32*vertex_count
    vertex_buffer_block_size=40
    print("Complex Vertex Buffer Block Size: " +Fore.GREEN+ str(complex_vertex_buffer_size)+Style.RESET_ALL)
    print("Complex Color and UV Buffer Block Size: " +Fore.GREEN+ str(complex_color_buffer_size)+Style.RESET_ALL)
    print("Complex Bone Buffer Block Size: " +Fore.GREEN+ str(complex_bone_buffer_size)+Style.RESET_ALL)

#print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)






########################################################################################################################################
#CREATE OBJECT AND MATERIAL FILE
########################################################################################################################################


#Create New Object and Material File
binary_file = open(sys.argv[1].split(".")[0]+".obj", "w")
material_file = open(sys.argv[1].split(".")[0]+".mtl", "w")

#Write Object File Header
binary_file.write("# GooseTools Model Extractor V." + str(major) + "." + str(minor))
binary_file.write("\n# https://github.com/GrantHilgert/GooseTools\n")



#Write Material defintion to Object file
mtllib_file_name=sys.argv[1].split("\\")[len(sys.argv[1].split("\\"))-1].split(".")[0]
binary_file.write("mtllib " + str(mtllib_file_name) + ".mtl\n")


#bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2+len(index_buffer)+vertex_count*24)
#progress_bar_count=0



byte_count=0



byte_count=0
block_count=0
skip_count=1
count=0



normal_buffer=""


#Write Object Name
binary_file.write("o " + str(asset_name) + "\n")


#Every two bytes. One line in the excel file
word_index=0

#materials
current_material=""
old_material=""
#indexed list of all vertex material data
material_buffer="" 
#List of materials used in the model
material_list=""
material_count=0

data_pos_index="POS X"

#number of bytes to skip until next write
skip_count=0
#Dont write on the same loop
write_flag=0






########################################################################################################################################
#New .OBJ and .MTL Creation Routine 
########################################################################################################################################



#####################
# SIMPLE STRUCTURE
#####################
# 1 Block Total
# Block 1:
# long 1: X
# long 2: Y
# long 3: Z
# long 4: Normal X
# long 5: Normal Y
# long 6: Normal Z
# long 7: Unknown - Why Always 1?
# long 8: Unknown
# long 9: Unknown
# long 10: Unknown - Why Always -1?
# long 12: RED + GREEN + BLUE + "FF"

#####################
# COMPLEX STRUCTURE
#####################
# 3 Blocks Total
#Block 1
# long 1: X
# long 2: Y
# long 3: Z
# long 4: Normal X
# long 5: Normal Y
# long 6: Normal Z
# long 7: Unknown - Why Always 1?
# long 8: Unknown
# long 9: Unknown
# long 10: Unknown - Why Always -1?

#Block 2
# long 1: X
# long 2: Y
# long 3: Z
# long 4: Normal X
# long 5: Normal Y
# long 6: Normal Z
# long 7: Unknown - Why Always 1?
# long 8: Unknown
# long 9: Unknown
# long 10: Unknown - Why Always -1?

#Block 3
# long 1: Unknown
# long 2: Unknown
# long 3: Unknown
# long 4: Unknown
# long 5: Unknown
# long 6: Unknown
# long 7: Unknown
# long 8: Unknown











# SIMPLE OBJECT STATE MACHINE
#POS: Positon
#NORM: Normal
#SKIP: Unknown
#COLOR: COLOR
#USEMTL: MATERIAL



########################################################################################################################################
#Process Colors
########################################################################################################################################
print("DEBUG - SIMPLE COLOR for loop size:" + str(int(vertex_count*vertex_buffer_block_size/4)))
material_buffer_write_count=0
if asset_type == "simple":
    data_pos_index="POS X"
    for long_index in range(int(vertex_count*vertex_buffer_block_size/4)):

        temp_string=""
        #for each byte
        for temp_index in range(8):
            #collect one double from the string
            temp_string+=vertex_buffer[long_index*8+temp_index]
     
            #SKIP the Vertex Data this round
        if data_pos_index.split()[0].strip() =="POS":    
            if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
                data_pos_index="POS Y"

                write_flag=1
            if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:     
                data_pos_index="POS Z"
                write_flag=1
            if data_pos_index.split()[1].strip() =="Z" and write_flag == 0:                     
                data_pos_index="NORM X"
                write_flag=1


                #write the normals instead
        if data_pos_index.split()[0].strip() =="NORM":    
            if data_pos_index.split()[1].strip() =="X" and write_flag == 0:                  
                data_pos_index="NORM Y"
                write_flag=1
            if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:   
                data_pos_index="NORM Z"
                write_flag=1
            if data_pos_index.split()[1].strip() =="Z" and write_flag == 0: 
                data_pos_index="SKIP"
                write_flag=1
        

        if data_pos_index.split()[0].strip() == "SKIP" and write_flag == 0:
            #print("SKIP COUNT BEFORE: " + str(skip_count))
            skip_count+=1
            #print("SKIP COUNT AFTER: " + str(skip_count))
            #print("DEBUG - SKIPPING: " + str(skip_count) + " DATA : " + str(temp_string))        
        if data_pos_index.split()[0] =="SKIP" and skip_count==5 and write_flag == 0:
            #print("COLOR!!!!!")
            data_pos_index="COLOR"
            skip_count=0
            write_flag=1

            #Add Material to buffer
            current_material=str(temp_string)        
            material_buffer+=current_material + " "
            material_buffer_write_count+=1
            if current_material != old_material:
                old_material=current_material
                material_list+=current_material + " "
                print("Found Simple Material"+ Fore.GREEN + "[RAW: " + current_material + " ]" +Style.RESET_ALL)
            data_pos_index="POS X"
        #print(str(data_pos_index) + " : " + str(temp_string))
        write_flag=0


# Th
elif asset_type == "complex":
    data_pos_index="UV X"
    for long_index in range(int(complex_color_buffer_size/4)):
        #print("POS: " + data_pos_index + " : " + str(long_index))
        temp_string=""
        #Create a LONG string from 8 characters
        for temp_index in range(8):
            #collect one double from the string
            temp_string+=vertex_buffer[(int(complex_vertex_buffer_size/4)+long_index)*8+temp_index]

            #SKIP the Vertex Data this round
        if data_pos_index.split()[0].strip() =="UV":    
            if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
                data_pos_index="UV Y"
                write_flag=1
            if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:     
                data_pos_index="COLOR"
                write_flag=1
        if data_pos_index.split()[0].strip() =="COLOR" and write_flag == 0:     

            skip_count=0
            write_flag=1

            #Add Material to buffer
            current_material=str(temp_string)        
            material_buffer+=current_material + " "

            if current_material != old_material:
                old_material=current_material
                material_list+=current_material + " "
                print("Found Complex Material"+ Fore.GREEN + "[RAW: " + current_material + " ]" +Style.RESET_ALL)
            data_pos_index="UV X"

        write_flag=0






#Write Default color if we dont know the structure
else:
    print("FAIL: WRITE DEFAULT COLOR PLACEHOLDER")















########################################################################################################################################
#WRITE VERTEX
########################################################################################################################################


data_pos_index="POS X"

#number of bytes to skip until next write
skip_count=0
#Dont write on the same loop
write_flag=0
#Write Vertex Data and collect material data at the same time to save time
print("VERTEX RANGE: " + str(int(vertex_count*vertex_buffer_block_size/4)))
for long_index in range(int(vertex_count*vertex_buffer_block_size/4)):
    #print("POS: " + data_pos_index)
    #print(str(long_index))
    temp_string=""
    #for each byte
    for temp_index in range(8):
        #collect one double from the string
        temp_string+=vertex_buffer[long_index*8+temp_index]
     
    if data_pos_index.split()[0].strip() =="POS":    
        if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
            binary_file.write("v ")
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write(" ")         
            data_pos_index="POS Y"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write(" ")          
            data_pos_index="POS Z"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Z" and write_flag == 0:          
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write("\n")             
            data_pos_index="NORM X"
            write_flag=1

            #write the normals instead
    if data_pos_index.split()[0].strip() =="NORM":    
        if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
            data_pos_index="NORM Y"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:
            data_pos_index="NORM Z"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Z" and write_flag == 0:     
            data_pos_index="SKIP"
            write_flag=1

    if data_pos_index.split()[0].strip() == "SKIP" and write_flag == 0:
        skip_count+=1
    

    if asset_type == "simple":
        if data_pos_index.split()[0] =="SKIP" and skip_count==5 and write_flag == 0:
            data_pos_index="COLOR"
            skip_count=0
            write_flag=1
            data_pos_index="POS X"
    
    elif asset_type == "complex":
        if data_pos_index.split()[0] =="SKIP" and skip_count==4 and write_flag == 0:
            data_pos_index="COLOR"
            skip_count=0
            write_flag=1
            data_pos_index="POS X"


    write_flag=0
    #print(data_pos_index + str(skip_count))





########################################################################################################################################
#WRITE NORMALS
########################################################################################################################################



#End New Vertex Write and Color Extraction Routine
####################################################################
#Being New Normal Write Routine

#data_pos_index="NORM X" - I think this was a bug. changed to POS X V1.00
data_pos_index="POS X"
#Write Normal Data
normal_offset=12
print("NORMAL RANGE: " + str(int(vertex_count*vertex_buffer_block_size/4)))
for long_index in range(int(vertex_count*vertex_buffer_block_size/4)):
    #print("POS: " + data_pos_index)
    temp_string=""
    #for each byte
    for temp_index in range(8):
        #collect one double from the string
        temp_string+=vertex_buffer[long_index*8+temp_index]
 
        #SKIP the Vertex Data this round
    if data_pos_index.split()[0].strip() =="POS":    
        if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
            data_pos_index="POS Y"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:     
            data_pos_index="POS Z"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Z" and write_flag == 0:                     
            data_pos_index="NORM X"
            write_flag=1


            #write the normals instead
    if data_pos_index.split()[0].strip() =="NORM":    
        if data_pos_index.split()[1].strip() =="X" and write_flag == 0:          
            binary_file.write("vn ")
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write(" ")           
            data_pos_index="NORM Y"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Y" and write_flag == 0:
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write(" ")           
            data_pos_index="NORM Z"
            write_flag=1
        if data_pos_index.split()[1].strip() =="Z" and write_flag == 0:
            binary_file.write(str(round(float(str(struct.unpack('f', bytes.fromhex(temp_string))).strip('(),')),7)))
            binary_file.write("\n")           
            data_pos_index="SKIP"
            write_flag=1
    if data_pos_index.split()[0] =="SKIP" and write_flag == 0:
        skip_count+=1

    if asset_type == "simple":
        if data_pos_index.split()[0] =="SKIP" and skip_count==5 and write_flag == 0:
            data_pos_index="COLOR"
            skip_count=0
            write_flag=1
            data_pos_index="POS X"
    
    elif asset_type == "complex":
        if data_pos_index.split()[0] =="SKIP" and skip_count==4 and write_flag == 0:
            data_pos_index="COLOR"
            skip_count=0
            write_flag=1
            data_pos_index="POS X"

    write_flag=0
        

#End New Normal Write Routine
####################################################################
#Begin Face Write






binary_file.write("g " + str(asset_name) + "_0\n")




current_face_color=""
old_face_color=""

old_material=""
current_material=""


#ver 0.3: Index Buffer is aranged LSB:MSB
#ver 0.1: Face objects strings are reveresed how they appear in the data stream 
#Index Buffer 
index_buffer_count=0
byte_count=0
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

#for item in range(len(material_buffer.split())):
    #print("item " + str(item) + " : "+ material_buffer.split()[item])
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

            #print(str(pos_a)+" "+str(pos_b))
            print("Material Buffer Write Count: " + str(material_buffer_write_count) + " POS A: " + str(pos_a-1))
            if material_buffer.split()[pos_a-1] == material_buffer.split()[pos_b-1]:
                current_material=material_buffer.split()[pos_a-1]
            elif material_buffer.split()[pos_a-1] == material_buffer.split()[pos_c-1]:
                current_material=material_buffer.split()[pos_a-1]
            elif material_buffer.split()[pos_b-1] == material_buffer.split()[pos_c-1]:
                current_material=material_buffer.split()[pos_b-1]
            elif material_buffer.split()[pos_a-1] == material_buffer.split()[pos_c-1]:
                current_material=material_buffer.split()[pos_b-1]                  

            if current_material != old_material:
                old_material=current_material
                material_count_index+=1
                print("Writting Material: "+ Fore.GREEN + "[ "+ current_material + " ]" +Style.RESET_ALL)
                binary_file.write("usemtl " + get_material_name(current_material)+"\n")



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

    #progress_bar_count+=1
    #bar.update(progress_bar_count)









#Write Material FIle

#Write Material File Header
material_file.write("# GooseTools Model Extractor V." + str(major) + "." + str(minor))
material_file.write("\n# https://github.com/GrantHilgert/GooseTools\n")
material_file.write("# Material Count: "+ str(len(material_list.split()))+"\n")
material_file.write("\n")

material_list_duplicate=""

material_count_index=0

print(material_list)
for material_index in range(len(material_list.split())):
    



    kd_red_hex=str(material_list.split()[material_index])[0]+str(material_list.split()[material_index])[1]
    kd_green_hex=str(material_list.split()[material_index])[2]+str(material_list.split()[material_index])[3]
    kd_blue_hex=str(material_list.split()[material_index])[4]+str(material_list.split()[material_index])[5]



    print(kd_red_hex + " " + kd_green_hex + " " + kd_blue_hex)

    kd_red=(int(kd_red_hex,16))/255
    kd_green=(int(kd_green_hex,16))/255
    kd_blue=(int(kd_blue_hex,16))/255
    print(str(kd_red) + " " + str(kd_green) + " " + str(kd_blue))

    material_count_index+=1
    #material_file.write("# Raw Material: "+ str(material_list.split()[material_index])+"\n")
    
    material_file.write("newmtl "+ get_material_name(material_list.split()[material_index]) +"\n")
    material_file.write("Ns 0.000000" +"\n")
    material_file.write("Ka "+ str(format(kd_red,'.6f')) +" "+str(format(kd_green,'.6f')) +" "+ str(format(kd_blue,'.6f'))  +"\n")
    material_file.write("Kd "+ str(format(kd_red,'.6f')) +" "+str(format(kd_green,'.6f')) +" "+ str(format(kd_blue,'.6f'))  +"\n")
    material_file.write("Ks 0.500000 0.500000 0.500000\n")
    material_file.write("Ke 0.000000 0.000000 0.000000\n")
    material_file.write("Ni 1.450000\n")
    material_file.write("d 1.000000\n")
    material_file.write("illum 1\n") 
    material_file.write("\n")

print("Writting .MTL: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)

















binary_file.close        
material_file.close        





#print("Script Complete")
asset_file.close



                

