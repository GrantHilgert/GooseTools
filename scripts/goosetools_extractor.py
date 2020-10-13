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

#Init Colorama
init()

print("GooseTool's Complex Asset Utility")
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
# long 1: Unknown
# long 2: Unknown
# long 3: Unknown
# long 4: Unknown
# long 5: Unknown
# long 6: Unknown
# long 7: Unknown
# long 8: Unknown



########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################



#Returns whether the asset is simple(i.g. Pumpkin) or has bone(i.g. Goose)
def get_asset_type(num_of_vertex, size_of_vertex_buffer,bone_count):
 

    # Complex Structure (Type-B)
    

    complex_vertex_buffer_size=40*num_of_vertex
    complex_color_buffer_size=12*num_of_vertex
    complex_bone_buffer_size=32*num_of_vertex
    complex_bone_lable_size=12
    complex_buffer_combined_size=complex_vertex_buffer_size+complex_color_buffer_size+complex_bone_buffer_size 

    if (complex_buffer_combined_size == size_of_vertex_buffer) and bone_count > 0: 

        print("Model Structure: "+ Fore.YELLOW + "[NPC]" +Style.RESET_ALL)        
        return "npc"
    

    elif (complex_buffer_combined_size + complex_bone_lable_size == size_of_vertex_buffer) and (bone_count > 0): 

        print("Model Structure: "+ Fore.YELLOW + "[GOOSE]" +Style.RESET_ALL)        
        return "goose"

    # Simple Structure (Type-A)
    elif (size_of_vertex_buffer/num_of_vertex).is_integer():
        print("Model Structure: "+ Fore.YELLOW + "[SIMPLE]" +Style.RESET_ALL)
        return "simple"

        #This buffer is something else and we cant decode it, throw an error.
    else:
        print("Model Structure: "+ Fore.RED + "[UNKNOWN]" +Style.RESET_ALL) 
        return "fail"





#Creates a blender friendly material name
def get_material_name(raw_material_data):

    return "ugg_material.00"+ str(material_count_index)



global material_vertex_count_array
material_vertex_count_array=""


current_material_count=0
def get_material_list(num_of_vertex, size_of_vertex_buffer,bone_count):
    asset_type=get_asset_type(num_of_vertex, size_of_vertex_buffer,bone_count)
    global material_vertex_count_array
    material_vertex_count_array=""
    
    global material_vertex_start_array
    material_vertex_start_array="0 "

    already_counted_vertex_array=""

    temp_material_list=""
    current_material=""
    previous_material=""
    current_material_count=0
    if asset_type == "simple":
        for vertex in range(num_of_vertex):
            
            current_material_buffer = get_simple_obj_color_hex(vertex, num_of_vertex)
            current_material=current_material_buffer.split()[0] + current_material_buffer.split()[1] + current_material_buffer.split()[2] + "ff"
            
            if previous_material.strip() != current_material.strip() and previous_material.strip() != "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                #print("DEBUG - VERTEX: "+str(vertex))
                temp_material_list+=current_material + " "
                material_vertex_count_array+=str(current_material_count) + " "
                material_vertex_start_array+=str(vertex) + " "
                current_material_count=0
            elif previous_material == "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                temp_material_list+=current_material + " "
            else:
                

                current_material_count+=1              
            previous_material=current_material            
        material_vertex_start_array+=str(num_of_vertex) + " "
        material_vertex_count_array+=str(current_material_count) + " "

                

    
    elif (asset_type == "goose"):
        for vertex in range(num_of_vertex):
            
            current_material_buffer = get_obj_color_hex(vertex, num_of_vertex)
            current_material=current_material_buffer.split()[0] + current_material_buffer.split()[1] + current_material_buffer.split()[2] + "ff"
            #print("VERTEX: " + str(vertex) + " COLOR: " +str(current_material))
            if previous_material.strip() != current_material.strip() and previous_material.strip() != "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                #print("DEBUG - VERTEX: "+str(vertex))
                temp_material_list+=current_material + " "
                material_vertex_count_array+=str(current_material_count) + " "
                material_vertex_start_array+=str(vertex) + " "
                current_material_count=1
            elif previous_material == "":
                print("Processing Initial Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                temp_material_list+=current_material + " "
                previous_material=current_material
                current_material_count=1
            else:
                current_material_count+=1              
            previous_material=current_material  
        material_vertex_start_array+=str(num_of_vertex) + " "
        material_vertex_count_array+=str(current_material_count) + " "

    elif (asset_type == "npc"):
        for vertex in range(num_of_vertex):
            
            current_material_buffer = get_obj_npc_color_hex(vertex, num_of_vertex)
            current_material=current_material_buffer.split()[0] + current_material_buffer.split()[1] + current_material_buffer.split()[2] + "ff"
            #print("VERTEX: " + str(vertex) + " COLOR: " +str(current_material))
            if previous_material.strip() != current_material.strip() and previous_material.strip() != "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                #print("DEBUG - VERTEX: "+str(vertex))
                temp_material_list+=current_material + " "
                material_vertex_count_array+=str(current_material_count) + " "
                material_vertex_start_array+=str(vertex) + " "
                current_material_count=1
            elif previous_material == "":
                print("Processing Initial Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                temp_material_list+=current_material + " "
                previous_material=current_material
                current_material_count=1
            else:
                current_material_count+=1              
            previous_material=current_material  
        material_vertex_start_array+=str(num_of_vertex) + " "
        material_vertex_count_array+=str(current_material_count) + " "



    else:
        print("ERROR - Could not get material list: "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)


    return temp_material_list


def generate_material_name(index):
    if len(str(index)) == 1:
        return "ugg_material.00"+ str(index)
    elif len(str(index)) == 2:
        return "ugg_material.0"+ str(index) 
    elif len(str(index)) == 3:
        return "ugg_material."+ str(index) 
    else:
        print("ERROR - Could not generate material name: "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)            
        return "defaultMaterial"


def get_material_vertex_count(index):
    if len(material_vertex_count_array) > index:
        return material_vertex_count_array.split()[index]
    else:
        print("ERROR - MATERIAL INDEX OUT OF RANGE")
        print("ARRAY: " + str(material_vertex_count_array))
        return str(0)

#######################
# COMPLEX ASSETS
#######################

def get_complex_vertex_buffer_block_size():
    return 40
def get_complex_vertex_buffer_size(vertex_count):
    return vertex_count*get_complex_vertex_buffer_block_size()

def get_complex_color_buffer_block_size():
    return 12
def get_complex_color_buffer_size(vertex_count):
    return vertex_count*get_complex_color_buffer_block_size()

def get_complex_bone_buffer_block_size():
    return 32
def get_complex_bone_buffer_size(vertex_count):
    return vertex_count*get_complex_bone_buffer_block_size()
  

# returns #num1 #num2 #num3
# face_number is zero indexed
def get_obj_face(face_number):

    f=face_number
    vertex_1=index_buffer[f*12+10] + index_buffer[f*12+11] + index_buffer[f*12+8] + index_buffer[f*12+9]
    vertex_2=index_buffer[f*12+6] + index_buffer[f*12+7] + index_buffer[f*12+4] + index_buffer[f*12+5]
    vertex_3=index_buffer[f*12+2] + index_buffer[f*12+3] + index_buffer[f*12+0] + index_buffer[f*12+1]

    return str(int(vertex_1,16)) + " " + str(int(vertex_2,16)) + " " + str(int(vertex_3,16))



def get_obj_vertex(vertex_number,vertex_buffer_size):
    v=vertex_number*get_complex_vertex_buffer_block_size()*2   
    word_vertex_x=vertex_buffer[v]+vertex_buffer[v+1]+vertex_buffer[v+2]+vertex_buffer[v+3]+vertex_buffer[v+4]+vertex_buffer[v+5]+vertex_buffer[v+6]+vertex_buffer[v+7]
    word_vertex_y=vertex_buffer[v+8]+vertex_buffer[v+9]+vertex_buffer[v+10]+vertex_buffer[v+11]+vertex_buffer[v+12]+vertex_buffer[v+13]+vertex_buffer[v+14]+vertex_buffer[v+15]
    word_vertex_z=vertex_buffer[v+16]+vertex_buffer[v+17]+vertex_buffer[v+18]+vertex_buffer[v+19]+vertex_buffer[v+20]+vertex_buffer[v+21]+vertex_buffer[v+22]+vertex_buffer[v+23]

    float_vertex_x=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_x))).strip('(),')),7)
    float_vertex_y=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_y))).strip('(),')),7)
    float_vertex_z=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_z))).strip('(),')),7)

    return str(float_vertex_x) + " " + str(float_vertex_y) + " " + str(float_vertex_z)



