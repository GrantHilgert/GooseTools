#GooseTool's Obj to Asset Converter
major=0
minor=5

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



print("GooseTool's Object to Asset Converter")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")



########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################

def float_to_hex(f):

    data_double=str(hex(struct.unpack('<I', struct.pack('<f', f))[0])).split('x')[1]

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

    return output_data



def get_color(vertex_num,new_color):


    return "63aacsff"

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

def material_vertex_count(material_buffer, material, vertex_index):
    count=0
    for material_in_buffer in material_buffer.split("@"):
        if material_in_buffer.split()[0] == material:
            for item_num in range(len(material_in_buffer.split())-1):
                if int(material_in_buffers.split()[item_num+1].strip()) == int(vertex_index.strip()):
                    count+=1
    return count


def get_best_material(material_buffer, vertex_index):
    #print("Getting Best Material For: " + str(vertex_index))
    count_local=0
    count_total=0
    count_string=''
    for material_in_buffer in material_buffer.split("@"):
            for item_num in range(len(material_in_buffer.split())-1):
                if int(material_in_buffer.split()[item_num+1].strip()) == int(vertex_index.strip()):
                    count_local+=1
                    count_total+=1
            count_string+=str(count_local) + " "

            count_local=0

    best_count=0
    best_index=0
    index=0
    for max_count in count_string.split():
        if int(max_count) > int(best_count):
            print("NEW MAX: " + str(max_count) + " > " + str(best_count))         
            best_count = max_count
            best_index = index
        elif int(max_count) == int(best_count) and int(best_count) != 0:
            print("ERROR THERE IS A TIE")
        elif int(max_count) != 0:
            print("IGNORING: " + str(max_count) + " < " + str(best_count))   


        index+=1

    #print("WINNER: " + str(str(material_buffer.split("@")[best_index]).split()[0]) + " with " + str(best_count))
    return str(str(material_buffer.split("@")[best_index]).split()[0])


def get_best_material_fast(material_buffer, vertex_index):
    #print("Getting Best Material For: " + str(vertex_index))
    material= np.zeros(mtl_material_count_preprocess*3, dtype=float)

    count_local=0
    count_total=0
    count_string=''
    for material_in_buffer in material_buffer.split("@"):
            for item_num in range(len(material_in_buffer.split())-1):
                if int(material_in_buffer.split()[item_num+1].strip()) == int(vertex_index.strip()):
                    count_local+=1
                    count_total+=1
            count_string+=str(count_local) + " "

            count_local=0

    best_count=0
    best_index=0
    index=0
    for max_count in count_string.split():
        if int(max_count) > int(best_count):
            print("NEW MAX: " + str(max_count) + " > " + str(best_count))         
            best_count = max_count
            best_index = index
        elif int(max_count) == int(best_count) and int(best_count) != 0:
            print("ERROR THERE IS A TIE")
        elif int(max_count) != 0:
            print("IGNORING: " + str(max_count) + " < " + str(best_count))   


        index+=1

    #print("WINNER: " + str(str(material_buffer.split("@")[best_index]).split()[0]) + " with " + str(best_count))
    return str(str(material_buffer.split("@")[best_index]).split()[0])


def get_material_value_from_name(material_name, component):
    global obj_material_list
    global mtl_kd_array
    index=0
    for material_list_item in obj_material_list.split():
        #print(material_name.strip() + " == " + material_list_item.strip())
        if material_name.strip() == material_list_item.strip():
            if component == "r":
                return str(mtl_kd_array[index*3])
            elif component == "g":
                return str(mtl_kd_array[(index*3)+1])
            elif component == "b":
                return str(mtl_kd_array[(index*3)+2])
            else:
                #print("FAILED TO GET MATERIAL FROM NAME")
                return "FAIL"
        #else:
    
            #print("ERROR MATERIAL NOT IN LIST")
        index+=1



def find_material_face_max(material):
    global face_material_buffer
    face_max=0
    for material_in_buffer in face_material_buffer.split("@"):
        if len(material_in_buffer.split()) > 0 and material == material_in_buffer.split()[0].strip():
            for test_value in material_in_buffer.split():
                if test_value != material:
                    if int(test_value) > int(face_max):
                        face_max = int(test_value)
    return face_max

def find_material_face_min(material):
    global face_material_buffer
    face_min=0
    for material_in_buffer in face_material_buffer.split("@"):
        if len(material_in_buffer.split()) > 0 and material == material_in_buffer.split()[0].strip():
            for test_value in material_in_buffer.split():
                if test_value != material:
                    if face_min != 0:
                        if int(test_value) < int(face_min):
                            face_min = int(test_value)
                    else:
                        face_min = int(test_value)

    return face_min


def find_material_face_buffer_size(material):
    global face_material_buffer
    buffer_size=0
    face_max=0
    for material_in_buffer in face_material_buffer.split("@"):  
        if len(material_in_buffer.split()) > 0 and material == material_in_buffer.split()[0].strip():
            for test_value in material_in_buffer.split():
                if test_value != material:
                    if int(test_value) > int(face_max):
                        face_max = int(test_value)
                        #Buffer size increases every time index increases
                        buffer_size+=1
    return buffer_size



def get_global_skip_list():
    global face_material_buffer
    #count_start=find_material_face_min(material)
    #count_stop=find_material_face_max(material)
    count_start=min(obj_face_array)-1
    count_stop=max(obj_face_array)-1
    n_global_skip_list=""
    next_count=count_start
    found=0
    skip_list=''
    for face_index in range(max(obj_face_array)-1):
        if str(" " + str(face_index) + " ") not in face_material_buffer:
            n_global_skip_list+=str(face_index) + " "          

    return n_global_skip_list


def get_material_local_skip_list(material):
    global face_material_buffer
    count_start=find_material_face_min(material)
    count_stop=find_material_face_max(material)

    next_count=count_start
    found=0
    skip_list=''
    for material_in_buffer in face_material_buffer.split("@"):  
        if len(material_in_buffer.split()) > 0 and material == material_in_buffer.split()[0].strip():
            for face_index in range(count_start,count_stop):
                #if face_index == 0:
                    #print("DEBUG - MATERIAL SKIP LIST: " + str(material_in_buffer.split()[0].strip()))
                    #print("MIB: " + str(int(material_in_buffer.split()[face_index])) + " COUNT: " + str(int(next_count)))
                if str(" " + str(face_index) + " " ) in material_in_buffer:
                    #print("FOUND " + str(next_count))
                    found=1

                if found == 0:
                    skip_list+=str(face_index) + " "
                found=0     


    return skip_list





def get_material_global_buffer_range(material):
	#local_max=find_material_face_max(material)
	#local_min=find_material_face_min(material)
    local_max=max(obj_face_array)-1
    local_min=min(obj_face_array)-1
    skip_list_size=len(get_material_local_skip_list(material).split())
    #print("MAX: " + str(local_max)+ " MIN: " + str(local_min) + " SKIP SIZE: " + str(skip_list_size))
    return local_max-local_min-skip_list_size+1

