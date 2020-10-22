#GooseTool's Complex Collada Generator
major=1
minor=0

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
from string import *
from datetime import date
import numpy as np
import subprocess
#Init Colorama
init()

print("GooseTool's Collada to Asset")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")
print("October 2020")


today = date.today()




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
# long 1: UV
# long 2: UV
# long 3: RED + GREEN + BLUE + "FF"

#Block 3
# long 1: BONE 1 WEIGHT
# long 2: BONE 2 WEIGHT
# long 3: BONE 3 WEIGHT
# long 4: BONE 4 WEIGHT
# long 5: BONE 1 INDEX
# long 6: BONE 2 INDEX
# long 7: BONE 3 INDEX
# long 8: BONE 4 INDEX



########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################

def float_to_hex(f):

    data_double=str(hex(struct.unpack('<I', struct.pack('<f', f))[0])).split('x')[1]

    #print(Fore.CYAN +"DEBUG - ORIGINAL: " + str(f) + " UNPACKED: " + str(data_double))
    if f==0:
        output_data="00000000"
    else:
        #print("Double: " + str(data_double))
        data_word_H=str(data_double[:4])
        data_word_L=str(data_double[-4:])
        #print("Word H: " + str(data_word_H))
        #print("WORD L: " + str(data_word_L))
        data_byte1=str(data_word_L[-2:])
        data_byte2=str(data_word_L[:2])
        data_byte3=str(data_word_H[-2:])
        data_byte4=str(data_word_H[:2])
        output_data=data_byte1+data_byte2+data_byte3+data_byte4
    #print(Fore.CYAN +"DEBUG - ORIGINAL: " + str(f) + " UNPACKED: " + str(data_double) + " OUTPUT: "  +str(output_data))
    if len(output_data) < 8:
        print("FLOAT ERROR")
    return output_data














########################################################################################################################################
# Read .DAE File
########################################################################################################################################



collada_file = open(sys.argv[1], "r")

COLLADA_LINE = collada_file.readlines()


global position_buffer
global position_buffer_size
position_buffer_size=0

global normal_buffer
global normal_buffer_size
normal_buffer_size=0

global color_buffer
global color_buffer_size
color_buffer_size=0

global index_buffer
global index_buffer_size
index_buffer_size=0

global face_index_count
face_index_count=0
global face_index_max
face_index_max=0

global face_buffer
global face_buffer_size

face_buffer_size=0


global bind_pose_buffer
global bind_pose_buffer_size
bind_pose_buffer_size=0

global bone_weight_buffer
global bone_weight_buffer_size
bone_weight_buffer_size=0

global bone_weight_index_buffer
global bone_weight_index_size
bone_weight_index_size=0

global weight_index_count
weight_index_count=0
global weight_index_max
weight_index_max=0


global bone_name_buffer
global bone_name_hash

global joint_weight_count_buffer
global joint_index_buffer
global vertex_weight_count
vertex_weight_count=0



bone_name_array=""
bone_count=0

global asset_name
global center_x
global center_y
global center_z


center_x=0
center_y=0
center_z =0




global extent_x
global extent_y
global entent_z

extent_x=0
extent_y=0
extent_z=0

global vertex_count
global index_count
index_count=0
#bind_matrix=np.zeros(shape=(4,4), dtype=float)


#flags
lib_geometries_flag=0
mesh_position_flag=0
mesh_normal_flag=0
mesh_color_flag=0
mesh_face_flag=0

lib_controller_flag=0
bind_pose_flag=0
vertex_weight_flag=0
joint_flag=0

asset_name="N/A"