def get_obj_normal(vertex_number,vertex_buffer_size):
    v=vertex_number*get_complex_vertex_buffer_block_size()*2   
    word_normal_x=vertex_buffer[v+24]+vertex_buffer[v+25]+vertex_buffer[v+26]+vertex_buffer[v+27]+vertex_buffer[v+28]+vertex_buffer[v+29]+vertex_buffer[v+30]+vertex_buffer[v+31]
    word_normal_y=vertex_buffer[v+32]+vertex_buffer[v+33]+vertex_buffer[v+34]+vertex_buffer[v+35]+vertex_buffer[v+36]+vertex_buffer[v+37]+vertex_buffer[v+38]+vertex_buffer[v+39]
    word_normal_z=vertex_buffer[v+40]+vertex_buffer[v+41]+vertex_buffer[v+42]+vertex_buffer[v+43]+vertex_buffer[v+44]+vertex_buffer[v+45]+vertex_buffer[v+46]+vertex_buffer[v+47]

    float_normal_x=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_x))).strip('(),')),7)
    float_normal_y=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_y))).strip('(),')),7)
    float_normal_z=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_z))).strip('(),')),7)

    return str(float_normal_x) + " " + str(float_normal_y) + " " + str(float_normal_z)


def get_obj_uv(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)+vertex_number*get_complex_color_buffer_block_size()*2 
    word_s=vertex_buffer[v]+vertex_buffer[v+1]+vertex_buffer[v+2]+vertex_buffer[v+3]+vertex_buffer[v+4]+vertex_buffer[v+5]+vertex_buffer[v+6]+vertex_buffer[v+7]
    word_t=vertex_buffer[v+8]+vertex_buffer[v+9]+vertex_buffer[v+10]+vertex_buffer[v+11]+vertex_buffer[v+12]+vertex_buffer[v+13]+vertex_buffer[v+14]+vertex_buffer[v+15]

    float_s=round(float(str(struct.unpack('f', bytes.fromhex(word_s))).strip('(),')),7)
    float_t=round(float(str(struct.unpack('f', bytes.fromhex(word_t))).strip('(),')),7)

    return str(float_s) + " " + str(float_t)

def get_obj_color(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
    
    byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]


    #error check
    color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]

    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
    normalized_red=(int(byte_red,16))/255
    normalized_green=(int(byte_green,16))/255
    normalized_blue=(int(byte_blue,16))/255

    return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)



def get_obj_color_hex(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
    #print("DEBUG - V: " + str(v))
    byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]
    #error check


    color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]

    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)





def get_obj_bone_root(vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)*2+get_complex_color_buffer_size(vertex_buffer_size)*2
    temp_string=""
    for index in range(24):
        temp_string+=vertex_buffer[v+index]
    return str(temp_string)

def get_obj_bone_buffer(vertex_number,vertex_buffer_size):
    v=(get_complex_vertex_buffer_size(vertex_buffer_size)*2+get_complex_color_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_bone_buffer_block_size()*2)+24
    temp_string=""
    for index in range(get_complex_bone_buffer_block_size()*2):
        temp_string+=vertex_buffer[v+index]
    return str(temp_string)





def get_obj_vertex_weight(weight_position,vertex_number,num_of_vertex,asset_type):
    bone_weight_string=""
    bone_num_string=""
    if ((asset_type == "npc") or (asset_type == "goose")) and weight_position < 4:

        if asset_type == "npc":
            v=(get_complex_vertex_buffer_size(num_of_vertex)*2+get_complex_color_buffer_size(num_of_vertex)*2)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position  	
        elif asset_type == "goose":
            unknown_goose_data=24
            v=(get_complex_vertex_buffer_size(num_of_vertex)*2+get_complex_color_buffer_size(num_of_vertex)*2+unknown_goose_data)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position

        for bone_char_index in range(8):
            bone_weight_string+=vertex_buffer[v+bone_char_index]

        for bone_num_char_index in range(8):
            bone_num_string+=vertex_buffer[v+bone_num_char_index+32]

        bone_num_byte_1=bone_num_string[0]+bone_num_string[1]
        bone_num_byte_2=bone_num_string[2]+bone_num_string[3]
        bone_num_byte_3=bone_num_string[4]+bone_num_string[5] 
        bone_num_byte_4=bone_num_string[6]+bone_num_string[7]

        bone_num_hex=bone_num_byte_4+bone_num_byte_3+bone_num_byte_2+bone_num_byte_1
        bone_num_int=int(bone_num_hex,16)


        vertex_weight=round(float(str(struct.unpack('f', bytes.fromhex(bone_weight_string))).strip('(),')),7)

        if bone_num_int == 0 and vertex_weight == 0:
            return "0 0.0"

        return str(bone_num_int+1) + " " +str(vertex_weight)
        #print("VERTEX: "+ Fore.CYAN +str(vertex_number)+Style.RESET_ALL + " BONE: "+ Fore.YELLOW + str(bone_num_int)+Style.RESET_ALL + " WEIGHT: " + Fore.GREEN+str(vertex_weight)+Style.RESET_ALL)

    else:
        print(Fore.RED + "ERROR: Asset type: " + str(asset_type) + " has no vertex weight." +Style.RESET_ALL)   		
        return ""

def get_obj_vertex_weight_count(vertex_number,num_of_vertex,asset_type):
    if ((asset_type == "npc") or (asset_type == "goose")):
        for weight_position in range(4):
            bone_weight_string=""
            bone_num_string=""
            if asset_type == "npc":
                v=(get_complex_vertex_buffer_size(num_of_vertex)*2+get_complex_color_buffer_size(num_of_vertex)*2)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position   
            elif asset_type == "goose":
                unknown_goose_data=24
                v=(get_complex_vertex_buffer_size(num_of_vertex)*2+get_complex_color_buffer_size(num_of_vertex)*2+unknown_goose_data)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position

            for bone_char_index in range(8):
                bone_weight_string+=vertex_buffer[v+bone_char_index]

            for bone_num_char_index in range(8):
                bone_num_string+=vertex_buffer[v+bone_num_char_index+32]

            bone_num_byte_1=bone_num_string[0]+bone_num_string[1]
            bone_num_byte_2=bone_num_string[2]+bone_num_string[3]
            bone_num_byte_3=bone_num_string[4]+bone_num_string[5] 
            bone_num_byte_4=bone_num_string[6]+bone_num_string[7]

            bone_num_hex=bone_num_byte_4+bone_num_byte_3+bone_num_byte_2+bone_num_byte_1
            bone_num_int=int(bone_num_hex,16)

            #print("DEBUG = BONE WEIGHT STRING: " + str(bone_weight_string))
            vertex_weight=round(float(str(struct.unpack('f', bytes.fromhex(bone_weight_string))).strip('(),')),7)

            if vertex_weight == 0 and bone_num_int == 0:
                return weight_position    
        return 4
    else:
        print(Fore.RED + "ERROR: Asset type: " + str(asset_type) + " has no vertex weight [Weight Count]." +Style.RESET_ALL)           
        return ""