def get_material_local_buffer_range(material):
    local_max=find_material_face_max(material)
    local_min=find_material_face_min(material)

    skip_list_size=len(get_material_local_skip_list(material).split())
    #print("MAX: " + str(local_max)+ " MIN: " + str(local_min) + " SKIP SIZE: " + str(skip_list_size))
    return local_max-local_min-skip_list_size



init()






########################################################################################################################################
#PARSE TEMPLATE ASSET
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
        print("Reference Asset Name: "+ Fore.GREEN + "["+ str(asset_name) + "]" +Style.RESET_ALL)
    
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
#PRINT INFO
########################################################################################################################################




asset_type=get_asset_type(vertex_count,vertex_buffer_size)
if asset_type == "simple":
    vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
    print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
elif asset_type == "complex":

    complex_vertex_buffer_size=40*vertex_count
    complex_color_buffer_size=12*vertex_count
    complex_bone_buffer_size=32*vertex_count
    vertex_buffer_block_size=40
    typeless_data_buffer_size=complex_vertex_buffer_size+complex_color_buffer_size+complex_bone_buffer_size+12
    print("Complex Material Block Size: " +Fore.GREEN+ str(complex_color_buffer_size)+Style.RESET_ALL)
    print("Complex Vertex Buffer Size: " +str(typeless_data_buffer_size))
    print("Complex Vertex Block Size: " +Fore.GREEN+ str(complex_vertex_buffer_size)+Style.RESET_ALL)
    print("Complex Bone Block Size: " +Fore.GREEN+ str(complex_bone_buffer_size)+Style.RESET_ALL)

#print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)



########################################################################################################################################
#PREPROCESS .OBJ FILE
########################################################################################################################################


#open Object file from command line
object_file = open(sys.argv[2], "r")


#extract vertex buffer size
obj_vertex_count_preprocess=0
obj_normal_count_preprocess=0
obj_uv_count_preprocess=0
obj_face_count_preprocess=0
obj_name_count_preprocess=0

obj_material_filename=""
obj_material_path=""
obj_material_count_preprocess=0
obj_material_list=""

obj_header_text_preprocess=""
obj_multi_obj_preprocess_flag=0
obj_count_preprocess=1

obj_vertex_count_array_preprocess=""
obj_normal_count_array_preprocess=""
obj_uv_count_array_preprocess=""
obj_face_count_array_preprocess=""

obj_name=""

obj_line_count_preprocess=0


obj_vertex_array_size_preprocess=0
obj_normal_array_size_preprocess=0
obj_uv_array_size_preprocess=0
obj_face_array_size_preprocess=0