#comb through file, line by line
print("Reading Mesh File...")
for line in COLLADA_LINE: 

    #print("line")

    if "<geometry id=" in line:
        asset_name=line.split("name=")[1].split(">")[0].strip("\"")
        print("Asset Name: "+ Fore.GREEN + str(asset_name) +Style.RESET_ALL)  


    #Mesh Positions
    elif ("<source id=" in line) and ("-positions" in line):
        mesh_position_flag=1

    elif ("<float_array id=" in line) and (mesh_position_flag == 1):
        position_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        temp_buffer=line.split(">")[1].split("<")[0].split()
        print("Position Buffer Size: "+ Fore.GREEN  +str(position_buffer_size) +Style.RESET_ALL)
        position_buffer=np.zeros(position_buffer_size, dtype=float)
        for index in range(position_buffer_size):
            position_buffer[index]=float(temp_buffer[index])
        print("Extracted Position Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        mesh_position_flag=0

    #Mesh Normals
    elif ("<source id=" in line) and ("-normals" in line):
        mesh_normal_flag=1

    elif ("<float_array id=" in line) and (mesh_normal_flag == 1):

        normal_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        temp_buffer=line.split(">")[1].split("<")[0].split()
        print("Normal Buffer Size: "+ Fore.GREEN  +str(normal_buffer_size)+Style.RESET_ALL)
        normal_buffer=np.zeros(normal_buffer_size, dtype=float)
        for index in range(normal_buffer_size):
            normal_buffer[index]=float(temp_buffer[index])
        print("Extracted Normal Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        mesh_normal_flag=0

    #Mesh Colors
    elif ("<source id=" in line) and ("-colors" in line):
        mesh_color_flag=1

    elif ("<float_array id=" in line) and (mesh_color_flag == 1):
        color_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        temp_buffer=line.split(">")[1].split("<")[0].split()
        print("Color Buffer Size: "+ Fore.GREEN  +str(color_buffer_size) +Style.RESET_ALL)
        color_buffer=np.zeros(color_buffer_size, dtype=float)
        for index in range(color_buffer_size):
            color_buffer[index]=float(temp_buffer[index])
        print("Extracted Color Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        mesh_color_flag=0


    #Faces
    elif ("<vertices id=" in line) and ("-vertices" in line):
        mesh_face_flag=1

    elif ("triangles material=" in line) and (mesh_face_flag == 1):
        face_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        print("Face Buffer Size: "+ Fore.GREEN  +str(face_buffer_size) +Style.RESET_ALL)


    elif ("<p>" in line) and (mesh_face_flag == 1):       
        temp_buffer=line.split("<p>")[1].split("</p>")[0].split()
        face_index_count=len(temp_buffer)
        face_buffer=np.zeros(face_index_count, dtype=int)
        for index in range(face_index_count):
            face_buffer[index]=int(temp_buffer[index])
            if face_buffer[index] > face_index_max:
            	face_index_max=face_buffer[index]
        print("Extracted Face Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        print("Number of Face Index: " + str(face_index_count) + " Max Face Index: " + str(face_index_max))
        mesh_face_flag=0





############################
# Library Controllers
############################

    elif "<library_controllers>" in line:
        lib_controller_flag=1
        lib_geometries_flag=0


    elif ("<Name_array id=" in line ) and (lib_controller_flag == 1):
   
        bone_count=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        print("Number of Bone Names: "+ Fore.GREEN  +str(bone_count) +Style.RESET_ALL)
        bone_name_buffer=line.split(">")[1].split("<")[0].strip()
        print("Extracted Bone Name Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)

    #Bind Pose
    elif ("<source id=" in line) and ("bind_poses" in line) and (lib_controller_flag==1):
        bind_pose_flag=1

    elif ("<float_array id=" in line) and (bind_pose_flag == 1) :
        bind_pose_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        temp_buffer=line.split(">")[1].split("<")[0].split()
        print("Bind Pose Buffer Size: "+ Fore.GREEN  +str(bind_pose_buffer_size) +Style.RESET_ALL)
        bind_pose_buffer=np.zeros(bind_pose_buffer_size, dtype=float)
        print("DEBUG - BIND POSE BUFFER SIZE: " + str(bind_pose_buffer_size))
        print("DEBUG - ACTUAL BIND POSE BUFFER SIZE: " + str(len(temp_buffer)))
        for index in range(bind_pose_buffer_size):
            bind_pose_buffer[index]=float(temp_buffer[index])
        print("Extracted Bind Pose Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        bind_pose_flag=0


    #Vertex Weight
    elif ("<source id=" in line) and ("-skin-weights" in line) and (lib_controller_flag==1):
        vertex_weight_flag=1

    elif ("<float_array id=" in line) and (vertex_weight_flag == 1):
        vertex_weight_buffer_size=int(line.split("count=")[1].split(">")[0].strip(" \" "))
        temp_buffer=line.split(">")[1].split("<")[0].split()
        print("Vertex Weight Buffer Size: "+ Fore.GREEN  +str(vertex_weight_buffer_size) +Style.RESET_ALL)
        vertex_weight_buffer=np.zeros(vertex_weight_buffer_size, dtype=float)
        for index in range(vertex_weight_buffer_size):
            vertex_weight_buffer[index]=float(temp_buffer[index])
        print("Extracted Vertex Weight Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        vertex_weight_flag=0


    #Vertex/Weight Joints
    elif "<joints>" in line:
        joint_flag=1
    elif ("<vertex_weights count=" in line) and (joint_flag == 1):
        vertex_weight_count=int(line.split("=")[1].split(">")[0].strip(" \" "))
        joint_weight_count_buffer=np.zeros(vertex_weight_count, dtype=int)
        joint_index_buffer=np.zeros(vertex_weight_count*8, dtype=int)

    elif ("<vcount>" in line) and (joint_flag == 1):
        temp_buffer=line.split(">")[1].split("<")[0].strip().split()
        for index in range(vertex_weight_count):
            joint_weight_count_buffer[index]=int(temp_buffer[index])
        print("Extracted Vertex Weight Shape Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
    
    elif ("<v>" in line) and (joint_flag == 1):
        temp_buffer=line.split(">")[1].split("<")[0].strip().split()
        weight_index_count=len(temp_buffer)
        for index in range(weight_index_count):
            joint_index_buffer[index]=int(temp_buffer[index])
            if joint_index_buffer[index] > weight_index_max:
            	weight_index_max=joint_index_buffer[index]
        print("Extracted Vertex Weight Index Buffer: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
        print("Number of Weight Index: " + str(weight_index_count) + " Max Weight Index: " + str(weight_index_max))
        joint_flag=0




########################################################################################################################################
# Process Data
########################################################################################################################################




#Vertex Buffer Size
if normal_buffer_size > position_buffer_size:
    vertex_range=int(normal_buffer_size/3)

elif normal_buffer_size < position_buffer_size:
    vertex_range=int(position_buffer_size/3)

elif normal_buffer_size == position_buffer_size:
    vertex_range=int(position_buffer_size/3)

#Debug
print("DEBUG - VERTEX RANGE: " + str(vertex_range))
vertex_range=int(position_buffer_size/3)
print("DEBUG - VERTEX RANGE: " + str(vertex_range))
vertex_buffer_size=vertex_range*40 + vertex_range*12 + 12 + vertex_range*32

print("DEBUG - VERTEX BUFFER SIZE: " + str(vertex_buffer_size))

## center and extent data


center_x=0.0
center_y=-2.033516
center_z =7.290411
extent_x=13.18078
extent_y=4.925367
extent_z=7.290861

if center_x.is_integer():
    center_x=int(center_x)
 
if center_y.is_integer():
    center_y=int(center_y)

if center_z.is_integer():
    center_z=int(center_z)


if extent_x.is_integer():
    extent_x=int(extentr_x)
 
if extent_y.is_integer():
    extent_y=int(extent_y)

if extent_z.is_integer():
    extent_z=int(extent_z)


########################################################################################################################################
# Write .asset file
########################################################################################################################################
new_asset_file = open(sys.argv[1].split(".")[0] + ".asset", "w")



new_asset_file.write("%YAML 1.1\n")
new_asset_file.write("%TAG !u! tag:unity3d.com,2011:\n")
new_asset_file.write("--- !u!43 &4300000\n")
new_asset_file.write("Mesh:\n")
new_asset_file.write("  m_CorrespondingSourceObject: {fileID: 0}\n")
new_asset_file.write("  m_PrefabInstance: {fileID: 0}\n")
new_asset_file.write("  m_PrefabAsset: {fileID: 0}\n")
new_asset_file.write("  m_Name: "+str(asset_name)+"\n")
new_asset_file.write("  serializedVersion: 9\n")
new_asset_file.write("  m_SubMeshes:\n")
new_asset_file.write("  - serializedVersion: 2\n")
new_asset_file.write("    firstByte: 0\n")
new_asset_file.write("    indexCount: "+str(face_buffer_size*3)+"\n")
new_asset_file.write("    topology: 0\n")
new_asset_file.write("    baseVertex: 0\n")
new_asset_file.write("    firstVertex: 0\n")
new_asset_file.write("    vertexCount: "+str(vertex_range)+"\n")
new_asset_file.write("    localAABB:\n")
new_asset_file.write("      m_Center: {x: "+str(center_x)+", y: "+str(center_y)+", z: "+str(center_z)+"}\n")
new_asset_file.write("      m_Extent: {x: "+str(extent_x)+", y: "+str(extent_y)+", z: "+str(extent_z)+"}\n")
new_asset_file.write("  m_Shapes:\n")
new_asset_file.write("    vertices: []\n")
new_asset_file.write("    shapes: []\n")
new_asset_file.write("    channels: []\n")
new_asset_file.write("    fullWeights: []\n")
new_asset_file.write("  m_BindPose:\n")

###############################
# Write Bind Pose
###############################

for index in range(int(bind_pose_buffer_size/16)):
    for i in range(4):
        for j in range(4):
            e_value=bind_pose_buffer[index*16+i*4+j]
            if (e_value == 1) or (e_value == 0) or (e_value == -1):
                e_value=int(e_value)

            if (i == 0) and (j == 0):
                new_asset_file.write("  - e" + str(i) + str(j) + ": " + str(e_value).upper()+"\n")
            else:
                new_asset_file.write("    e" + str(i) + str(j) + ": " + str(e_value).upper()+"\n")

###############################
# Write Bone Name Hash
###############################


new_asset_file.write("  m_BoneNameHashes: 97a622db43a3bd0e18ac2d35927943ddbb8f7228e4c559aa69e847a79fe62f1daca53b6f44f9c3e8fb5d068865b5966201c93cf7ff8bfb766730785006889998085ed24389c4d2ddbb06240ac076b4fb85556f950e881f825efd4cb4a34bbb01ff4b5106bbe4b7da5596f6b2f720ac3ba4e9b6afbfe60f9cfa2ea8659913a79f386a8856\n")
new_asset_file.write("  m_RootBoneNameHash: 3676481175\n")
new_asset_file.write("  m_MeshCompression: 0\n")
new_asset_file.write("  m_IsReadable: 1\n")
new_asset_file.write("  m_KeepVertices: 0\n")
new_asset_file.write("  m_KeepIndices: 0\n")
new_asset_file.write("  m_IndexFormat: 0\n")





def get_face_position_index(face_number):
    index=face_number*9
    return str(face_buffer[index]) +" " + str(face_buffer[index+3]) + " " + str(face_buffer[index+6])


def get_face_position(face_number):
    temp_index_buffer=get_face_position_index(face_number)

    temp_position_v1=str(position_buffer[int(temp_index_buffer.split()[0])*3]) + " " + str(position_buffer[int(temp_index_buffer.split()[0])*3+1]) + " " +str(position_buffer[int(temp_index_buffer.split()[0])*3+2])
    temp_position_v2=str(position_buffer[int(temp_index_buffer.split()[1])*3]) + " " + str(position_buffer[int(temp_index_buffer.split()[1])*3+1]) + " " +str(position_buffer[int(temp_index_buffer.split()[1])*3+2])
    temp_position_v3=str(position_buffer[int(temp_index_buffer.split()[2])*3]) + " " + str(position_buffer[int(temp_index_buffer.split()[2])*3+1]) + " " +str(position_buffer[int(temp_index_buffer.split()[2])*3+2])

    return temp_position_v1 + " " + temp_position_v2 + " " +temp_position_v3


def get_face_normal_index(face_number):
    index=face_number*9
    return str(face_buffer[index+1]) +" " + str(face_buffer[index+4] )+ " " + str(face_buffer[index+7])

def get_face_normal(face_number):
    temp_index_buffer=get_face_normal_index(face_number)
    
    temp_normal_v1=str(normal_buffer[int(temp_index_buffer.split()[0])*3]) + " " + str(normal_buffer[int(temp_index_buffer.split()[0])*3+1]) + " " +str(normal_buffer[int(temp_index_buffer.split()[0])*3+2])
    temp_normal_v2=str(normal_buffer[int(temp_index_buffer.split()[1])*3]) + " " + str(normal_buffer[int(temp_index_buffer.split()[1])*3+1]) + " " +str(normal_buffer[int(temp_index_buffer.split()[1])*3+2])
    temp_normal_v3=str(normal_buffer[int(temp_index_buffer.split()[2])*3]) + " " + str(normal_buffer[int(temp_index_buffer.split()[2])*3+1]) + " " +str(normal_buffer[int(temp_index_buffer.split()[2])*3+2])

    return temp_normal_v1 + " " + temp_normal_v2 + " " +temp_normal_v3



    return str(normal_buffer[int(temp_index_buffer.split()[0])]) + " " + str(normal_buffer[int(temp_index_buffer.split()[1])]) + " " +str(normal_buffer[int(temp_index_buffer.split()[2])])

def get_face_color_index(face_number):
    index=face_number*9
    return str(face_buffer[index+2]) +" " + str(face_buffer[index+5]) + " " + str(face_buffer[index+8])


def get_face_color(face_number):
    temp_index_buffer=get_face_color_index(face_number)
    temp_color_v1=str(color_buffer[int(temp_index_buffer.split()[0])*4]) + " " + str(color_buffer[int(temp_index_buffer.split()[0])*4+1]) + " " +str(color_buffer[int(temp_index_buffer.split()[0])*4+2])
    temp_color_v2=str(color_buffer[int(temp_index_buffer.split()[1])*4]) + " " + str(color_buffer[int(temp_index_buffer.split()[1])*4+1]) + " " +str(color_buffer[int(temp_index_buffer.split()[1])*4+2])
    temp_color_v3=str(color_buffer[int(temp_index_buffer.split()[2])*4]) + " " + str(color_buffer[int(temp_index_buffer.split()[2])*4+1]) + " " +str(color_buffer[int(temp_index_buffer.split()[2])*4+2])

    #print("DEBUG - TEMP FACE COLOR VALUES: " + str(temp_color_values))
    return temp_color_v1 + " " + temp_color_v2 + " " +temp_color_v3

def get_face_hex_color(face_number):
    temp_face_color_buffer=get_face_color(face_number)
    temp_ugg_color_buffer=""

    for vertex_number in range(3):
        temp_color_buffer=temp_face_color_buffer.split()[vertex_number*3] + " " + temp_face_color_buffer.split()[vertex_number*3+1] + " " + temp_face_color_buffer.split()[vertex_number*3+2]
        #print("DEBUG - TEMP COLOR BUFFER: " + str(temp_color_buffer))
        color_red_hex=hex(int(float(temp_color_buffer.split()[0])*255)).split("x")[1]
        color_green_hex=hex(int(float(temp_color_buffer.split()[1])*255)).split("x")[1]
        color_blue_hex=hex(int(float(temp_color_buffer.split()[2])*255)).split("x")[1]
        #print("COLOR RED: MTL: " + str(compressed_obj_vertex_color_array[vertex_pointer*3]) +" DEC: " + str(int(compressed_obj_vertex_color_array[vertex_pointer*3]*255)) + " CONVERT: " + str(color_red_hex))
        #print("COLOR GREEN: MTL: " + str(compressed_obj_vertex_color_array[vertex_pointer*3+1]) +" DEC: " + str(int(compressed_obj_vertex_color_array[vertex_pointer*3+1]*255)) + " CONVERT: " + str(color_green_hex))
        #print("COLOR BLUE: MTL: " + str(compressed_obj_vertex_color_array[vertex_pointer*3+2]) +" DEC: " + str(int(compressed_obj_vertex_color_array[vertex_pointer*3+2]*255)) + " CONVERT: " + str(color_blue_hex))               


        if len(color_red_hex) == 1:
            color_red_hex= "0" + str(color_red_hex)
        if len(color_red_hex) == 0:
            color_red_hex= "00"


        if len(color_green_hex) == 1:
            color_green_hex= "0" + str(color_green_hex)
        if len(color_green_hex) == 0:
            color_green_hex= "00"

        if len(color_blue_hex) == 1:
            color_blue_hex= "0" + str(color_blue_hex)
        if len(color_blue_hex) == 0:
            color_blue_hex= "00"

        temp_ugg_color_buffer+= color_red_hex +  color_green_hex +  color_blue_hex + "ff" + " "
    return temp_ugg_color_buffer



def get_face_color_list():
    temp_color_list=""
    temp_color_count=0
    temp_collision_count=0
    for index in range(int(face_buffer_size)):
        temp_color = get_face_hex_color(index)
        #print("DEBUG - TEMP COLOR: "+ str(temp_color))
        v1=temp_color.split()[0]
        v2=temp_color.split()[1]
        v3=temp_color.split()[2]
        
        if (v1 != v2) and (v1 != v3) and (v2 == v3):
            #print(Fore.RED + "ERROR - FACE COLOR VERTEX MISMATCH: Index = " +str(index) + " v1 = "+ str(v1)+ " v2/v3 = " + str(v2)  +Style.RESET_ALL)
            temp_collision_count+=1
        if (v1 != v2) and (v2 != v3) and (v1 == v3):
            #print(Fore.RED + "ERROR - FACE COLOR VERTEX MISMATCH: Index = " +str(index) + " v2 = "+ str(v2)+ " v1/v3 = " + str(v3)  +Style.RESET_ALL)
            temp_collision_count+=1
        if (v1 != v3) and (v2 != v3) and (v1 == v2):
            #print(Fore.RED + "ERROR - FACE COLOR VERTEX MISMATCH: Index = " +str(index) + " v3 = "+ str(v3)+ " v1/v2 = " + str(v3)  +Style.RESET_ALL)
            temp_collision_count+=1
        if (v1 != v2) and (v1 != v3) and (v1 != v2):
            #print(Fore.RED + "ERROR - FACE COLOR VERTEX MISMATCH: Index = " +str(index) + " v1 = "+ str(v1)+ " v2 = " + str(v2)  + " v3 = " + str(v3)  +Style.RESET_ALL)
            temp_collision_count+=2

        if v1 not in temp_color_list:
            temp_color_list+= str(v1) + " "
            temp_color_count+=1
            print("DEBUG - FOUND NEW COLOR: " +  str(v1))
        if v2 not in temp_color_list:
            temp_color_list+= str(v2) + " "
            temp_color_count+=1
            print("DEBUG - FOUND NEW COLOR: " +  str(v2))
        if v3 not in temp_color_list:
            temp_color_list+= str(v3) + " "
            temp_color_count+=1
            print("DEBUG - FOUND NEW COLOR: " +  str(v3))
    if temp_collision_count > 0:
        print("DEBUG - Number of Collisions: " +  Fore.RED + str(temp_collision_count)+ Style.RESET_ALL)
    return temp_color_list 

###############################
# Write Index Buffer
###############################
print("DEBUG - INDEX BUFFER START")
get_face_color_list()


global new_vertex_buffer
global new_normal_buffer
global new_color_buffer


global new_face_buffer
new_face_buffer=""


new_asset_file.write("  m_IndexBuffer: ")

#if normal_buffer_size > position_buffer_size:
debug_skip=0
if debug_skip == 1:
    new_position_index_buffer=np.zeros(normal_buffer_size, dtype=int)
    new_normal_index_buffer=np.zeros(normal_buffer_size, dtype=int)
    new_color_index_buffer=np.zeros(normal_buffer_size, dtype=np.int64)



    extra_normal_count=0

    for i in range(int(face_buffer_size)):
        i_postion_buffer=get_face_position_index(i).split()
        i_normal_buffer=get_face_normal_index(i).split()
        i_color_buffer=get_face_hex_color(i).split()

        v1_position=i_postion_buffer[0]
        v1_normal=i_normal_buffer[0]
        v1_color=int(i_color_buffer[0],16)

        v2_position=i_postion_buffer[1]
        v2_normal=i_normal_buffer[1]
        v2_color=int(i_color_buffer[1],16)   
        
        v3_position=i_postion_buffer[2]
        v3_normal=i_normal_buffer[2]
        v3_color=int(i_color_buffer[2],16)     


        new_position_index_buffer[int(v1_normal)]=v1_position
        new_position_index_buffer[int(v2_normal)]=v2_position
        new_position_index_buffer[int(v3_normal)]=v3_position

        new_normal_index_buffer[int(v1_normal)]=v1_normal
        new_normal_index_buffer[int(v2_normal)]=v2_normal
        new_normal_index_buffer[int(v3_normal)]=v3_normal
    
        new_color_index_buffer[int(v1_normal)]=v1_color
        new_color_index_buffer[int(v2_normal)]=v2_color
        new_color_index_buffer[int(v3_normal)]=v3_color

        byte1 =format(int(v1_normal),"04x")
        byte2 =format(int(v1_normal),"04x")
        byte3 =format(int(v1_normal),"04x")

        byte_1_transform=str(byte1[-2:])+ str(byte1[:2])
        byte_2_transform=str(byte2[-2:])+ str(byte2[:2])
        byte_3_transform=str(byte3[-2:])+ str(byte3[:2])

        #print("DEBUG: BYTE1: " + str(byte1) + " BYTE2: " + str(byte2) + " BYTE3: " + str(byte3))

        temp_string=byte_3_transform+byte_2_transform+byte_1_transform

        new_asset_file.write(temp_string)
        
        #print("Position Resize: " + str(i) + " of " + str(face_buffer_size))
        


#elif position_buffer_size > normal_buffer_size:
elif debug_skip == 0:
    new_position_index_buffer=np.zeros(position_buffer_size, dtype=int)
    new_normal_index_buffer=np.zeros(position_buffer_size, dtype=int)
    new_color_index_buffer=np.zeros(position_buffer_size, dtype=np.int64)

    extra_normal_count=0

    for i in range(int(face_buffer_size)):
        i_postion_buffer=get_face_position_index(i).split()
        i_normal_buffer=get_face_normal_index(i).split()
        i_color_buffer=get_face_hex_color(i).split()     
        
        v1_position=i_postion_buffer[0]
        v1_normal=i_normal_buffer[0]
        v1_color=int(i_color_buffer[0],16)

        v2_position=i_postion_buffer[1]
        v2_normal=i_normal_buffer[1]
        v2_color=int(i_color_buffer[1],16)   
        
        v3_position=i_postion_buffer[2]
        v3_normal=i_normal_buffer[2]
        v3_color=int(i_color_buffer[2],16)     



        new_position_index_buffer[int(v1_position)]=v1_position
        new_position_index_buffer[int(v2_position)]=v2_position
        new_position_index_buffer[int(v3_position)]=v3_position
        
        new_normal_index_buffer[int(v1_position)]=v1_normal
        new_normal_index_buffer[int(v2_position)]=v2_normal
        new_normal_index_buffer[int(v3_position)]=v3_normal

        new_color_index_buffer[int(v1_position)]=v1_color
        new_color_index_buffer[int(v1_position)]=v2_color
        new_color_index_buffer[int(v1_position)]=v3_color

        byte1 =format(int(v1_position),"04x")
        byte2 =format(int(v2_position),"04x")
        byte3 =format(int(v3_position),"04x")

        byte_1_transform=str(byte1[-2:])+ str(byte1[:2])
        byte_2_transform=str(byte2[-2:])+ str(byte2[:2])
        byte_3_transform=str(byte3[-2:])+ str(byte3[:2])

        #print("DEBUG: BYTE1: " + str(byte1) + " BYTE2: " + str(byte2) + " BYTE3: " + str(byte3))

        temp_string=byte_3_transform+byte_2_transform+byte_1_transform

        new_asset_file.write(temp_string)

        #print("Normal Resize: " + str(i) + " of " + str(face_buffer_size))

#elif position_buffer_size == normal_buffer_size:
elif debug_skip == 1:
    new_position_index_buffer=np.zeros(position_buffer_size, dtype=int)
    new_normal_index_buffer=np.zeros(position_buffer_size, dtype=int)
    new_color_index_buffer=np.zeros(position_buffer_size, dtype=np.int64)

    extra_normal_count=0

    for i in range(int(face_buffer_size)):
        i_postion_buffer=get_face_position_index(i).split()
        i_normal_buffer=get_face_normal_index(i).split()
        i_color_buffer=get_face_hex_color(i).split()     
        
        v1_position=i_postion_buffer[0]
        v1_normal=i_normal_buffer[0]
        v1_color=int(i_color_buffer[0],16)

        v2_position=i_postion_buffer[1]
        v2_normal=i_normal_buffer[1]
        v2_color=int(i_color_buffer[1],16)   
        
        v3_position=i_postion_buffer[2]
        v3_normal=i_normal_buffer[2]
        v3_color=int(i_color_buffer[2],16)     



        new_position_index_buffer[int(v1_position)]=v1_position
        new_position_index_buffer[int(v2_position)]=v2_position
        new_position_index_buffer[int(v3_position)]=v3_position

        new_normal_index_buffer[int(v1_position)]=v1_normal
        new_normal_index_buffer[int(v2_position)]=v2_normal
        new_normal_index_buffer[int(v3_position)]=v3_normal

        new_color_index_buffer[int(v1_normal)]=v1_color
        new_color_index_buffer[int(v2_normal)]=v2_color
        new_color_index_buffer[int(v3_normal)]=v3_color



        byte1 =format(int(v1_position),"04x")
        byte2 =format(int(v2_position),"04x")
        byte3 =format(int(v3_position),"04x")

        byte_1_transform=str(byte1[-2:])+ str(byte1[:2])
        byte_2_transform=str(byte2[-2:])+ str(byte2[:2])
        byte_3_transform=str(byte3[-2:])+ str(byte3[:2])

        #print("DEBUG: BYTE1: " + str(byte1) + " BYTE2: " + str(byte2) + " BYTE3: " + str(byte3))

        temp_string=byte_3_transform+byte_2_transform+byte_1_transform

        new_asset_file.write(temp_string)

        #print("Normal Resize: " + str(i) + " of " + str(face_buffer_size))






new_asset_file.write("\n")


# A: POSITON/NORMALS 
# B: UV/COLOR
# C: VERTEX WEIGHTS
ugg_vertex_buffer_block_A=""
ugg_vertex_buffer_block_B=""
ugg_vertex_buffer_block_C=""








#for index in range(int(face_buffer_size): 












new_asset_file.write("  m_VertexData:\n")
new_asset_file.write("    serializedVersion: 2\n")
new_asset_file.write("    m_VertexCount: "+str(vertex_range)+"\n")
new_asset_file.write("    m_Channels:\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 3\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 12\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 3\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 24\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 4\n")
new_asset_file.write("    - stream: 1\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 2\n")
new_asset_file.write("      dimension: 4\n")
new_asset_file.write("    - stream: 1\n")
new_asset_file.write("      offset: 4\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 2\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 0\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 0\n")
new_asset_file.write("    - stream: 2\n")
new_asset_file.write("      offset: 0\n")
new_asset_file.write("      format: 0\n")
new_asset_file.write("      dimension: 4\n")
new_asset_file.write("    - stream: 2\n")
new_asset_file.write("      offset: 16\n")
new_asset_file.write("      format: 11\n")
new_asset_file.write("      dimension: 4\n")

###############################
# Write Vertex Buffer
###############################

new_asset_file.write("    m_DataSize: "+str(vertex_buffer_size)+"\n")
new_asset_file.write("    _typelessdata: ")



for index in range(vertex_range):


    new_asset_file.write(str(float_to_hex(position_buffer[new_position_index_buffer[index]*3])))
    new_asset_file.write(str(float_to_hex(position_buffer[new_position_index_buffer[index]*3+1])))
    new_asset_file.write(str(float_to_hex(position_buffer[new_position_index_buffer[index]*3+2])))

    new_asset_file.write(str(float_to_hex(normal_buffer[new_normal_index_buffer[index]*3])))
    new_asset_file.write(str(float_to_hex(normal_buffer[new_normal_index_buffer[index]*3+1])))
    new_asset_file.write(str(float_to_hex(normal_buffer[new_normal_index_buffer[index]*3+2])))
    
    new_asset_file.write("0000803f0000000000000000000080bf")

print("Writing Vertex and Normals: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)




for index in range(vertex_range):

    new_asset_file.write("0000000000000000")
    new_asset_file.write(hex(new_color_index_buffer[index]).split("0x")[1])
    #print(hex(new_color_index_buffer[index]).split("0x")[1])



print("Writing Colors: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
#if asset_type == "goose":
new_asset_file.write("cd57213fbb476a3f00000000")

def format_hex(hex_value):
    new_bone=hex_value
    if len(new_bone) == 1:
        new_bone="0" +new_bone
        
    new_bone_count=8-len(new_bone)

    if len(new_bone.strip()) > 2:
        print(Fore.RED + "ERROR - BONE INDEX GREATER THAN FF: " + str(new_bone))
    for j in range(new_bone_count):
        new_bone+="0"
    return new_bone


def get_vertex_weight_hex(vertex_number):
    weight_num=int(joint_weight_count_buffer[vertex_number])
    temp_index=0
    temp_string=""
    temp_weight_joint_index=""
    for index in range(vertex_number):
        temp_index+=int(joint_weight_count_buffer[index])*2

    # Weights
    if weight_num > 0:
        temp_string+=str(float_to_hex(vertex_weight_buffer[joint_index_buffer[temp_index+1]])) + " "
    else:
        temp_string+="00000000 " 
    if weight_num > 1:
        temp_string+=str(float_to_hex(vertex_weight_buffer[joint_index_buffer[temp_index+3]])) + " "
    else:
        temp_string+="00000000 "     
    if weight_num > 2:
        temp_string+=str(float_to_hex(vertex_weight_buffer[joint_index_buffer[temp_index+5]])) + " "
    else:
        temp_string+="00000000 "     
    if weight_num > 3:
        temp_string+=str(float_to_hex(vertex_weight_buffer[joint_index_buffer[temp_index+7]])) + " "
    else:
        temp_string+="00000000 "     


    #Bones - THis wont work for bones over 255 but for UGG, the bones dont go past 34. Ill fix it when it become a problem
    if weight_num > 0:
        #print("Bone Number: " + str(joint_index_buffer[temp_index]))
        new_bone=str(hex(joint_index_buffer[temp_index])).split("0x")[1]
        temp_string+=format_hex(new_bone) + " "

    else:
        temp_string+="00000000 "       
    if weight_num > 1:
        #print("Bone Number: " + str(joint_index_buffer[temp_index+2]))
        new_bone=str(hex(joint_index_buffer[temp_index+2])).split("0x")[1]
        temp_string+=format_hex(new_bone) + " "

    else:
        temp_string+="00000000 "     
    if weight_num > 2:
        #print("Bone Number: " + str(joint_index_buffer[temp_index+4]))
        new_bone=str(hex(joint_index_buffer[temp_index+4])).split("0x")[1]
        temp_string+=format_hex(new_bone) + " "

    else:
        temp_string+="00000000 "     
    if weight_num > 3:
        #print("Bone Number: " + str(joint_index_buffer[temp_index+6]))
        new_bone=str(hex(joint_index_buffer[temp_index+6])).split("0x")[1]
        temp_string+=format_hex(new_bone) + " "

    else:
        temp_string+="00000000 "     

    #print("DEBUG - VERTEX: " +str(vertex_number) + " WEIGHT/INDEX STRING: "+ str(temp_string))
    return temp_string





for index in range(vertex_range):
    temp_weights=get_vertex_weight_hex(new_position_index_buffer[index]).split()
    for j in range(8):
        new_asset_file.write(temp_weights[j])

print("Writing Vertex Weights: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)

new_asset_file.write("\n")


new_asset_file.write("  m_CompressedMesh:\n")
new_asset_file.write("    m_Vertices:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Range: 0\n")
new_asset_file.write("      m_Start: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_UV:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Range: 0\n")
new_asset_file.write("      m_Start: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_Normals:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Range: 0\n")
new_asset_file.write("      m_Start: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_Tangents:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Range: 0\n")
new_asset_file.write("      m_Start: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_Weights:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_NormalSigns:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_TangentSigns:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_FloatColors:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Range: 0\n")
new_asset_file.write("      m_Start: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_BoneIndices:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_Triangles:\n")
new_asset_file.write("      m_NumItems: 0\n")
new_asset_file.write("      m_Data:\n")
new_asset_file.write("      m_BitSize: 0\n")
new_asset_file.write("    m_UVInfo: 0\n")
new_asset_file.write("  m_LocalAABB:\n")
new_asset_file.write("    m_Center: {x: "+str(center_x)+", y: "+str(center_y)+", z: "+str(center_z)+"}\n")
new_asset_file.write("    m_Extent: {x: "+str(extent_x)+", y: "+str(extent_y)+", z: "+str(extent_z)+"}\n")
new_asset_file.write("  m_MeshUsageFlags: 1\n")
new_asset_file.write("  m_BakedConvexCollisionMesh:\n")
new_asset_file.write("  m_BakedTriangleCollisionMesh:\n")
new_asset_file.write("  m_MeshMetrics[0]: 1\n")
new_asset_file.write("  m_MeshMetrics[1]: 1\n")
new_asset_file.write("  m_MeshOptimized: 1\n")
new_asset_file.write("  m_StreamData:\n")
new_asset_file.write("    offset: 0\n")
new_asset_file.write("    size: 0\n")
new_asset_file.write("    path:\n")


new_asset_file.close()


print("Asset Compilation: "+ Fore.GREEN + "[COMPLETE]" +Style.RESET_ALL)

########################################################################################################################################
# CONVERT TO UNITY ASSET BUNDLE EXTRACTOR DUMP
########################################################################################################################################


python_script="asset_to_UABE.py"
input_file=str(sys.argv[1].split(".")[0] + ".asset")


print("STARTING SUBPROCESS: "+ Fore.YELLOW + "["+str(python_script)+"]" +Style.RESET_ALL)
subprocess.call(["python", python_script, input_file])