def get_bone_hash(bone_number,bone_count):
    temp_string=""
    temp_index=bone_number*int(len(bone_name_hash)/bone_count)
    for bone_hash_string_index in range(int(len(bone_name_hash)/bone_count)):
        temp_string+=bone_name_hash[temp_index+bone_hash_string_index]
    
    return str(temp_string)


def get_bone_name_buffer(bone_count):
    temp_bone_name_buffer="Body_Armature_Bone "
    for bone_index in range(bone_count):
        temp_bone_name_buffer+="Body_Armature_Bone_"+str("{0:0=3d}".format(bone_index)) + " "
    return temp_bone_name_buffer


def get_bone_name(bone_number,bone_count):
    if bone_number == 1:
        temp_bone_name="Body_Armature_Bone "
    elif bone_number <= bone_count:
        temp_bone_name+="Body_Armature_Bone_"+str("{0:0=2d}".format(bone_number)) + " "
    return temp_bone_name



#######################
# NPC ASSETS
#######################


def get_obj_npc_color_hex(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
    #print("DEBUG - V: " + str(v))
    #byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    #byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    #byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]
    #error check

    byte_red=vertex_buffer[v]+vertex_buffer[v+1]
    byte_green=vertex_buffer[v+2]+vertex_buffer[v+3]
    byte_blue=vertex_buffer[v+4]+vertex_buffer[v+5]
    #error check
    #color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]
    color_terminator=vertex_buffer[v+6]+vertex_buffer[v+7]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)



def get_obj_npc_color(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
    
    #byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    #byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    #byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]

    byte_red=vertex_buffer[v]+vertex_buffer[v+1]
    byte_green=vertex_buffer[v+2]+vertex_buffer[v+3]
    byte_blue=vertex_buffer[v+4]+vertex_buffer[v+5]
    #error check
    #color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]
    color_terminator=vertex_buffer[v+6]+vertex_buffer[v+7]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
    normalized_red=(int(byte_red,16))/255
    normalized_green=(int(byte_green,16))/255
    normalized_blue=(int(byte_blue,16))/255

    return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)

def get_obj_npc_bone_buffer(vertex_number,vertex_buffer_size):
    v=(get_complex_vertex_buffer_size(vertex_buffer_size)*2+get_complex_color_buffer_size(vertex_buffer_size)*2+vertex_number*get_complex_bone_buffer_block_size()*2)
    temp_string=""
    for index in range(get_complex_bone_buffer_block_size()*2):
        temp_string+=vertex_buffer[v+index]
    return str(temp_string)













#######################
# SIMPLE ASSETS
#######################

def get_simple_vertex_buffer_block_size():
    return 44


def get_simple_obj_vertex(vertex_number,vertex_buffer_size):
    v=vertex_number*get_simple_vertex_buffer_block_size()*2   
    word_vertex_x=vertex_buffer[v]+vertex_buffer[v+1]+vertex_buffer[v+2]+vertex_buffer[v+3]+vertex_buffer[v+4]+vertex_buffer[v+5]+vertex_buffer[v+6]+vertex_buffer[v+7]
    word_vertex_y=vertex_buffer[v+8]+vertex_buffer[v+9]+vertex_buffer[v+10]+vertex_buffer[v+11]+vertex_buffer[v+12]+vertex_buffer[v+13]+vertex_buffer[v+14]+vertex_buffer[v+15]
    word_vertex_z=vertex_buffer[v+16]+vertex_buffer[v+17]+vertex_buffer[v+18]+vertex_buffer[v+19]+vertex_buffer[v+20]+vertex_buffer[v+21]+vertex_buffer[v+22]+vertex_buffer[v+23]

    float_vertex_x=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_x))).strip('(),')),7)
    float_vertex_y=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_y))).strip('(),')),7)
    float_vertex_z=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_z))).strip('(),')),7)

    return str(float_vertex_x) + " " + str(float_vertex_y) + " " + str(float_vertex_z)



def get_simple_obj_normal(vertex_number,vertex_buffer_size):
    v=vertex_number*get_simple_vertex_buffer_block_size()*2   
    word_normal_x=vertex_buffer[v+24]+vertex_buffer[v+25]+vertex_buffer[v+26]+vertex_buffer[v+27]+vertex_buffer[v+28]+vertex_buffer[v+29]+vertex_buffer[v+30]+vertex_buffer[v+31]
    word_normal_y=vertex_buffer[v+32]+vertex_buffer[v+33]+vertex_buffer[v+34]+vertex_buffer[v+35]+vertex_buffer[v+36]+vertex_buffer[v+37]+vertex_buffer[v+38]+vertex_buffer[v+39]
    word_normal_z=vertex_buffer[v+40]+vertex_buffer[v+41]+vertex_buffer[v+42]+vertex_buffer[v+43]+vertex_buffer[v+44]+vertex_buffer[v+45]+vertex_buffer[v+46]+vertex_buffer[v+47]

    float_normal_x=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_x))).strip('(),')),7)
    float_normal_y=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_y))).strip('(),')),7)
    float_normal_z=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_z))).strip('(),')),7)

    return str(float_normal_x) + " " + str(float_normal_y) + " " + str(float_normal_z)


def get_simple_obj_uv(vertex_number,vertex_buffer_size):
    #This probably isnt correct.
    v=vertex_number*get_simple_vertex_buffer_block_size()*2 
    word_s=vertex_buffer[v+48]+vertex_buffer[v+49]+vertex_buffer[v+50]+vertex_buffer[v+51]+vertex_buffer[v+52]+vertex_buffer[v+53]+vertex_buffer[v+54]+vertex_buffer[v+55]
    word_t=vertex_buffer[v+56]+vertex_buffer[v+57]+vertex_buffer[v+58]+vertex_buffer[v+59]+vertex_buffer[v+60]+vertex_buffer[v+61]+vertex_buffer[v+62]+vertex_buffer[v+63]

    float_s=round(float(str(struct.unpack('f', bytes.fromhex(word_s))).strip('(),')),7)
    float_t=round(float(str(struct.unpack('f', bytes.fromhex(word_t))).strip('(),')),7)

    return str(float_s) + " " + str(float_t)


def get_simple_obj_color(vertex_number,vertex_buffer_size):
    v=vertex_number*get_simple_vertex_buffer_block_size()*2
    
    byte_red=vertex_buffer[v+80]+vertex_buffer[v+81]
    byte_green=vertex_buffer[v+82]+vertex_buffer[v+83]
    byte_blue=vertex_buffer[v+84]+vertex_buffer[v+85]
    #error check
    color_terminator=vertex_buffer[v+86]+vertex_buffer[v+87]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
    normalized_red=(int(byte_red,16))/255
    normalized_green=(int(byte_green,16))/255
    normalized_blue=(int(byte_blue,16))/255

    return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)

def get_simple_obj_color_hex(vertex_number,vertex_buffer_size):
    v=vertex_number*get_simple_vertex_buffer_block_size()*2
    
    byte_red=vertex_buffer[v+80]+vertex_buffer[v+81]
    byte_green=vertex_buffer[v+82]+vertex_buffer[v+83]
    byte_blue=vertex_buffer[v+84]+vertex_buffer[v+85]
    #error check
    color_terminator=vertex_buffer[v+86]+vertex_buffer[v+87]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)

















########################################################################################################################################
# PREPROCESS ASSET 
########################################################################################################################################


material_count_index=0
material_count=0
#open asset file from command line
asset_file = open(sys.argv[1], "r")