#Read file line by line
OBJECT_LINE = object_file.readlines()
print("Preprocessing file : "+Fore.GREEN + str(sys.argv[2].split("\\")[len(sys.argv[2].split("\\"))-1]) +Style.RESET_ALL)
for line in OBJECT_LINE:
    
    if "v" == line.split()[0] and obj_multi_obj_preprocess_flag == 1:
        #Detect Multiple Objects.
        obj_count_preprocess+=1
        obj_vertex_count_array_preprocess+=str(obj_vertex_count_preprocess) + " "
        obj_normal_count_array_preprocess+=str(obj_normal_count_preprocess) + " "
        obj_uv_count_array_preprocess+=str(obj_uv_count_preprocess) + " "
        obj_face_count_array_preprocess+=str(obj_face_count_preprocess) + " "
        
        obj_vertex_array_size_preprocess+=obj_vertex_count_preprocess
        obj_normal_array_size_preprocess+=obj_normal_count_preprocess
        obj_uv_array_size_preprocess+=obj_uv_count_preprocess
        obj_face_array_size_preprocess+=obj_face_count_preprocess

        obj_vertex_count_preprocess=0
        obj_normal_count_preprocess=0
        obj_uv_count_preprocess=0
        obj_face_count_preprocess=0
        obj_multi_obj_preprocess_flag=0


        print("New Object Detected: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
    if "v" == line.split()[0]:
        obj_vertex_count_preprocess+=1
    if "vn" in line.split()[0]:
        obj_normal_count_preprocess+=1
    if "vt" in line.split()[0]:
        obj_uv_count_preprocess+=1
    if "f" in line.split()[0]:
        obj_face_count_preprocess+=1
        obj_multi_obj_preprocess_flag=1
    
    if "mtllib" == line.split()[0]:
        obj_material_filename=line.split()[1]
    if "usemtl" == line.split()[0]:
        obj_material_list+=line.split()[1] + " "
        obj_material_count_preprocess+=1

    if "o" == line.split()[0]:
        obj_name+=line.split()[1] + " "
        obj_name_count_preprocess+=1
    
    if obj_vertex_count_preprocess == 0 and obj_material_path == "":
        obj_header_text_preprocess+=line
    obj_line_count_preprocess+=1

#Store Last Preprocess Values in Array
obj_vertex_count_array_preprocess+=str(obj_vertex_count_preprocess)
obj_normal_count_array_preprocess+=str(obj_normal_count_preprocess)
obj_uv_count_array_preprocess+=str(obj_uv_count_preprocess)
obj_face_count_array_preprocess+=str(obj_face_count_preprocess)

#Store Last Preprocess Values
obj_vertex_array_size_preprocess+=obj_vertex_count_preprocess
obj_normal_array_size_preprocess+=obj_normal_count_preprocess
obj_uv_array_size_preprocess+=obj_uv_count_preprocess
obj_face_array_size_preprocess+=obj_face_count_preprocess

#Return to beginng
object_file.seek(0)


print("OBJ Preprocessing: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)






########################################################################################################################################
#PREPROCESS .MTL FILE
########################################################################################################################################

obj_material_path_ok=0
obj_material_path=sys.argv[2].split(".")[0] + ".mtl"
mtl_material_count_preprocess=0
mtl_material_buffer=""

if path.exists(obj_material_path):
    obj_material_path_ok=1
    print("Preprocessing file : "+Fore.MAGENTA + str(obj_material_filename) +Style.RESET_ALL)
    mtl_file = open(obj_material_path, "r")

    #Parse the MTL file
    MTL_LINE = mtl_file.readlines()
    for line_mtl in MTL_LINE: 
        if len(line_mtl.split()) > 0:    
            if "newmtl" == line_mtl.split()[0]:
                mtl_material_count_preprocess+=1

    print("MTL Preprocessing: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)       
    print(str(mtl_material_count_preprocess))

    #Parse MTL file
    mtl_kd_array= np.zeros(mtl_material_count_preprocess*3, dtype=float)
    mtl_file.seek(0)
    material_current=""
    material_next=""

    mtl_material_index=0
    mtl_material_error_temp=0
    for line_mtl in MTL_LINE: 
        if len(line_mtl.split()) > 0:
            if "newmtl" == line_mtl.split()[0].strip():

                if line_mtl.split()[1].strip() in obj_material_list:
                    mtl_material_index+=1
                    mtl_material_error_temp=0
                    mtl_material_buffer+=line_mtl.split()[1].strip() + " "
                else: 
                    print("Import Material from .mtl: "+Fore.RED + "[MATCH FAIL]" +Style.RESET_ALL)
                    print(str(line_mtl.split()[1].strip()))
                    mtl_material_error_temp=1  
            
            if "Kd" == line_mtl.split()[0].strip() and mtl_material_error_temp == 0:
                #store diffused colore data
                mtl_kd_array[(mtl_material_index-1)*3]=line_mtl.split()[1].strip()
                mtl_kd_array[(mtl_material_index-1)*3+1]=line_mtl.split()[2].strip()
                mtl_kd_array[(mtl_material_index-1)*3+2]=line_mtl.split()[3].strip()

                print("Import .mtl Material: "+Fore.YELLOW + "[" + str(obj_material_list.split()[mtl_material_index-1])+ "]" +Style.RESET_ALL) 

else:

    print(".MTL File Not Found : "+Fore.RED + str(obj_material_path) +Style.RESET_ALL)

#print("DEBUG - MATERIAL INDEX COUNT:" + str(mtl_material_index))



print(".Obj Info")

print("Number of Objects: "+Fore.GREEN + str(obj_count_preprocess)+Style.RESET_ALL)
print("Object Names: "+Fore.GREEN + str(obj_name)+Style.RESET_ALL)
print("Number of Materials: "+Fore.GREEN + str(obj_material_count_preprocess)+Style.RESET_ALL)
print("Materials: "+Fore.YELLOW +str(obj_material_list)+Style.RESET_ALL)



print("Total Vertex: "+Fore.GREEN +str(obj_vertex_array_size_preprocess)+Style.RESET_ALL)
print("Total Normal: "+Fore.GREEN +str(obj_normal_array_size_preprocess)+Style.RESET_ALL)
print("Total UV: "+Fore.GREEN +str(obj_uv_array_size_preprocess)+Style.RESET_ALL)
print("Total Face: "+Fore.GREEN +str(obj_face_array_size_preprocess)+Style.RESET_ALL)





########################################################################################################################################
#PARSE OBJECT FILE DATA
########################################################################################################################################
#Parse Object File Data



obj_vertex_count=0
obj_normal_count=0
obj_uv_count=0
obj_face_count=0









#Parse Control
g1_found=0
g2_found=0
v_found=0
vn_found=0
f_found=0
fail_flag=0
error_flag=0


#Verticies
#my indexing method breaks on position 0
global obj_vertex_array
obj_vertex_array= np.zeros((obj_count_preprocess*obj_vertex_array_size_preprocess)*3, dtype=float)
#Normals
global obj_normal_array
obj_normal_array= np.zeros((obj_count_preprocess*obj_normal_array_size_preprocess)*3, dtype=float)
#UV
global obj_uv_array
obj_uv_array= np.zeros((obj_count_preprocess*obj_uv_array_size_preprocess)*3, dtype=float)

#Faces
global obj_face_array
obj_face_array= np.zeros((obj_count_preprocess*obj_face_array_size_preprocess)*3, dtype=int)

#Face Color Array
global obj_face_color_array
obj_face_color_array= np.zeros((obj_count_preprocess*obj_face_array_size_preprocess)*3*3, dtype=float)









#Colors - deprecicated
obj_color_array= np.zeros((obj_count_preprocess*obj_vertex_array_size_preprocess)*3, dtype=float)


#Object Header Information
obj_vert_count=0
obj_index_cound=0
obj_g1=''
obj_g2=''


obj_next_index=1
object_index=0

debug_count=0

face_material_buffer=''
failed_vertex_color=0
failed_face_list=''
failed_face_buffer=''

#reset color index
mtl_material_index=0
#bar = progressbar.ProgressBar(max_value=obj_line_count_preprocess)
#progress_bar_count=0
#Read file line by line
OBJECT_LINE = object_file.readlines()
#comb through file, line by line
#print("Processing Object "+str(object_index) + ":")
for line in OBJECT_LINE: 
    #check for Errors
    if fail_flag == 0:
        #print(str(debug_count))
        #Check if we are at the next object from the list we compiled during preprocessing
        
        if ("o" in line.split()[0] or "g" in line.split()[0]):
            if len(obj_name.split()) >= obj_next_index:
                if obj_name.split()[obj_next_index-1].strip() == line.split()[1].strip():
                    #print(str(obj_name.split()[obj_next_index].strip())+" == "+str(line.split()[1].strip()))
                    print("Setting New Object: "+Fore.GREEN + "["+obj_name.split()[obj_next_index-1].strip() +"]"+Style.RESET_ALL)
                    object_index=obj_next_index
                    obj_next_index+=1
                    obj_normal_count=0
                    obj_vertex_count=0
                    obj_uv_count=0
                    obj_s_value=0
                    obj_face_material='default'


        #Collect Verticies
        elif "v" == line.split()[0]:
            #print("Reading Verticies")

            #print(str(object_index*obj_vertex_count*3))

            obj_vertex_array[object_index*obj_vertex_count*3]=float(str(line.split()[1]))
            obj_vertex_array[object_index*obj_vertex_count*3+1]=float(str(line.split()[2]))
            obj_vertex_array[object_index*obj_vertex_count*3+2]=float(str(line.split()[3]))
            obj_vertex_count+=1


        #Collect Normals
        elif "vn" == line.split()[0]: 
            #print("Reading Normals")
            vn_found=1
            obj_normal_array[object_index*obj_normal_count*3]=float(str(line.split()[1]))
            obj_normal_array[object_index*obj_normal_count*3+1]=float(str(line.split()[2]))
            obj_normal_array[object_index*obj_normal_count*3+2]=float(str(line.split()[3]))
            #obj_normal_array[obj_vertex_count_vn*3]=0
            #obj_normal_array[obj_vertex_count_vn*3+1]=0
            #obj_normal_array[obj_vertex_count_vn*3+2]=0
            obj_normal_count+=1
        
        #Collect UV
        elif "vt" == line.split()[0]: 
            #print("Reading UV")
            vt_found=1
            obj_uv_array[object_index*obj_uv_count*3]=float(str(line.split()[1]))
            obj_uv_array[object_index*obj_uv_count*3+1]=float(str(line.split()[2]))

            #obj_normal_array[obj_vertex_count_vn*3]=0
            #obj_normal_array[obj_vertex_count_vn*3+1]=0
            #obj_normal_array[obj_vertex_count_vn*3+2]=0
            obj_uv_count+=1


        #Set Material
        elif "usemtl" == line.split()[0]: 

            if str(line.split()[1]).strip() in mtl_material_buffer:
                print("Linking Face to Material: "+ Fore.YELLOW +"["+ str(line.split()[1])+"]" +Style.RESET_ALL)
                obj_face_material=str(line.split()[1])
                #Create a huge face material buffer for vertex baking
                face_material_buffer+="@ "
                face_material_buffer+=str(line.split()[1])
                face_material_buffer+=" "
                mtl_material_index+=1
            else:
                print("Failed to link Face to Material: "+ Fore.RED + str(line.split()[1]) +Style.RESET_ALL)

        elif "mtllib" == line.split()[0]: 
            if obj_material_filename == line.split()[1] and obj_material_path_ok == 1:
                print("Using .MTL file: "+ Fore.GREEN + str(obj_material_path) +Style.RESET_ALL)
            else:
                print("Use .MTL file: "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)
        
        #Set S property
        elif "s" == line.split()[0]: 
            obj_s_value=str(line.split()[1])
        #Find Faces, Stored in reverse order
        


        elif "f" == line.split()[0]: 
            #print("Reading Faces")        


            face_buffer=line.split()
            data1=face_buffer[1].split("/")
            data2=face_buffer[2].split("/")
            data3=face_buffer[3].split("/")
            face_material_buffer+=str(int(data1[0])) + " " + str(int(data2[0])) + " " + str(int(data3[0])) + " "
            #print("FACE 1: " +str(int(data1[0])))

            #print("FACE 2: " +str(int(data2[0])))

            #print("FACE 3: " +str(int(data3[0])))

            
            obj_face_array[obj_face_count*3]=int(data1[0])
            obj_face_array[obj_face_count*3+1]=int(data2[0])
            obj_face_array[obj_face_count*3+2]=int(data3[0])

            #Copy Face  1 Colors to Buffer
            obj_face_color_array[obj_face_count*9]=get_material_value_from_name(obj_face_material, 'r')
            obj_face_color_array[obj_face_count*9+1]=get_material_value_from_name(obj_face_material, 'g')
            obj_face_color_array[obj_face_count*9+2]=get_material_value_from_name(obj_face_material, 'b')

            #Copy Face  2 Colors to Buffer
            obj_face_color_array[obj_face_count*9+3]=get_material_value_from_name(obj_face_material, 'r')
            obj_face_color_array[obj_face_count*9+4]=get_material_value_from_name(obj_face_material, 'g')
            obj_face_color_array[obj_face_count*9+5]=get_material_value_from_name(obj_face_material, 'b')

            #Copy Face  3 Colors to Buffer
            obj_face_color_array[obj_face_count*9+6]=get_material_value_from_name(obj_face_material, 'r')
            obj_face_color_array[obj_face_count*9+7]=get_material_value_from_name(obj_face_material, 'g')
            obj_face_color_array[obj_face_count*9+8]=get_material_value_from_name(obj_face_material, 'b')


            obj_face_count+=1
            #print(str((int(data1[0])-1)*3) +"=="+ str(mtl_kd_array[(mtl_material_index-1)*3]))
            #Write Vertex Color Data
 
########################################################################################################################################
#BAKE VERTEX DATA - DEPRECIATED
########################################################################################################################################           



            #Probably delete everytthing from  TO HERE *******************************************************





        elif "#" in line:
            print("COMMENT: "+Fore.CYAN +str(line.strip("\n")) + Style.RESET_ALL)

        else:
            print("PARSE ERROR: "+Fore.RED + "Could not Parse: " +str(line) + Style.RESET_ALL)
            print(str(obj_material_list.split()[obj_next_index]))

    #progress_bar_count+=1
    #bar.update(progress_bar_count)

    debug_count+=1

 
########################################################################################################################################
#DUPLCIATE MULTI-COLORED VERTEX AND COMPRESS OBJECT
########################################################################################################################################   


print("Number of Failed Color Vertex "+Fore.GREEN + str(failed_vertex_color)+Style.RESET_ALL)
#print("Failed Faces: " + failed_face_list)

############################
# Get size of new buffer
############################

compressed_buffer_size=0
uncompressed_buffer_size=0
for test_material in obj_material_list.split():
    #print("TEST MATERIAL: "  + str(test_material))
    #print("FACE MATERAIL BUFFER" + str(face_material_buffer))
    buf_size=str(find_material_face_buffer_size(test_material))
    buf_max=str(find_material_face_max(test_material))
    buf_min=str(find_material_face_min(test_material))


    #print(str(test_material) + " Max Face Number: " + buf_max + " Min Face Number: " + buf_min)
    #print(str(test_material) + " Buffer Size: " + buf_size + " Uncompressed Buffer Size: " + str(int(buf_max)-int(buf_min)))
    uncompressed_buffer_size+=int(buf_max)-int(buf_min)
    compressed_buffer_size+=int(buf_size)

print("Buffer size before: " +Fore.YELLOW + str(uncompressed_buffer_size) +Style.RESET_ALL)
print("Buffer size after compression: " +Fore.YELLOW + str(compressed_buffer_size) +Style.RESET_ALL)

############################
# Create New Buffers
############################

global compressed_obj_vertex_array
compressed_obj_vertex_array = np.zeros((uncompressed_buffer_size)*3*3, dtype=float)
#Normals
global compressed_obj_normal_array
compressed_obj_normal_array = np.zeros((uncompressed_buffer_size)*3*3, dtype=float)
#UV
global compressed_obj_uv_array
compressed_obj_uv_array= np.zeros((uncompressed_buffer_size)*3*3, dtype=float)
#Colors
global compressed_obj_vertex_color_array
compressed_obj_color_array= np.zeros((uncompressed_buffer_size)*3, dtype=float)
#Faces
global compressed_obj_face_array
compressed_obj_face_array= np.zeros((obj_face_array_size_preprocess)*3, dtype=int)
#Face Colors
global compressed_obj_face_color_array
compressed_obj_face_color_array= np.zeros((obj_face_array_size_preprocess)*3*3, dtype=float)

global compression_factor
compression_factor=np.zeros((obj_face_array_size_preprocess)*3, dtype=float)

global compressed_obj_vertex_color_array
compressed_obj_vertex_color_array= np.zeros((obj_face_array_size_preprocess)*3*3, dtype=float)

#Offset from each different material 
global_offset=0
local_offset=0

###################################
#Start Copying Data 
##################################

# 1) For each material, find the small face index and the largest face index "The range"
# 2) Use the range to find all the numbers that dont exist between the largest and the smallest and put them in our list
# 3) For each material we found during preprocessing, interate over the entire face buffer.
# 4) For all the faces that use out maerial, write them to our new compressed buffer
# 5) The materials stack on top of each other in the face buffer. If a vertex shares colors with multiple faces, it gets copied to our new buffer once for every color
# 6) If a index is in our skip list, we dont write it. This compresses the new buffer. 



def compress_face(input_face,input_material):
    check_postion=input_face/3

    if ((input_face+1)/3).is_integer():
        pos_index = 2
    elif ((input_face+1)/2).is_integer():
        pos_index = 1
    elif ((input_face+1)/1).is_integer():
        pos_index = 0

    # input_face = face index
    # input material = face material 
    #


    if float(obj_face_color_array[(input_face*3 )]) == float(get_material_value_from_name(input_material, 'r')):               
        if float(obj_face_color_array[input_face*3+1]) == float(get_material_value_from_name(input_material, 'g')):           
            if float(obj_face_color_array[input_face*3+2]) == float(get_material_value_from_name(input_material, 'b')):      
                    
                compressed_vertex_index=(obj_face_array[(input_face)] - local_compressed_face_offset) + global_compressed_face_buffer_index - int(compression_factor[obj_face_array[input_face]-1]) -1
                #print("COMPRESSED INDEX = " + str(obj_face_array[(input_face)]) + " - " + str(local_compressed_face_offset) + " + " + str(global_compressed_face_buffer_index) + " - " + str(int(compression_factor[obj_face_array[input_face] - local_compressed_face_offset]-1)) + " - 1 = " +str(compressed_vertex_index) )
                
                if compressed_obj_vertex_array[compressed_vertex_index*3] == 0 or float(compressed_obj_vertex_array[compressed_vertex_index*3] )== float(obj_vertex_array[(obj_face_array[input_face]-1)*3]):
                    
                    if compressed_obj_vertex_array[compressed_vertex_index*3+1] == 0 or float(compressed_obj_vertex_array[compressed_vertex_index*3+1] )== float(obj_vertex_array[(obj_face_array[input_face]-1)*3+1]):
                        
                        if compressed_obj_vertex_array[compressed_vertex_index*3+2] == 0 or float(compressed_obj_vertex_array[compressed_vertex_index*3+2] )== float(obj_vertex_array[(obj_face_array[input_face]-1)*3+2]):                                          
                            #print("DEBUG - Input: " +str(input_face) + " WRITTING FACE : "+str(obj_face_array[input_face]) +" With Index: "+ str(input_face)+  " COMPRESSED INDEX: " + str(int(compressed_vertex_index)*3) + " COMPRESSION FACTOR: " + str(int(compression_factor[obj_face_array[input_face]-1])))
                        #print("DEBUG - COMPRESSED FACE (1): " + str(obj_face_array[input_face*3]) + " ==> " + str(int(obj_face=_array[input_face*3]) - local_compressed_face_offset + global_compressed_face_buffer_index))
                                

                            # VERTEX
                            compressed_obj_vertex_array[compressed_vertex_index*3] = obj_vertex_array[(obj_face_array[input_face]-1)*3]
                            compressed_obj_vertex_array[compressed_vertex_index*3+1] = obj_vertex_array[(obj_face_array[input_face]-1)*3+1]
                            compressed_obj_vertex_array[compressed_vertex_index*3+2] = obj_vertex_array[(obj_face_array[input_face]-1)*3+2]

                            # Normal
                            compressed_obj_normal_array[compressed_vertex_index*3] = obj_normal_array[(obj_face_array[input_face]-1)*3]
                            compressed_obj_normal_array[compressed_vertex_index*3+1] = obj_normal_array[(obj_face_array[input_face]-1)*3+1]
                            compressed_obj_normal_array[compressed_vertex_index*3+2] = obj_normal_array[(obj_face_array[input_face]-1)*3+2]

                            #Vertex Colors
                            compressed_obj_vertex_color_array[compressed_vertex_index*3] = float(get_material_value_from_name(input_material, 'r'))
                            compressed_obj_vertex_color_array[compressed_vertex_index*3+1] = float(get_material_value_from_name(input_material, 'g'))
                            compressed_obj_vertex_color_array[compressed_vertex_index*3+2] = float(get_material_value_from_name(input_material, 'b'))
                        

                            # FACE
                            compressed_obj_face_array[input_face] = int(obj_face_array[input_face]) - local_compressed_face_offset + global_compressed_face_buffer_index - int(compression_factor[(obj_face_array[input_face]-1)])
                            
                            #Face Color - Depreciated
                            compressed_obj_face_color_array[input_face*3] = obj_face_color_array[input_face*3]
                            compressed_obj_face_color_array[input_face*3+1] = obj_face_color_array[input_face*3+1]
                            compressed_obj_face_color_array[input_face*3+2] = obj_face_color_array[input_face*3+2]

                        else: 
                            print(Fore.RED +"ERROR - Z POS " + str(pos_index) + " WRITTING FACE : "+str(obj_face_array[input_face]) +" With Index: "+ str(input_face)+  " COMPRESSED INDEX: " + str(int(compressed_vertex_index)) + " COMPRESSION FACTOR: " + str(int(compression_factor[obj_face_array[input_face]-1]))+Style.RESET_ALL)
                            print("DEBUG: " + str(compressed_obj_vertex_array[compressed_vertex_index*3+2]) +" == " + str(obj_vertex_array[obj_face_array[input_face-1]*3-2]))

                    else: 
                        print(Fore.RED +"ERROR - Y POS  " + str(pos_index) + " WRITTING FACE : "+str(obj_face_array[input_face]) +" With Index: "+ str(input_face)+  " COMPRESSED INDEX: " + str(int(compressed_vertex_index)) + " COMPRESSION FACTOR: " + str(int(compression_factor[obj_face_array[input_face]-1]))+Style.RESET_ALL)
                        print("DEBUG: " + str(compressed_obj_vertex_array[compressed_vertex_index*+1]) +" == " + str(obj_vertex_array[obj_face_array[input_face]*3-1]))
                else: 
                    print(Fore.RED +"ERROR - X POS  " + str(pos_index) + " WRITTING FACE : "+str(obj_face_array[input_face]) +" With Index: "+ str(input_face)+  " COMPRESSED INDEX: " + str(int(compressed_vertex_index)) + " COMPRESSION FACTOR: " + str(int(compression_factor[obj_face_array[input_face]-1]))+Style.RESET_ALL)
                    print("DEBUG: " + str(compressed_obj_vertex_array[compressed_vertex_index*3]) +" == " + str(obj_vertex_array[(obj_face_array[input_face]-1)*3]))
                    
                    print("DEBUG BELOW: " + str(compressed_obj_vertex_array[compressed_vertex_index*3]) +" == " +  str(obj_vertex_array[(obj_face_array[input_face]-2)*3]))
                    print("DEBUG ABOVE : " + str(compressed_obj_vertex_array[compressed_vertex_index*3]) +" == " + str(obj_vertex_array[(obj_face_array[input_face]-0)*3]))


            else: 
                print(Fore.RED +"ERROR - Blue Face Color Buffer corrupt: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
                print("DEBUG: " + str(obj_face_color_array[input_face*3]) +" == " + str(get_material_value_from_name(current_material, 'r')))
        else: 
            print(Fore.RED +"ERROR - Green Face Color Buffer corrupt: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
            print("DEBUG: " + str(obj_face_color_array[face_index*3+1]) +" == " + str(get_material_value_from_name(current_material, 'g')))













last_compression=0

#Copy to the new buffer at the correct new offset
compressed_vertex_index=0
#Controls write location of compressed face buffer
compressed_face_index=0
material_buffer_index=0

global global_compressed_face_buffer_index
global_compressed_face_buffer_index=0
global local_compressed_face_offset
local_compressed_face_offset=0
current_material=""
previous_material=""

compressed_index=0



global global_skip_list
global_skip_list=get_global_skip_list()
#print("GLOBAL SKIP LIST: "+global_skip_list)


for material_buffer_index in range(len(face_material_buffer.split("@"))-1):
    #print("###########################################################################################")

    #print("DEBUG - MATERIAL BUFFER INDEX: " + str(material_buffer_index+1))
    #print(str(face_material_buffer.split("@")[material_buffer_index+1]))

    if len(face_material_buffer.split("@")[material_buffer_index+1].split()) > 0:
        previous_material=current_material
        current_material=face_material_buffer.split("@")[material_buffer_index+1].split()[0]
        #print("DEBUG- SET MATERIASL - PREVIOUS: " + str(previous_material) + "  CURRENT: " + str(current_material))
    




    print("Calculating Compression Precursor:" +Fore.YELLOW + "[" +str(current_material) + "]" + Style.RESET_ALL)
    local_skip_list=get_material_local_skip_list(current_material)
    print("Compression Precursor for " + str(current_material) + ": " +Fore.GREEN + "[DONE]" + Style.RESET_ALL)
    #print("SKIP LIST: " + local_skip_list)
    #for skip_item in local_skip_list.split():
    	#print("SKIP: " + str(skip_item))
    #list for things we have already skipped

    compressed_index=0
    
    # 
    compression_factor_skip_index=0
    #for every item in vertex buffer

    #####################################
    # LOCAL AND GLOBAL OFFSET
    #####################################
    current_material_max=find_material_face_max(current_material)
    current_material_min=find_material_face_min(current_material)

    local_compressed_face_offset=current_material_min-1

    #setup offset
    if previous_material == "":
        global_compressed_face_buffer_index=0
        #print("DEBUG USING PREVIOUS MATERIAL:" +Fore.YELLOW + "[" +str(current_material) + "]" + Style.RESET_ALL)
    else:
        global_compressed_face_buffer_index+=(get_material_local_buffer_range(previous_material))+1
        #print("DEBUG MATERIAL BUFFER START INDEX:" +Fore.YELLOW + "[" +str(global_compressed_face_buffer_index) + "]" + Style.RESET_ALL)


    #####################################
    # NEW COMPRESSION FACTOR
    #####################################

    print("Building Compression Matrix:" +Fore.YELLOW + "[" +str(current_material) + "]" + Style.RESET_ALL)
    compression_factor_skip_index=0
    last_compression=0
    for face_index in range(current_material_min-1,current_material_max):
        if str(face_index) in local_skip_list.split():
            compression_factor_skip_index+=1
            last_compression=compression_factor_skip_index
        compression_factor[face_index] = int(last_compression)
    old_last_compression=int(last_compression)
    print("Compression Matrix: " + str(current_material) + ": " +Fore.GREEN + "[DONE]" + Style.RESET_ALL)
    #for index in range(len(compression_factor)):
       # print(compression_factor[index])


    #last_compression=0
    #for compression_factor_index in range(int(len(obj_vertex_array)/3)):
        #get position of number in skip vector
        #if the index is in the index buffer skip list
     #   if (" "+str(compression_factor_index)+" ") in local_skip_list:
            #print("DEBUG - SKIPPING: " + str(compression_factor_index))
       #     compression_factor_skip_index+=1
      #      last_compression=compression_factor_skip_index
            #print("DEBUG - ADDING TO BUFFER: " + "compression_factor[" + str(compression_factor_index) + "] = int("+str(compression_factor_skip_index)+")")
     #   compression_factor[compression_factor_index] = int(last_compression)












    

    #print("MIN VERTEX INDEX: "+ str(find_material_face_min(current_material)))
    #print("MAX VERTEX INDEX: "+ str(find_material_face_max(current_material)))
    #print("CURRENT MATERIAL: " + str(current_material))
    #print("SKIPLIST_SIZE: " + str(len(local_skip_list.split())))
    #print("Global Index: " +str(global_compressed_face_buffer_index))
    #print("Local Offset: " +str(local_compressed_face_offset))
    #print("STARTING OFFSET: " + str(current_material_min - local_compressed_face_offset + global_compressed_face_buffer_index - int(compression_factor[current_material_min - local_compressed_face_offset-1])-1 ))








    for face_index in range(int(len(obj_face_array))):

        compress_face(face_index,current_material)







global_compressed_face_buffer_index+=(get_material_local_buffer_range(previous_material))+1

compressed_buffer_sized_postprocess=global_compressed_face_buffer_index
#for face_index in range(int(len(compressed_obj_face_array)/3)):
#	print("FACE "+ str(face_index) + ": " + str(compressed_obj_face_array[face_index*3]) +"// "+str(compressed_obj_face_array[face_index*3+1]) +"// "+str(compressed_obj_face_array[face_index*3+2]) )


#print(str(compressed_obj_vertex_array))
#global_compressed_face_buffer_index+=(get_material_local_buffer_range(previous_material))+1
#for vertex_index in range(int(global_compressed_face_buffer_index)):
	#print("VERTEX " + str(vertex_index) + "  X: " + str(compressed_obj_vertex_array[vertex_index*3]) +"  Y: "+str(compressed_obj_vertex_array[vertex_index*3+1]) +"  Z: "+str(compressed_obj_vertex_array[vertex_index*3+2] ))



#print("REAL BUFFER")

#for vertex_index in range(int(len(obj_vertex_array)/3)):
    #print("VERTEX " + str(vertex_index) + "  X: " + str(obj_vertex_array[vertex_index*3]) +"  Y: "+str(obj_vertex_array[vertex_index*3+1]) +"  Z: "+str(obj_vertex_array[vertex_index*3+2] ))





        #Face 1
        #compressed_obj_face_array[index*3] = obj_face_array[index*3] - local_offset + global_offset

        #Face 2
        #obj_face_array[index*3+1]

        #Face 3
        #obj_face_array[index*3+2]

















########################################################################################################################################
#End Bake Data
########################################################################################################################################             

           
            

    
print("Object Info")

print("Number of Objects: "+Fore.GREEN + str(obj_count_preprocess)+Style.RESET_ALL)
for object_num in range(obj_count_preprocess):
    print("#######################################################")
    print("Object Number: " + str(object_num+1))
    print("Object Name: "+Fore.GREEN + str(obj_g1)+Style.RESET_ALL)
    print("Material: "+Fore.GREEN + str(obj_g2)+Style.RESET_ALL)
    print("Total Vertexs(v): "+Fore.GREEN +str(compressed_buffer_sized_postprocess)+Style.RESET_ALL)
    print("Total Normal(vn): "+Fore.GREEN +str(compressed_buffer_sized_postprocess)+Style.RESET_ALL)
    print("Total Faces(f): "+Fore.GREEN +str(len(compressed_obj_face_array)/3)+Style.RESET_ALL)

print("#######################################################")
#print("Vertex Data")
#for vertex_data in range(obj_vertex_count):
   # print("Vertex: " + str(vertex_data) + " X: " + str(obj_vertex_array[vertex_data*3]) + " Y: " + str(obj_vertex_array[vertex_data*3+1]) + " Z: " + str(obj_vertex_array[vertex_data*3+2]))
#for vertex_data in range(obj_vertex_count_vn):
    #print("Normal: " + str(vertex_data) + " X: " + str(obj_normal_array[vertex_data*3]) + " Y: " + str(obj_normal_array[vertex_data*3+1]) + " Z: " + str(obj_normal_array[vertex_data*3+2]))
#for vertex_data in range(obj_vertex_count_f):
    #print("Face " + str(vertex_data) + ": " + str(obj_face_array[vertex_data*3]) + " " + str(obj_face_array[vertex_data*3+1]) + " " + str(obj_face_array[vertex_data*3+2]))








bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2+len(index_buffer)+vertex_count*24)
progress_bar_count=0


########################################################################################################################################
#WRITE SIMPLE ASSET FILE
########################################################################################################################################

if asset_type == "simple":

    new_asset_file_name=str(sys.argv[2]).split(".")[0] + "_GooseTools_Compiled"+str(obj_g1)+".asset"
    print(new_asset_file_name)
    new_asset = open(new_asset_file_name, "w")

    #return to beggining of file
    asset_file.seek(0)
    YAML_LINE = asset_file.readlines()
    for line in YAML_LINE:
        if "m_Name:" in line:
            new_asset.write("  m_Name: "+ asset_name+ "\n")
            print("Writting Asset Name: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_VertexCount:" in line:
            new_asset.write("    m_VertexCount: "+ str(compressed_buffer_sized_postprocess)+ "\n")
            print("Writting Vertex Count Main: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "    vertexCount: " in line:
            new_asset.write("    vertexCount: "+ str(compressed_buffer_sized_postprocess)+ "\n")
            print("Writting Vertex Count Sub: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "indexCount" in line:
            new_asset.write("    indexCount: "+ str(obj_face_count_preprocess*3)+ "\n")
            print("Writting Index Count: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_IndexBuffer:" in line:

            new_asset.write("  m_IndexBuffer: ")
            for byte in range(obj_face_count_preprocess):
                
                #print("DEBUG: BYTE: " + str(byte*3) + " FACE INDEX: " + str(compressed_obj_face_array[byte*3]-1))
                #print("DEBUG: BYTE: " + str(byte*3+1) + " FACE INDEX: " + str(compressed_obj_face_array[byte*3+1]-1))
                #print("DEBUG: BYTE: " + str(byte*3+2) + " FACE INDEX: " + str(compressed_obj_face_array[byte*3+2]-1))







                byte1 =format(compressed_obj_face_array[byte*3]-1,"04x")
                #print("Byte1: " + str(byte1))
                #print("First: " +str(byte1[:2]))
                #print("Second: " +str(byte1[-2:]))

                byte2 =format(compressed_obj_face_array[byte*3+1]-1,"04x")
                #print("Byte2: " + str(byte2))
                #print("First: " +str(byte2[:2]))
                #print("Second: " +str(byte2[-2:]))

                byte3 =format(compressed_obj_face_array[byte*3+2]-1,"04x")
                #print("Byte3: " + str(byte3))
                #print("First: " +str(byte3[:2]))
                #print("second: " +str(byte3[-2:]))

                #write first byte first
                new_asset.write(str(byte1[-2:])+str(byte1[:2]))
                new_asset.write(str(byte2[-2:])+str(byte2[:2]))
                new_asset.write(str(byte3[-2:])+str(byte3[:2]))

 



                #Swapped face index buffer
                #new_asset.write(str(byte3[-2:])+str(byte3[:2]))
                #new_asset.write(str(byte2[-2:])+str(byte2[:2]))        
                #new_asset.write(str(byte1[-2:])+str(byte1[:2])) 



            new_asset.write("\n")
            print("Writting Index Buffer: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "m_DataSize:" in line:
            new_asset.write("    m_DataSize: "+ str(int(compressed_buffer_sized_postprocess)*44)+"\n")
            print("    m_DataSize: "+ str(obj_vertex_count_preprocess*44)+"\n")
            print("Writting Vertex Buffer Data Size: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "_typelessdata:" in line:
            print("Typeless Data")
            new_asset.write("    _typelessdata: ")


            #Default for now is 44 bytes
            loop_byte = vertex_buffer_block_size
            loop_count=0
            vertex_decode="POS"
            for vertex_pointer in range(compressed_buffer_sized_postprocess):
                #print(str(vertex_pointer))
                #Write Vertex
                if vertex_decode=="POS":
                    #print("Writing Vector: " + str(vertex_pointer) +" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_vertex_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_vertex_array[vertex_pointer*3])))


                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3+2])))



                    vertex_decode="NORM"
                #Write Normals
                if vertex_decode=="NORM":
                    #print("Writing Normal: " + str(vertex_pointer)+" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_normal_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3+2])))
                    #new_asset.write("00000000")
                    #new_asset.write("00000000")
                    #new_asset.write("00000000")
                    vertex_decode="UV"

                #write "Other" data
                #put color stuff here when decoded
                #Write Normals
                if vertex_decode=="UV":
                    #print("Writing UV: " + str(vertex_pointer)+" Loop: " + str(loop_count))
                    #just copy from source asset since its not decoded yet
                    data_position=int(vertex_pointer*vertex_buffer_block_size*2+48)

                    #for index in range(32):
                    #    new_asset.write(vertex_buffer[data_position+index])
                    new_asset.write("0000803F0000000000000000000080BF")                    
                    vertex_decode="COLOR"
    





#####################################################   
#write color data

                #Write Model Colors
                if vertex_decode=="COLOR":


                    color_red_hex=hex(int(compressed_obj_vertex_color_array[vertex_pointer*3]*255)).split("x")[1]
                    color_green_hex=hex(int(compressed_obj_vertex_color_array[vertex_pointer*3+1]*255)).split("x")[1]
                    color_blue_hex=hex(int(compressed_obj_vertex_color_array[vertex_pointer*3+2]*255)).split("x")[1]
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





                    #default blue
                    #new_asset.write("63AAC2FF")
                    #print("COLOR: " +str(color_red_hex) + str(color_green_hex)+ str(color_blue_hex) + "ff")
                    new_asset.write(str(color_red_hex) + str(color_green_hex)+ str(color_blue_hex) + "ff")






                    vertex_decode="POS"
 #End write color                   
#####################################################








                if loop_count == loop_byte:
                    #print("Loop count reset")
                    vertex_decode="POS"
                    loop_count=0
                loop_count+=1
            new_asset.write("\n")












            print("Writting Vertex Buffer: "+Fore.GREEN + "[COMPLETE]" +Style.RESET_ALL)
        #Write rest of file. Soon to be depreciated
        #new_asset.write(object_footer)
        else:
            new_asset.write(line)




########################################################################################################################################
#WRITE COMPLEX ASSET FILE
########################################################################################################################################

elif asset_type == "complex":

    new_asset_file_name=str(sys.argv[2]).split(".")[0] + "_GooseTools_Compiled"+str(obj_g1)+".asset"
    print(new_asset_file_name)
    new_asset = open(new_asset_file_name, "w")

    #return to beggining of file
    asset_file.seek(0)
    YAML_LINE = asset_file.readlines()
    for line in YAML_LINE:
        if "m_Name:" in line:
            new_asset.write("  m_Name: "+ asset_name+ "\n")
            print("Writting Asset Name: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_VertexCount:" in line:
            new_asset.write("    m_VertexCount: "+ str(int(obj_vertex_count_preprocess))+ "\n")
            print("Writting Vertex Count Main: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "    vertexCount: " in line:
            new_asset.write("    vertexCount: "+ str(int(obj_vertex_count_preprocess))+ "\n")
            print("Writting Vertex Count Sub: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "indexCount" in line:
            new_asset.write("    indexCount: "+ str(obj_face_count_preprocess*3)+ "\n")
            print("Writting Index Count: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_IndexBuffer:" in line:

            new_asset.write("  m_IndexBuffer: ")
            for byte in range(obj_face_count_preprocess):
                
                #print("DEBUG: BYTE: " + str(byte*3) + " FACE INDEX: " + str(obj_face_array[byte*3]-1))
                #print("DEBUG: BYTE: " + str(byte*3+1) + " FACE INDEX: " + str(obj_face_array[byte*3+1]-1))
               # print("DEBUG: BYTE: " + str(byte*3+2) + " FACE INDEX: " + str(obj_face_array[byte*3+2]-1))
                byte1 =format(obj_face_array[byte*3]-1,"04x")
                #print("Byte1: " + str(byte1))
                #print("First: " +str(byte1[:2]))
                #print("Second: " +str(byte1[-2:]))

                byte2 =format(obj_face_array[byte*3+1]-1,"04x")
                #print("Byte2: " + str(byte2))
                #print("First: " +str(byte2[:2]))
                #print("Second: " +str(byte2[-2:]))

                byte3 =format(obj_face_array[byte*3+2]-1,"04x")
                #print("Byte3: " + str(byte3))
                #print("First: " +str(byte3[:2]))
                #print("second: " +str(byte3[-2:]))

                #write first byte first





                new_asset.write(str(byte3[-2:])+str(byte3[:2]))
                new_asset.write(str(byte2[-2:])+str(byte2[:2]))
                new_asset.write(str(byte1[-2:])+str(byte1[:2])) 



                #Swapped face index buffer
                #new_asset.write(str(byte3[-2:])+str(byte3[:2]))
                #new_asset.write(str(byte2[-2:])+str(byte2[:2]))        
                #new_asset.write(str(byte1[-2:])+str(byte1[:2])) 



            new_asset.write("\n")
            print("Writting Index Buffer: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "m_DataSize:" in line:
            new_asset.write("    m_DataSize: "+ str(typeless_data_buffer_size)+"\n")
            print("    m_DataSize: "+ str(typeless_data_buffer_size)+"\n")
            print("Writting Vertex Buffer Data Size: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "_typelessdata:" in line:
            print("Typeless Data")
            new_asset.write("    _typelessdata: ")




            ##############################
            #WRITE BLOCK 1 - VERTEX , NORMAL, UNKNOWN
            ##############################
            #Default for now is 44 bytes
            loop_byte = vertex_buffer_block_size
            loop_count=0
            vertex_decode="POS"
            for vertex_pointer in range(compressed_buffer_sized_postprocess):
                #print(str(vertex_pointer))
                #Write Vertex
                if vertex_decode=="POS":
                    #print("Writing Vector: " + str(vertex_pointer) +" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_vertex_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_vertex_array[vertex_pointer*3])))


                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(compressed_obj_vertex_array[vertex_pointer*3+2])))



                    vertex_decode="NORM"
                #Write Normals
                if vertex_decode=="NORM":
                    #print("Writing Normal: " + str(vertex_pointer)+" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_normal_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(compressed_obj_normal_array[vertex_pointer*3+2])))
                    #new_asset.write("00000000")
                    #new_asset.write("00000000")
                    #new_asset.write("00000000")
                    vertex_decode="UV"

                #write "Other" data
                #put color stuff here when decoded
                #Write Normals
                if vertex_decode=="UV":


                    #for index in range(32):
                    #    new_asset.write(vertex_buffer[data_position+index])
                    new_asset.write("0000803F0000000000000000000080BF")                    
                    vertex_decode="POS"
    




            ##############################
            #WRITE BLOCK 2 - UV, COLOR
            ##############################
            vertex_decode="UV"
            for vertex_pointer in range(compressed_buffer_sized_postprocess):


                if vertex_decode=="UV":
                    #Dont write any UV data for now
                    new_asset.write("0000000000000000")  
                    vertex_decode="COLOR"
                #Write Model Colors
                if vertex_decode=="COLOR":


                    color_red_hex=hex(int(compressed_obj_vertex_color_array[(vertex_pointer)*3]*255)).split("x")[1]
                    color_green_hex=hex(int(compressed_obj_vertex_color_array[(vertex_pointer)*3+1]*255)).split("x")[1]
                    color_blue_hex=hex(int(compressed_obj_vertex_color_array[(vertex_pointer)*3+2]*255)).split("x")[1]



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





                    #default blue
                    #new_asset.write("63AAC2FF")

                    new_asset.write(str(color_red_hex) + str(color_green_hex)+ str(color_blue_hex) + "ff")


                    vertex_decode="UV"
 #End write color                   
#####################################################










            ##############################
            #WRITE BLOCK 3 - 12 Bytes of Data
            ##############################
            for vertex_pointer in range(24):
                new_asset.write(str(vertex_buffer[obj_vertex_count_preprocess*80+obj_vertex_count_preprocess*24+vertex_pointer]))

            ##############################
            #WRITE BLOCK 4 - BONE DATA
            ##############################

            vertex_decode="UV"
            for vertex_pointer in range(obj_vertex_count_preprocess*64):
                new_asset.write(str(vertex_buffer[obj_vertex_count_preprocess*80+obj_vertex_count_preprocess*24+24+vertex_pointer]))







            new_asset.write("\n")
            print("Writting Vertex Buffer: "+Fore.GREEN + "[COMPLETE]" +Style.RESET_ALL)


        else:
            new_asset.write(line)







else:
    print(Fore.RED + "Script Terminated. One or more Errors has prevented the asset from compiling" +Style.RESET_ALL)











#close all the files
object_file.close()
asset_file.close()


















                