YAML_LINE = asset_file.readlines()


global asset_name
global index_count
global vertex_count
global vertex_buffer
global index_buffer
global bone_name_hash

asset_name='NA'
index_count='NA'
vertex_count='NA'
index_buffer=''
vertex_buffer='NA'
vertex_buffer_size='NA'
vertex_buffer_block_size='NA'


bind_pose_buffer=''
bind_pos_matrix_count=0
bind_pose_flag=0
bind_pose_complete=0

bone_name_hash=""
root_bone_name_hash=""
matrix_row=0
matrix_col=0

count=0
#comb through file, line by line
print("Reading Mesh File...")
for line in YAML_LINE: 
    #print("Line{}: {}".format(count, line.strip()))
    
    ##############BIND POSE PARSER############
        #Copy Bind Pose Data
    if "m_BindPose:" in line:
        if "m_BindPose: []" in line:
            print("Bind Pose Buffer"+ Fore.YELLOW + "[NO DATA]" +Style.RESET_ALL)           
        elif "m_BindPose:" in line:
            bind_pose_flag=1

    if "m_BoneNameHashes:" in line:
        if len(line.strip().split(":")) > 1:
            bone_name_hash=str(line.strip().split(":")[1]).strip()
            bind_pose_complete=1
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
    if bind_pose_flag == 1 and bind_pose_complete != 1:   
        if len(str(str(line).split("e")[1].split(":")[0].strip())) > 0:
            if str(str(line).split("e")[1].split(":")[0].strip())[0].isdigit():
                matrix_id=int(str(matrix_col)+str(matrix_row))
                test_value=int(str(line).split("e")[1].split(":")[0].strip())
                if int(matrix_id) == int(test_value):
                    bind_pose_buffer+=line.split(":")[1].strip()+" "
                    matrix_row+=1
                if matrix_row == 4:
                    matrix_row = 0
                    matrix_col+=1
                if matrix_col == 4:
                    matrix_row=0
                    matrix_col=0
                    bind_pos_matrix_count+=1


        #print("DEBUG - BIND POSE MATRIX")
        #bind_pose_buffer=str(line.split(":", maxsplit=1)[1].strip())




print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)
print("Bind Pose Count: "+ Fore.GREEN +str(bind_pos_matrix_count)+Style.RESET_ALL)



########################################################################################################################################
#PROCESS ASSET
########################################################################################################################################


asset_type=get_asset_type(vertex_count,vertex_buffer_size,bind_pos_matrix_count)

material_list=get_material_list(vertex_count,vertex_buffer_size,bind_pos_matrix_count)

if len(material_list.split()) == len(material_vertex_count_array.split()):
    print("Vertex Colors Optimization: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("WARNING: Assert Vertex Colors Not Optimized"+ Fore.YELLOW + "[WARNING]" +Style.RESET_ALL)    


########################################################################################################################################
#  COMPLEX ASSETS - Preprocess Avatar
########################################################################################################################################


if (asset_type == "goose") or (asset_type == "npc"):

    
    avatar_name=""
    avatar_size=0

    avatar_skeleton_flag=0
    avatar_skelton_ID=""

    avatar_skeleton_pose_flag=0
    avatar_skeleton_pose_count=0

    avatar_default_pose_flag=0
    avatar_default_pose_count=0

    avatar_skelton_name_ID_array=""

    avatar_left_hand_bone_index=""
    avatar_left_hand_bone_index_flag=0
    
    avatar_right_hand_bone_index=""
    avatar_right_hand_bone_index_flag=0  
    
    avatar_human_hand_bone_index=""

    avatar_human_bone_mass_array_count=0
    avatar_human_bone_mass_array_flag=0

    avatar_collider_scale=0
    avatar_collider_arm_twist=0
    avatar_collider_fore_arm_twist=0
    avatar_collider_upper_leg_twist=0
    avatar_collider_leg_twist=0
    avatar_collider_arm_stretch=0
    avatar_collider_leg_stretch=0
    avatar_collider_feet_spacing=0
    avatar_collider_has_left_hand=0
    avatar_collider_has_right_hand=0
    avatar_collider_has_TDoF=0
    
    avatar_bone_name_array=""
    avatar_bone_name_array_count=0

    avatar_root_motion_bone_index=0


    avatar_tos_flag=0
    if len(sys.argv) > 2:
        avatar_file = open(sys.argv[2], "r")

        AVATAR_LINE = avatar_file.readlines()


        print("Preprocessing File...")
        for line in AVATAR_LINE: 

            if "m_name:" in line:
                avatar_name=line.split(":")[1].strip()

            elif "m_AvatarSize:" in line:  
                avatar_size=int(line.split(":")[1].strip())

            elif "m_ID:" in line:
                avatar_skelton_ID=line.split(":")[1].strip()

            elif "m_AvatarSkeletonPose:" in line:
                avatar_skeleton_pose_flag=1
                avatar_default_pose_flag=0
            
            elif "- t:" in line and avatar_skeleton_pose_flag == 1:
                avatar_skeleton_pose_count+=1
            
            elif "m_DefaultPose:" in line:
                avatar_default_pose_flag=1
                avatar_skeleton_pose_flag=0
            
            elif "- t:" in line and avatar_default_pose_flag == 1:
                avatar_default_pose_count+=1     

            elif "m_SkeletonNameIDArray:" in line:
                avatar_skelton_name_ID_array=line.split(":")[1].strip()

            elif "m_LeftHand:" in line:
                avatar_left_hand_bone_index_flag=1
                avatar_right_hand_bone_index_flag=0 
                
            elif "m_RightHand:" in line:
                avatar_left_hand_bone_index_flag=0
                avatar_right_hand_bone_index_flag=1
                

            elif "m_HandBoneIndex:" in line and avatar_left_hand_bone_index_flag == 1:
                avatar_left_hand_bone_inde=line.split(":")[1].strip()

            elif "m_HandBoneIndex:" in line and avatar_right_hand_bone_index_flag == 1:
                avatar_right_hand_bone_index=line.split(":")[1].strip()

            elif "m_HumanBoneIndex:" in line:
                avatar_human_hand_bone_index=line.split(":")[1].strip()

            elif "m_HumanBoneMass:" in line:
                avatar_human_bone_mass_array_flag=1

            elif "-" in line and avatar_human_bone_mass_array_flag==1:
                avatar_human_bone_mass_array_count+=1

            elif "m_ColliderIndex:" in line:
                avatar_human_bone_mass_array_flag=0


            elif "m_TOS:" in line:
                avatar_tos_flag=1

            elif ":" in line and avatar_tos_flag == 1:
                avatar_bone_name_array+= line.split(":")[1].strip() + " "
                avatar_bone_name_array_count+=1








########################################################################################################################################
#  COMPLEX ASSETS - Preprocess Avatar
########################################################################################################################################




        avatar_bone_name_hash_array=np.zeros(avatar_bone_name_array_count, dtype=np.int64)

        avatar_skeleton_pose_array=np.zeros((avatar_skeleton_pose_count*10), dtype=float)
        avatar_default_pose_array=np.zeros((avatar_default_pose_count*10), dtype=float)
        
        avatar_human_root_bone_array=np.zeros(10, dtype=float)

        avatar_human_bone_mass_array=np.zeros(avatar_human_bone_mass_array_count, dtype=float)
        avatar_root_motion_bone_array=np.zeros(10, dtype=float)

        avatar_skeleton_pose_flag=0
        avatar_default_pose_flag=0
        avatar_root_bone_flag=0
        avatar_tos_flag=0

        avatar_skeleton_pose_index=0
        avatar_default_pose_index=0
        avatar_bone_name_hash_index=0

        avatar_file.seek(0)
        AVATAR_LINE = avatar_file.readlines()

        print("Reading Avatar File...")
        for line in AVATAR_LINE: 
    
            if "m_AvatarSkeletonPose:" in line:
                avatar_skeleton_pose_flag=1
                avatar_default_pose_flag=0
                avatar_root_bone_flag=0
            elif "t:" in line and avatar_skeleton_pose_flag == 1:
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+1] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and avatar_skeleton_pose_flag == 1:
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+3] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+4] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+5] = float(line.split("z:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and avatar_skeleton_pose_flag == 1:
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+7] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+8] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_skeleton_pose_array[avatar_skeleton_pose_index*10+9] = float(line.split("z:")[1].split("}")[0].strip())
                avatar_skeleton_pose_index+=1


            elif "m_DefaultPose:" in line:
                avatar_default_pose_flag=1
                avatar_skeleton_pose_flag=0
                avatar_root_bone_flag=0
            elif "t:" in line and avatar_default_pose_flag == 1:
                avatar_default_pose_array[avatar_default_pose_index*10] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+1] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and avatar_default_pose_flag == 1:
                avatar_default_pose_array[avatar_default_pose_index*10+3] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+4] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+5] = float(line.split("z:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and avatar_default_pose_flag == 1:
                avatar_default_pose_array[avatar_default_pose_index*10+7] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+8] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_default_pose_array[avatar_default_pose_index*10+9] = float(line.split("z:")[1].split("}")[0].strip())
                avatar_default_pose_index+=1


            elif "m_RootX:" in line:
                avatar_default_pose_flag=0
                avatar_skeleton_pose_flag=0
                avatar_root_bone_flag=1
            elif "t:" in line and avatar_root_bone_flag == 1:
                avatar_human_root_bone_array[0] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[1] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and avatar_root_bone_flag == 1:
                avatar_human_root_bone_array[3] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[4] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[5] = float(line.split("z:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and avatar_root_bone_flag == 1:
                avatar_human_root_bone_array[7] = float(line.split("{x:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[8] = float(line.split("y:")[1].split(",")[0].strip())
                avatar_human_root_bone_array[9] = float(line.split("z:")[1].split("}")[0].strip())
                avatar_root_bone_flag=0       





            elif "m_TOS:" in line:
                avatar_tos_flag=1

            elif ":" in line and avatar_tos_flag == 1:
                avatar_bone_name_hash_array[avatar_bone_name_hash_index] = np.int64(line.split(":")[0].strip())
                avatar_bone_name_hash_index+=1
















    else:
        print("ERROR - Complet Asset requires Accompaning Avatar Asset"+ Fore.RED + "[FAIL]" +Style.RESET_ALL) 
        print("Please call with \"python goosetools_extractor.py <mesh.asset> <avatar.asset>\"")






########################################################################################################################################
#PRINT INFO
########################################################################################################################################



print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Index Buffer Size: "+Fore.GREEN +str(len(index_buffer))+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)


if asset_type == "simple":
    vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
    print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
elif asset_type == "npc" or asset_type == "goose":
    print("Complex Vertex Buffer Block Size: " +Fore.GREEN+ str(get_complex_vertex_buffer_size(vertex_count))+Style.RESET_ALL)
    print("Complex Color and UV Buffer Block Size: " +Fore.GREEN+ str(get_complex_color_buffer_size(vertex_count))+Style.RESET_ALL)
    print("Complex Bone Buffer Block Size: " +Fore.GREEN+ str(get_complex_bone_buffer_size(vertex_count))+Style.RESET_ALL)

#print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)


for bone_name_index in range(len(avatar_bone_name_array.split())):
    print(avatar_bone_name_array.split()[bone_name_index])


########################################################################################################################################
# Write COLLADA FILE
########################################################################################################################################

collada_file = open(sys.argv[1].split(".")[0]+".dae", "w")


# Variables
collada_gemotery_id=str(asset_name)+"-mesh"
collada_name=str(asset_name)



collada_vertex_array_name=str(asset_name)+"-mesh-vertex-array"
collada_vertex_source_id=str(asset_name)+"-mesh-vertices"
collada_vertex_source_name=str(asset_name)+"-vertices"
collada_vetex_count=vertex_count








collada_face_array_name=""
collada_face_source_name=""
collada_face_count=index_count



#########################
# Write COLLADA HEADER
#########################


collada_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n")
collada_file.write("<COLLADA xmlns=\"http://www.collada.org/2005/11/COLLADASchema\" version=\"1.4.1\">\n")
collada_file.write("<asset>\n")
collada_file.write("<contributor>\n")
collada_file.write("<author>GooseTools</author>\n")
collada_file.write("<authoring_tool>GooseTool's version: " + str(major) + "." + str(minor) + "</authoring_tool>\n")
collada_file.write("</contributor>\n")
collada_file.write("<created>2020-10-10T13:17:06</created>\n")
collada_file.write("<modified>" + today.strftime("%Y-%m-%d")+"T13:17:06</modified>\n")
collada_file.write("<unit name=\"meter\" meter=\"1\"/>\n")
collada_file.write("<up_axis>Z_UP</up_axis>\n")
collada_file.write("</asset>\n")



#################################
# Write COLLADA LIBRARY EFFECTS
#################################

collada_file.write("<library_effects>\n")

#for material_num in range(len(material_list.split())+1):
for material_num in range(1):    
    collada_material_effect_name=generate_material_name(material_num) + "-effect"
    
    collada_file.write("<effect id=\"" + str(collada_material_effect_name) + "\">\n")
    collada_file.write("<profile_COMMON>\n")
    collada_file.write("<technique sid=\"common\">\n")
    collada_file.write("<lambert>\n")
    collada_file.write("<emission>\n")
    collada_file.write("<color sid=\"emission\">0 0 0 1</color>\n")
    collada_file.write("</emission>\n")
    collada_file.write("<diffuse>\n")
    collada_file.write("<color sid=\"diffuse\">0.8 0.8 0.8 1</color>\n")
    collada_file.write("</diffuse>\n")
    collada_file.write("<reflectivity>\n")
    collada_file.write("<float sid=\"specular\">0.5</float>\n")
    collada_file.write("</reflectivity>\n")
    collada_file.write("</lambert>\n")
    collada_file.write("</technique>\n")
    collada_file.write("</profile_COMMON>\n")
    collada_file.write("</effect>\n")

collada_file.write("</library_effects>\n")

#################################
# Write COLLADA LIBRARY MATERIALS
#################################

collada_file.write("<library_materials>\n")

#for material_num in range(len(material_list.split())+1):
for material_num in range(1):    
    collada_library_material_id=generate_material_name(material_num) + "-material"   
    collada_library_material_name=generate_material_name(material_num)
    collada_library_material_url=generate_material_name(material_num) + "-effect"

    collada_file.write("<material id=\"" + str(collada_library_material_id) + "\" name=\"" + str(collada_library_material_name) + "\">\n")
    collada_file.write("<instance_effect url=\"#" + str(collada_library_material_url) + "\"/>\n")
    collada_file.write("</material>\n")


collada_file.write("</library_materials>\n")



#################################
# Write COLLADA MESH HEADER
#################################


collada_file.write("<library_geometries>\n")
collada_file.write("<geometry id=\"" + collada_gemotery_id + "\" name=\"" + collada_name + "\">\n")
collada_file.write("<mesh>\n")



###############################
# Write COLLADA POSITIONS
###############################

collada_position_array_name=str(asset_name)+"-mesh-positions-array"
collada_position_source_id=str(asset_name)+"-mesh-positions"
collada_position_source_name=str(asset_name)+"-positions"
collada_position_count=vertex_count

collada_file.write("<source id=\"" + collada_position_source_id + "\">\n")
collada_file.write("<float_array id=\"" + collada_position_array_name + "\" count=\""+str(collada_position_count*3)+"\"> ")

for collada_position in range(int(collada_position_count)):
    if asset_type == "npc" or asset_type == "goose":
        collada_file.write(get_obj_vertex(collada_position,collada_position_count) + " ")
    elif asset_type == "simple":
        collada_file.write(get_simple_obj_vertex(collada_position,collada_position_count) + " ")

collada_file.write("</float_array>\n")

collada_file.write("<technique_common>\n")
collada_file.write("<accessor count=\""+str(collada_position_count)+"\" offset=\"0\" source=\"#" + collada_position_source_name + "\" stride=\"3\">\n")
collada_file.write("<param name=\"X\" type=\"float\" />\n")
collada_file.write("<param name=\"Y\" type=\"float\" />\n")
collada_file.write("<param name=\"Z\" type=\"float\" />\n")
collada_file.write("</accessor>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</source>\n")




################################
# Write COLLADA Normal
################################

collada_normal_array_name=str(asset_name)+"-mesh-normals-array"
collada_normal_source_id=str(asset_name)+"-mesh-normals"
collada_normal_source_name=str(asset_name)+"-normals"
collada_normal_count=vertex_count

collada_file.write("<source id=\"" + collada_normal_source_id + "\" name=\"" + collada_normal_source_name + "\">\n")
collada_file.write("<float_array id=\"" + collada_normal_array_name + "\" count=\""+str(collada_normal_count*3)+"\"> ")

#Normals go here
for collada_normal in range(int(collada_normal_count)):
    if asset_type == "npc" or asset_type == "goose":
        collada_file.write(get_obj_normal(collada_normal,collada_normal_count) + " ")
    elif asset_type == "simple":
        collada_file.write(get_simple_obj_normal(collada_normal,collada_normal_count) + " ")

collada_file.write("</float_array>\n")
collada_file.write("<technique_common>\n")
collada_file.write("<accessor count=\""+str(collada_normal_count)+"\" offset=\"0\" source=\"#" + collada_normal_source_name + "\" stride=\"3\">\n")
collada_file.write("<param name=\"X\" type=\"float\" />\n")
collada_file.write("<param name=\"Y\" type=\"float\" />\n")
collada_file.write("<param name=\"Z\" type=\"float\" />\n")
collada_file.write("</accessor>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</source>\n")






#########################
# Write COLLADA Colors
#########################

collada_color_array_name=str(asset_name)+"-mesh-colors-array"
collada_color_source_id=str(asset_name)+"-mesh-colors"
collada_color_source_name=str(asset_name)+"-colors"
collada_color_count=vertex_count

collada_file.write("<source id=\"" + collada_color_source_id + "\" name=\"" + collada_color_source_name + "\">\n")
collada_file.write("<float_array id=\"" + collada_color_array_name + "\" count=\""+str(collada_color_count*4)+"\"> ")

#Normals go here
for collada_color in range(int(collada_color_count)):
    
    if asset_type == "goose":
        collada_file.write(get_obj_color(collada_color,collada_color_count) + " 1 " )
    if asset_type == "npc":
        collada_file.write(get_obj_npc_color(collada_color,collada_color_count) + " 1 " )
    if asset_type == "simple":
         collada_file.write(get_simple_obj_color(collada_color,collada_color_count) + " 1 ")       
collada_file.write("</float_array>\n")


collada_file.write("<technique_common>\n")
collada_file.write("<accessor source=\"#" + str(collada_color_array_name) + "\" count=\"" + str(collada_color_count) + "\" stride=\"4\">\n")
collada_file.write("<param name=\"R\" type=\"float\" />\n")
collada_file.write("<param name=\"G\" type=\"float\" />\n")
collada_file.write("<param name=\"B\" type=\"float\" />\n")
collada_file.write("<param name=\"A\" type=\"float\" />\n")
collada_file.write("</accessor>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</source>\n")


#######################################
# Write COLLADA Vertices Position
#######################################

collada_file.write("<vertices id=\"" + collada_vertex_source_id + "\">\n")
collada_file.write("<input semantic=\"POSITION\" source=\"#" + collada_position_source_id + "\" />\n")
collada_file.write("</vertices>\n")


#######################################
# Write COLLADA TRIANGLES (.OBJ Faces)
#######################################

material_index=0
new_material_flag=0
#for material_num in range(len(material_list.split())):
    #print("DEBUG - MATERIAL NUM: " + str(material_num))
    #new_material_flag=0
    #collada_library_material_id=generate_material_name(material_num) + "-material"
    #material_vertex_start=int(material_vertex_start_array.split()[material_num])
    #material_vertex_end=int(material_vertex_count_array.split()[material_num])+material_vertex_start-1
    
    #current_face_count=0
    #for face in range(int(index_count/3)):
        #temp_face=get_obj_face(face)
        #v1=temp_face.split()[0]
        #v2=temp_face.split()[1]
        #v3=temp_face.split()[2]

        #if (int(v1) <= int(material_vertex_end)):
            #if(int(v2) <= int(material_vertex_end)):
                #if(int(v3) <= int(material_vertex_end)):
                    #if (int(v1) >= int(material_vertex_start)): 
                        #if(int(v2) >= int(material_vertex_start)):
                            #if(int(v3) >= int(material_vertex_start)):
                                #current_face_count+=1

                                #collada_triangle_vertex_count=current_face_count

                                #collada_file.write("<triangles material=\"" + str(collada_library_material_id) + "\" count=\""+str(collada_triangle_vertex_count) + "\">\n")
                                #collada_file.write("<input semantic=\"VERTEX\" source=\"#" + collada_vertex_source_id + "\" offset=\"0\"/>\n")
                                #collada_file.write("<input semantic=\"NORMAL\" source=\"#" + collada_normal_source_id + "\" offset=\"1\"/>\n")
                                #collada_file.write("<input semantic=\"COLOR\" source=\"#" + collada_color_source_id + "\" offset=\"2\" set=\"0\"/>\n")
                            #else:
                                #print("ERROR: FACE: "+str(face)+" V1: "+str(v1)  +" V3: "+str(v3) + " out of vertex_start "+ Fore.RED + "["+str(material_vertex_start)+"]" +Style.RESET_ALL+  " vertex_end "+ Fore.RED + "["+str(material_vertex_end)+"]" +Style.RESET_ALL)
                        #else:
                            #print("ERROR: FACE: "+str(face) +" V1: "+str(v1)  +" V2: "+str(v2) + " out of vertex_start "+ Fore.RED + "["+str(material_vertex_start)+"]" +Style.RESET_ALL+  " vertex_end "+ Fore.RED + "["+str(material_vertex_end)+"]" +Style.RESET_ALL)
                    #else:
                        #print("ERROR: V1 out of vertex_start "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)
                #else:
                    #print("ERROR: FACE: "+str(face) +" V1: "+str(v1)  +" V3: "+str(v3) + " out of vertex_start "+ Fore.RED + "["+str(material_vertex_start)+"]" +Style.RESET_ALL+  " vertex_end "+ Fore.RED + "["+str(material_vertex_end)+"]" +Style.RESET_ALL)
            #else:
                #print("ERROR: FACE: "+str(face) +" V1: "+str(v1)  +" V2: "+str(v2) + " out of vertex_start "+ Fore.RED + "["+str(material_vertex_start)+"]" +Style.RESET_ALL + "  vertex_end "+ Fore.RED + "["+str(material_vertex_end)+"]" +Style.RESET_ALL)
        #else:
            #print("ERROR: V1 out of vertex_end "+ Fore.RED + "[FAIL]" +Style.RESET_ALL)

    #Write the index buffer
    



collada_triangle_vertex_count=index_count

collada_file.write("<triangles material=\"" + str(collada_library_material_id) + "\" count=\""+str(collada_triangle_vertex_count) + "\">\n")
collada_file.write("<input semantic=\"VERTEX\" source=\"#" + collada_vertex_source_id + "\" offset=\"0\"/>\n")
collada_file.write("<input semantic=\"NORMAL\" source=\"#" + collada_normal_source_id + "\" offset=\"1\"/>\n")
collada_file.write("<input semantic=\"COLOR\" source=\"#" + collada_color_source_id + "\" offset=\"2\" set=\"0\"/>\n")

collada_file.write("<p>")




for face in range(int(index_count/3)):
    temp_face=get_obj_face(face)
    v1=temp_face.split()[0]
    v2=temp_face.split()[1]
    v3=temp_face.split()[2]
        
        #if ((int(v1) > int(material_vertex_end)) or (int(v2) > int(material_vertex_end)) or (int(v3) > int(material_vertex_end))) and new_material_flag != 1:
            #print("Writing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
            #material_index+=1
            #new_material_flag=1
        #elif ((int(v1) >= int(material_vertex_start)) and (int(v2) >= int(material_vertex_start)) and (int(v3) >= int(material_vertex_start))) and new_material_flag != 1:
            #Write Face
    collada_file.write(v1+" "+v1+" "+v1+" "+v2+" "+v2+" "+v2+" "+v3+" "+v3+" "+v3+" ")





        #else:
            #print("DEBUG - V1: " + str(v1) + " >= " + str(material_vertex_start) + " or > " + str(material_vertex_end) )       	
            #print("DEBUG - V2: " + str(v2)+ " >= " + str(material_vertex_start) + " or > " + str(material_vertex_end) )   
            #print("DEBUG - V3: " + str(v3)+ " >= " + str(material_vertex_start) + " or > " + str(material_vertex_end) )          		       
collada_file.write("</p>\n")
collada_file.write("</triangles>\n")












collada_file.write("</mesh>\n")
collada_file.write("</geometry>\n")
collada_file.write("</library_geometries>\n")

#########################################################################################################
# COLLADA CONTROLELRS - BONE INFORMATION
#########################################################################################################


collada_file.write("<library_controllers>\n")

if asset_type == "goose" or asset_type == "npc":



    collade_bone_number=bind_pos_matrix_count

    collada_skin_id="Body_Armature_"+str(asset_name)+"-skin"
    collada_skin_name="Body_Armature"
    collada_skin_source=collada_gemotery_id


    collada_skin_joints_id="Body_Armature_"+str(asset_name)+"-skin-joints"
    collada_skin_joints_array_name="Body_Armature_"+str(asset_name)+"-skin-joints-array"
    collade_bone_name_array_count=bind_pos_matrix_count
    #########################
    # SKINNING INFO
    #########################
    collada_file.write("<controller id=\"" + str(collada_skin_id) + "\" name=\"" + str(collada_skin_name) + "\">\n")
    collada_file.write("<skin source=\"#" + str(collada_skin_source) + "\">\n")
    collada_file.write("<bind_shape_matrix>1 0 0 0 0 1 0 0 0 0 1 -5.206488 0 0 0 1</bind_shape_matrix>\n")
    collada_file.write("<source id=\"" + str(collada_skin_joints_id) + "\">\n")
    collada_file.write("<Name_array id=\"" + str(collada_skin_joints_array_name) + "\" count=\"" + str(int(collade_bone_name_array_count)) + "\"> ")

    #Bone name placeholder
    #collada_file.write("Bone Bone_001 Bone_002 Bone_003 Bone_004 Bone_016 Bone_010 Bone_011 Bone_012 Bone_014 Bone_015 Bone_018 Bone_019 Bone_020 Bone_022 Bone_023 Bone_024 Bone_032 Bone_026 Bone_027 Bone_028 Bone_030 Bone_031 Bone_034 Bone_035 Bone_036 Bone_038 Bone_039 Bone_040 Bone_051 Bone_050 Bone_049 Bone_048 Bone_047 Bone_005 Bone_007 Bone_013 Bone_017 Bone_021 Bone_025 Bone_029 Bone_033 Bone_037 Bone_054 Bone_055 Bone_053 Bone_052")
    collada_file.write(get_bone_name_buffer(collade_bone_number))
    collada_file.write("</Name_array>\n")
    
    collada_file.write("<technique_common>\n")
    collada_file.write("<accessor source=\"#" + str(collada_skin_joints_array_name) + "\" count=\"" + str(int(collade_bone_name_array_count)) + "\" stride=\"1\">\n")
    collada_file.write("<param name=\"JOINT\" type=\"name\"/>\n")
    collada_file.write("</accessor>\n")
    collada_file.write("</technique_common>\n")
    collada_file.write("</source>\n")




    #########################
    # BIND POSE
    #########################

    collada_bind_pose_source_id="Body_Armature_"+str(asset_name)+"-skin-bind_poses"
    collada_bind_pose_array_name="Body_Armature_"+str(asset_name)+"-skin-bind_poses-array"

    collada_file.write("<source id=\"" + str(collada_bind_pose_source_id) + "\">\n")
    collada_file.write("<float_array id=\"" + str(collada_bind_pose_array_name) + "\" count=\"" + str(int(collade_bone_number*16)) + "\">\n")



    #Write Bind Pose here
    collada_file.write(str(bind_pose_buffer))

    collada_file.write("</float_array>\n")
    collada_file.write("<technique_common>\n")
    collada_file.write("<accessor source=\"#" + str(collada_bind_pose_array_name) + "\" count=\"" + str(int(collade_bone_number)) + "\" stride=\"16\">\n")
    collada_file.write("<param name=\"TRANSFORM\" type=\"float4x4\"/>\n")
    collada_file.write("</accessor>\n")
    collada_file.write("</technique_common>\n")
    collada_file.write("</source>\n")




    #########################
    # SKIN WEIGHTS
    #########################
    
    collada_skin_weight_source_id="Body_Armature_"+str(asset_name)+"-skin-weights"
    collada_skin_weight_array_name="Body_Armature_"+str(asset_name)+"-skin-weights-array"
    collade_skin_weight_count=0

    for vertex_index in range(vertex_count):
        collade_skin_weight_count+=get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)

    collada_file.write("<source id=\"" + str(collada_skin_weight_source_id) + "\">\n")
    collada_file.write("<float_array id=\"" + str(collada_skin_weight_array_name) + "\" count=\"" + str(int(collade_skin_weight_count)) + "\">\n")
    
    #Write Weights Here
    for vertex_index in range(vertex_count):
        for skin_weight_index in range(get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)):
            collada_file.write(get_obj_vertex_weight(skin_weight_index,vertex_index,vertex_count,asset_type).split()[1])
       
    collada_file.write("</float_array>\n")
    collada_file.write("<technique_common>\n")
    collada_file.write("<accessor source=\"#" + str(collada_skin_weight_array_name) + "\" count=\"" + str(int(collade_skin_weight_count)) + "\" stride=\"1\">\n")
    collada_file.write("<param name=\"WEIGHT\" type=\"float\"/>\n")
    collada_file.write("</accessor>\n")
    collada_file.write("</technique_common>\n")
    collada_file.write("</source>\n")


    ##################################
    # JOINT and WEIGHT INDEX BUFFER
    #################################



    collada_file.write("<joints>\n")
    collada_file.write("<input semantic=\"JOINT\" source=\"#" + str(collada_skin_joints_id) + "\"/>\n")
    collada_file.write("<input semantic=\"INV_BIND_MATRIX\" source=\"#" + str(collada_bind_pose_source_id) + "\"/>\n")
    collada_file.write("</joints>\n")
    collada_file.write("<vertex_weights count=\"" + str(vertex_count) + "\">\n")
    collada_file.write("<input semantic=\"JOINT\" source=\"#" + str(collada_skin_joints_id) + "\" offset=\"0\"/>\n")
    collada_file.write("<input semantic=\"WEIGHT\" source=\"#" + str(collada_skin_weight_source_id) + "\" offset=\"1\"/>\n")
    collada_file.write("<vcount>\n")

          #VCOUNT - NUMBER OF WEIGHTS PER VERTEX - BETWEEN 1 and 4
    for vertex_index in range(vertex_count):
        collada_file.write(str(get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)) +" ")



    collada_file.write("</vcount>\n")
    collada_file.write("<v>\n")



    #VERTEX POSTION
    global_vertex_positon_count=0
    for vertex_index in range(vertex_count):
        
        temp_vertex_weight_count=get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)
        #collada_file.write(str(temp_vertex_weight_count) +" ")
        for skin_weight_index in range(temp_vertex_weight_count):
            #print("DEBUG- TEMP VERTEX WEIGHT: " + str(temp_vertex_weight_count) + " : "  + str(skin_weight_index))         
            collada_file.write(str(get_obj_vertex_weight(skin_weight_index,vertex_index,vertex_count,asset_type)).split()[0] + " ")
            collada_file.write(str(global_vertex_positon_count+skin_weight_index) + " ")
        global_vertex_positon_count+=int(temp_vertex_weight_count)

    collada_file.write("</vertex_weights>\n")
    collada_file.write("</skin>\n")
    collada_file.write("</controller>\n")



collada_file.write("</library_controllers>\n")

















collada_visual_scene_id="Scene"
collada_visual_scene_name="Scene"
collada_visual_scene_url="Scene"

collada_visual_scene_node_id=str(asset_name)
collada_visual_scene_node_name=str(asset_name)


#########################
# COLLADA BINDING
#########################
collada_file.write("<library_visual_scenes>\n")
collada_file.write("<visual_scene id=\"" + str(collada_visual_scene_id) + "\" name=\"" + str(collada_visual_scene_name) +"\">\n")







#########################
# WRITE BONES
#########################


if asset_type == "goose" or asset_type == "npc":

    #Root Bone
    collada_file.write("<node id=\"Armature\" name=\"Armature\" type=\"NODE\">\n")
    collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 5.206488 0 0 0 1</matrix>\n")
    collada_file.write("<node id=\"Armature_Bone\" name=\"Bone\" sid=\"Bone\" type=\"JOINT\">\n")
    collada_file.write("<matrix sid=\"transform\">0.9964491 -0.0740106 -0.04014485 0 0.04014487 0.8367317 -0.5461397 0 0.07401059 0.5425888 0.8367316 0 0 0 0 1</matrix>\n")
    #All the children bones?
    for bone_index in range(collade_bone_number):

        collada_file.write("<node id=\"Armature_Bone_001\" name=\"Bone.001\" sid=\"Bone_001\" type=\"JOINT\">\n")
        collada_file.write("<matrix sid=\"transform\">0.165655 -0.5664322 -0.8072872 0 0.5321904 -0.6378247 0.5567341 0 -0.8302599 -0.5218564 0.1957912 -5.96046e-8 0 0 0 1</matrix>\n")
        collada_file.write("<extra>\n")
        collada_file.write("<technique profile=\"blender\">\n")
        collada_file.write("<layer sid=\"layer\" type=\"string\">0</layer>\n")
        collada_file.write("<roll sid=\"roll\" type=\"float\">-0.6829612</roll>\n")
        collada_file.write("<tip_x sid=\"tip_x\" type=\"float\">-1.817046</tip_x>\n")
        collada_file.write("<tip_y sid=\"tip_y\" type=\"float\">-0.9937923</tip_y>\n")
        collada_file.write("<tip_z sid=\"tip_z\" type=\"float\">-3.019416</tip_z>\n")
        collada_file.write("</technique>\n")
        collada_file.write("</extra>\n")
        collada_file.write("</node>\n")
          




elif asset_type == "simple":

    collada_file.write("<node id=\"Node_000000000349DD80\" name=\"Node_000000000349DD80\" type=\"NODE\">\n")
    collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
    collada_file.write("</node>\n")
    collada_file.write("<node id=\"" + str(collada_visual_scene_node_id) + "\" name=\"" + str(collada_visual_scene_node_name) + "\" type=\"NODE\">\n")
    collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
    collada_file.write("<instance_geometry url=\"#"+str(collada_gemotery_id)+"\" name=\""+str(collada_name)+"\">\n")






#########################
# COLLADA BIND MATERIALS
#########################

collada_file.write("<bind_material>\n")
collada_file.write("<technique_common>\n")

#for material_num in range(len(material_list.split())):
    #collada_library_material_id=generate_material_name(material_num) + "-material" 
    #collada_file.write("<instance_material symbol=\"" + str(collada_library_material_id) + "\" target=\"#" + str(collada_library_material_id) + "\"/>\n")

for material_num in range(1):
    collada_library_material_id=generate_material_name(material_num) + "-material" 
    collada_file.write("<instance_material symbol=\"" + str(collada_library_material_id) + "\" target=\"#" + str(collada_library_material_id) + "\"/>\n")


collada_file.write("</technique_common>\n")
collada_file.write("</bind_material>\n")
collada_file.write("</instance_geometry>\n")
collada_file.write("</node>\n")
collada_file.write("</visual_scene>\n")
collada_file.write("</library_visual_scenes>\n")
collada_file.write("<scene>\n")
collada_file.write("<instance_visual_scene url=\"#"+str(collada_visual_scene_url)+"\"/>\n")
collada_file.write("</scene>\n")
collada_file.write("</COLLADA>\n")




print("BONE ROOT: " + get_obj_bone_root(vertex_count))




#for index in range(vertex_count):
    #print("VERTEX: " +Fore.CYAN + str(index) + Style.RESET_ALL +" "+Fore.CYAN + str(get_obj_vertex_weight_count(index,vertex_count,asset_type)) + Style.RESET_ALL)
    #print("BONE 1: " + str(get_obj_vertex_weight(0,index,vertex_count,asset_type)))
    #print("BONE 2: " + str(get_obj_vertex_weight(1,index,vertex_count,asset_type)))
    #print("BONE 3: " + str(get_obj_vertex_weight(2,index,vertex_count,asset_type)))
    #print("BONE 4: " + str(get_obj_vertex_weight(3,index,vertex_count,asset_type)))
    #print("BONE INDEX 0 :" +Fore.YELLOW + str(get_obj_vertex_weight(0,index,vertex_count,asset_type)) + Style.RESET_ALL)
    #print("BONE INDEX 1 :" +Fore.YELLOW + str(get_obj_vertex_weight(1,index,vertex_count,asset_type)) + Style.RESET_ALL)
    #print("BONE INDEX 2 :" +Fore.YELLOW + str(get_obj_vertex_weight(2,index,vertex_count,asset_type)) + Style.RESET_ALL)
    #print("BONE INDEX 3 :" +Fore.YELLOW + str(get_obj_vertex_weight(3,index,vertex_count,asset_type)) + Style.RESET_ALL)        
    
print("BONE COUNT: " + Fore.GREEN +str(bind_pos_matrix_count)+ Style.RESET_ALL)
print("BONE NAME HASH SIZE: " + Fore.GREEN+ str(len(bone_name_hash))+ Style.RESET_ALL)
print("BONE NAME HASH BLOCK SIZE: "+ Fore.GREEN + str(len(bone_name_hash)/bind_pos_matrix_count)+ Style.RESET_ALL)




#########################
# End of COLLADA File
#########################
collada_file.close()









#print("Script Complete")
asset_file.close



                

