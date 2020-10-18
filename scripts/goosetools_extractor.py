#GooseTool's Complex Collada Generator
major=1
minor=1

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

















def get_avatar_bone_name(bone_number):

    if bone_number <= len(avatar_bone_name_array.split()):
        chain_length=len(avatar_bone_name_array.split()[bone_number].split("/"))
        return str(avatar_bone_name_array.split()[bone_number].split("/")[chain_length-1])

    else:

        print(Fore.RED + "ERROR - Bone Index "  + str(bone_number) + "out of range!" + Style.RESET_ALL)
        return "<error>"

def get_avatar_bone_id(bone_number):

    if bone_number <= len(avatar_bone_name_array.split()):
        chain_length=len(avatar_bone_name_array.split()[bone_number].split("/"))
        return "Armature_" +str(avatar_bone_name_array.split()[bone_number].split("/")[chain_length-1])

    else:

        print(Fore.RED + "ERROR - Bone Index "  + str(bone_number) + "out of range!" + Style.RESET_ALL)
        return "<error>"

def get_inverse_bind_transform(bone_number):
    
    bind_matrix=np.zeros(shape=(4,4), dtype=float)


    for row in range(4):
        for col in range(4):
            bind_matrix[row][col]=float(bind_pose_buffer.split()[bone_number*16+row+col])
    #Calculate inverse matrix
    
    #print(str(bind_matrix))
    inverse_matrix=np.linalg.inv(bind_matrix)

    return inverse_matrix
    



def get_int_hash_from_index(bone_index):
    

    byte_4=bone_name_hash[bone_index*8+6]+bone_name_hash[bone_index*8+7]
    byte_3=bone_name_hash[bone_index*8+4]+bone_name_hash[bone_index*8+5]
    byte_2=bone_name_hash[bone_index*8+2]+bone_name_hash[bone_index*8+3]
    byte_1=bone_name_hash[bone_index*8]+bone_name_hash[bone_index*8+1]
    temp_bone_hash=byte_4+byte_3+byte_2+byte_1
    #temp_bone_hash=byte_1+byte_2+byte_3+byte_4
    #print("TEMP STRING: " + str(temp_bone_hash ))
    #return str(struct.unpack('I', bytes.fromhex(temp_bone_hash))).strip('(),')
    return int(temp_bone_hash,16)
    #return int(byte_4,16)*255*255*255 + int(byte_3,16)*255*255 + int(byte_2,16)*255 + int(byte_1,16)


def get_bone_name_from_bind_pose_index(bone_index):

    temp_hash=get_int_hash_from_index(bone_index)
    for index in range(len(avatar_bone_name_hash_array)):
            if avatar_bone_name_hash_array[index] == temp_hash:
                bone_name=get_avatar_bone_name(index)
                #print("Matched Bone to Bind Pose: " + Fore.CYAN + "[" + str(bone_name) + "]" + Style.RESET_ALL)
                #return avatar_bone_name_array.split()[index]               
                chain_length=len(avatar_bone_name_array.split()[index].split("/"))
                return str(avatar_bone_name_array.split()[index].split("/")[chain_length-1])






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
    
    global avatar_bone_name_array
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
                if line.split(":")[1].strip() == "":
                    avatar_bone_name_array+= "unnamed_bone "
                else:
                    avatar_bone_name_array+= line.split(":")[1].strip() + " "
                avatar_bone_name_array_count+=1







########################################################################################################################################
#  COMPLEX ASSETS - Preprocess Avatar
########################################################################################################################################



        global avatar_bone_name_hash_array
        avatar_bone_name_hash_array=np.zeros(avatar_bone_name_array_count, dtype=np.int64)

        global avatar_skeleton_pose_array
        avatar_skeleton_pose_array=np.zeros((avatar_skeleton_pose_count*10), dtype=float)
        global avatar_default_pose_array
        avatar_default_pose_array=np.zeros((avatar_default_pose_count*10), dtype=float)
        global avatar_human_root_bone_array
        avatar_human_root_bone_array=np.zeros(10, dtype=float)
        global avatar_human_bone_mass_array
        avatar_human_bone_mass_array=np.zeros(avatar_human_bone_mass_array_count, dtype=float)
        global avatar_root_motion_bone_array
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

if asset_type == "npc" or asset_type == "goose":

    print("Avatar Name: "+Fore.GREEN + str(avatar_name)+Style.RESET_ALL)
    print("Avatar Size: "+Fore.GREEN +str(avatar_size)+Style.RESET_ALL)

    print("Avatar Skelton Pose Count: "+Fore.GREEN +str(avatar_skeleton_pose_count)+Style.RESET_ALL)
    print("Avatar Default Pose Count: "+Fore.GREEN +str(avatar_default_pose_count)+Style.RESET_ALL)

    for bone_name_index in range(len(avatar_bone_name_array.split())):
        print("BONE " + str(bone_name_index) + " NAME: " +Fore.CYAN+avatar_bone_name_array.split()[bone_name_index]+Style.RESET_ALL)


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
    collada_file.write("<index_of_refraction>\n")
    collada_file.write("<float sid=\"ior\">1.45</float>\n")
    collada_file.write("</index_of_refraction>\n")
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

collada_file.write("<triangles material=\"" + str(collada_library_material_id) + "\" count=\""+str(int(collada_triangle_vertex_count/3)) + "\">\n")
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
    collada_file.write("<bind_shape_matrix>1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</bind_shape_matrix>\n")
    collada_file.write("<source id=\"" + str(collada_skin_joints_id) + "\">\n")
    collada_file.write("<Name_array id=\"" + str(collada_skin_joints_array_name) + "\" count=\"" + str(int(collade_bone_name_array_count)) + "\"> ")

    #Bone name placeholder
    #collada_file.write("Bone Bone_001 Bone_002 Bone_003 Bone_004 Bone_016 Bone_010 Bone_011 Bone_012 Bone_014 Bone_015 Bone_018 Bone_019 Bone_020 Bone_022 Bone_023 Bone_024 Bone_032 Bone_026 Bone_027 Bone_028 Bone_030 Bone_031 Bone_034 Bone_035 Bone_036 Bone_038 Bone_039 Bone_040 Bone_051 Bone_050 Bone_049 Bone_048 Bone_047 Bone_005 Bone_007 Bone_013 Bone_017 Bone_021 Bone_025 Bone_029 Bone_033 Bone_037 Bone_054 Bone_055 Bone_053 Bone_052")
    
    for index in range(collade_bone_number):
        collada_file.write(get_bone_name_from_bind_pose_index(index) + " ")
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
    collada_file.write("<float_array id=\"" + str(collada_bind_pose_array_name) + "\" count=\"" + str(int(collade_bone_number*16)) + "\">")



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
    collada_file.write("<float_array id=\"" + str(collada_skin_weight_array_name) + "\" count=\"" + str(int(collade_skin_weight_count)) + "\">")
    
    #Write Weights Here
    for vertex_index in range(vertex_count):
        for skin_weight_index in range(get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)):
            collada_file.write(get_obj_vertex_weight(skin_weight_index,vertex_index,vertex_count,asset_type).split()[1] + " ")
       
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
    collada_file.write("<vcount>")

          #VCOUNT - NUMBER OF WEIGHTS PER VERTEX - BETWEEN 1 and 4
    for vertex_index in range(vertex_count):
        collada_file.write(str(get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)) +" ")



    collada_file.write("</vcount>\n")
    collada_file.write("<v>")



    #VERTEX POSTION
    global_vertex_positon_count=0
    for vertex_index in range(vertex_count):
        
        temp_vertex_weight_count=get_obj_vertex_weight_count(vertex_index,vertex_count,asset_type)
        #collada_file.write(str(temp_vertex_weight_count) +" ")
        for skin_weight_index in range(temp_vertex_weight_count):
            #print("DEBUG- TEMP VERTEX WEIGHT: " + str(temp_vertex_weight_count) + " : "  + str(skin_weight_index))         
            collada_file.write(str(int(str((get_obj_vertex_weight(skin_weight_index,vertex_index,vertex_count,asset_type)).split()[0]))-1) + " ")
            collada_file.write(str(global_vertex_positon_count+skin_weight_index))
            if (vertex_index != (vertex_count-1)) or (skin_weight_index != (temp_vertex_weight_count-1)):
                collada_file.write(" ")
        global_vertex_positon_count+=int(temp_vertex_weight_count)
    
    collada_file.write("</v>\n")
    collada_file.write("</vertex_weights>\n")
    collada_file.write("</skin>\n")
    collada_file.write("</controller>\n")



collada_file.write("</library_controllers>\n")














def get_bone_children(bone_name):
    temp_child_buffer=""
    parent_bone="unassigned"
    #print("DEBUG - BONE NAME: " + str(bone_name))
    for index in range(len(avatar_bone_name_array.split())):
        if bone_name == get_avatar_bone_name(index):
            parent_bone_index=index
            parent_bone=avatar_bone_name_array.split()[parent_bone_index] 
    #print("DEBUG - PARRENT BONE: " + str(parent_bone))
    for index in range(len(avatar_bone_name_array.split())):
        #print("if " + str(parent_bone) + " in " + str(avatar_bone_name_array.split()[index]) )
        if (parent_bone in avatar_bone_name_array.split()[index]) and (len(avatar_bone_name_array.split()[index].split("/")) > len(parent_bone.split("/"))):
            
            new_child=str(avatar_bone_name_array.split()[index].split("/")[(len(parent_bone.split("/")))])
            #print(Fore.GREEN + "YES" + Style.RESET_ALL  + " NEW CHILD: " + str(new_child))
            if new_child not in temp_child_buffer:
                    temp_child_buffer+=new_child + " "
    return temp_child_buffer


def get_bone_offspring(bone_name):
    offspring_buffer=""
    parent_bone="unassigned"
    #print("DEBUG - BONE NAME: " + str(bone_name))
    for index in range(len(avatar_bone_name_array.split())):
        if bone_name == get_avatar_bone_name(index):
            parent_bone_index=index
            parent_bone=avatar_bone_name_array.split()[parent_bone_index] 
    #print("DEBUG - PARRENT BONE: " + str(parent_bone))
    for index in range(len(avatar_bone_name_array.split())):
        #print("if " + str(parent_bone) + " in " + str(avatar_bone_name_array.split()[index]) )
        if (parent_bone in avatar_bone_name_array.split()[index]) and (len(avatar_bone_name_array.split()[index].split("/")) > len(parent_bone.split("/"))):
            new_child=get_avatar_bone_name (index)
            offspring_buffer+=new_child + " "
    return offspring_buffer

def get_bone_siblings(bone_name):
    offspring_buffer=""
    parent_bone="unassigned"
    #print("DEBUG - BONE NAME: " + str(bone_name))
    for index in range(len(avatar_bone_name_array.split())):
        if bone_name == get_avatar_bone_name(index):
            parent_bone_index=index
            parent_bone=avatar_bone_name_array.split()[parent_bone_index].split("/")[len(avatar_bone_name_array.split()[parent_bone_index].split("/"))-2] 
    return get_bone_children(parent_bone)



def get_bone_parent(bone_name):
    offspring_buffer=""
    parent_bone="unassigned"
    #print("DEBUG - BONE NAME: " + str(bone_name))
    for index in range(len(avatar_bone_name_array.split())):
        if bone_name == get_avatar_bone_name(index):
            parent_bone_index=index
            parent_bone=avatar_bone_name_array.split()[parent_bone_index].split("/")[len(avatar_bone_name_array.split()[parent_bone_index].split("/"))-2] 

    return parent_bone



def draw_bone_stucture():
    print("****" + get_armature_name()  +"****")
    print("ROOT: " + Fore.RED + get_root_bone_name() + Style.RESET_ALL)
    margin=" "
    level=0
    root_children=get_bone_children(get_armature_name()).split()
    for child in root_children:
        margin=" "

        sibling_buffer=""
        level=0
        print(Fore.CYAN + child + Style.RESET_ALL + "[" + str(level)+"]")
        level+=1
        margin="----"
        offspring_count=len(get_bone_offspring(child).split())
        temp_offspring=get_bone_offspring(child).split()
        temp_children=get_bone_children(child).split()     
        written_buffer=""
        current_child=child
        current_sib_count=1
        break_loop=0
        while len(written_buffer.split()) < offspring_count:
            for i in range(offspring_count):
                for j in range(offspring_count):
                    

                    if (temp_offspring[j] in temp_children) and (temp_offspring[j] not in written_buffer.split()):
                        #print("|"+margin+ "|")
                        
                        if len(get_bone_siblings(temp_offspring[j]).split()) > 1:
                            bone_color=Fore.YELLOW
                        else:
                            bone_color=Fore.GREEN
                        print(margin+"--"+bone_color + temp_offspring[j] + Style.RESET_ALL + "[" + str(level)+"]")
                        if len(get_bone_children(temp_offspring[j])) > 0:
                            level+=1
                        current_child = temp_offspring[j]
                        margin=margin+"----"
                        written_buffer+=current_child + " "
                        temp_children=get_bone_children(current_child).split()

                        #sibling_buffer+=str(len(get_bone_siblings(temp_offspring[j]))) + " "


            for sibling_name in get_bone_siblings(current_child).split():
                if sibling_name not in written_buffer and break_loop == 0:
                    current_child=sibling_name
                    margin=margin[:-4]
                    #print("|"+margin+ "|")
                    if len(get_bone_siblings(current_child).split()) > 1:
                        bone_color=Fore.YELLOW
                    else:
                            bone_color=Fore.GREEN
                    print(margin+"--"+bone_color + current_child + Style.RESET_ALL + "[" + str(level)+"]")
                    if len(get_bone_children(current_child)) > 0:
                        level+=1
                    margin=margin+"----"
                    written_buffer+=current_child + " "
                    temp_children=get_bone_children(current_child).split()
                    break_loop=1
            if break_loop==0:
                margin=margin[:-4]
                current_child=get_bone_parent(current_child)
                temp_children=get_bone_children(current_child).split()
                level-=1

            break_loop=0


def get_bone_stucture_buffer():
    level=0
    temp_buffer=get_root_bone_name() + " " + str(level) + " @ "
    root_children=get_bone_children(get_armature_name()).split()
    for child in root_children:
        level=1
        temp_buffer+=child + " " + str(level) + " @ "
        level+=1

        offspring_count=len(get_bone_offspring(child).split())
        temp_offspring=get_bone_offspring(child).split()
        temp_children=get_bone_children(child).split()     
        written_buffer=""
        current_child=child

        break_loop=0
        while len(written_buffer.split()) < offspring_count:
            for i in range(offspring_count):
                for j in range(offspring_count):
                    

                    if (temp_offspring[j] in temp_children) and (temp_offspring[j] not in written_buffer.split()):
                        
                        if len(get_bone_siblings(temp_offspring[j]).split()) > 1:
                            bone_color=Fore.YELLOW
                        else:
                            bone_color=Fore.GREEN
                        
                        temp_buffer+=temp_offspring[j] + " " + str(level) + " @ "
                        
                        if len(get_bone_children(temp_offspring[j])) > 0:
                            level+=1
                        current_child = temp_offspring[j]

                        written_buffer+=current_child + " "
                        temp_children=get_bone_children(current_child).split()


            for sibling_name in get_bone_siblings(current_child).split():
                if sibling_name not in written_buffer and break_loop == 0:
                    current_child=sibling_name
                    if len(get_bone_siblings(current_child).split()) > 1:
                        bone_color=Fore.YELLOW
                    else:
                            bone_color=Fore.GREEN
                    temp_buffer+=current_child + " " + str(level) + " @ "
                    if len(get_bone_children(current_child)) > 0:
                        level+=1

                    written_buffer+=current_child + " "
                    temp_children=get_bone_children(current_child).split()
                    break_loop=1
            if break_loop==0:

                current_child=get_bone_parent(current_child)
                temp_children=get_bone_children(current_child).split()
                level-=1

            break_loop=0

    return temp_buffer





def write_bone_structure(dae_file):
    
    bone_structure_buffer=get_bone_stucture_buffer()
    print(bone_structure_buffer)
    bind_pose_index=0
    #Armature
    armature_name=get_armature_name()
    dae_file.write("<node id=\""+str(armature_name)+"\" name=\""+str(armature_name)+"\" type=\"NODE\">\n")
    dae_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")



    #Root Bone
    root_bone_name=get_root_bone_name()
    if get_bone_name_from_bind_pose_index(bind_pose_index) == str(root_bone_name):
        print("Writing Root Bone: " + Fore.CYAN + "[" + str(root_bone_name) + "]" + Style.RESET_ALL)
    else:
        print("ERROR - Bind Pose Doesnt Match Root Bone" + Fore.RED + "[FAIL]" + Style.RESET_ALL)  
          
    dae_file.write("<node id=\""+str(root_bone_name)+"\" name=\""+str(root_bone_name)+ "\" sid=\"" + str(root_bone_name) + "\" type=\"JOINT\">\n")
    dae_file.write("<matrix sid=\"transform\">")
    inverse_bind_transform=get_inverse_bind_transform(0)
    for row in range(4):
        for col in range(4):
            dae_file.write(str(inverse_bind_transform[row][col]) + " ")
    dae_file.write("</matrix>\n")

    bind_pose_index+=1
    close_node_count=0
    #get_bone_name_from_bind_pose_index(bind_pose_index)


    for i in range(bind_pos_matrix_count-1):
        for j in range(len(bone_structure_buffer.split("@"))-1):
            temp_bone_name=get_bone_name_from_bind_pose_index(i+1)
            if bone_structure_buffer.split("@")[j].split()[0].strip() == temp_bone_name:
                print("Writing Bone: " + Fore.CYAN + "[" + str(temp_bone_name) + "]" + Style.RESET_ALL)
                dae_file.write("<node id=\"" + str(temp_bone_name) + "\" name=\"" + str(temp_bone_name) + "\" sid=\"" + str(temp_bone_name) + "\" type=\"JOINT\">\n")
                dae_file.write("<matrix sid=\"transform\">")
                #Write bone transform (Inverse of Bind Transform)     
                inverse_bind_transform=get_inverse_bind_transform(i+1)
                for row in range(4):
                    for col in range(4):
                        dae_file.write(str(inverse_bind_transform[row][col]) + " ")

                dae_file.write("</matrix>\n")
                for bi in range(len(bone_structure_buffer.split("@"))-1):
                    if bone_structure_buffer.split("@")[bi].split()[0] == get_bone_name_from_bind_pose_index(i+1):
                        current_pos=int(bone_structure_buffer.split("@")[bi].split()[1])
                        #print("DEBUG - " +str(bone_structure_buffer.split("@")[bi].split()[0])+" CURRENT POSITION: " + str(current_pos))  
                    if ((i+2) < bind_pos_matrix_count-1) and bone_structure_buffer.split("@")[bi].split()[0] == get_bone_name_from_bind_pose_index(i+2):
                        
                        next_pos=int(bone_structure_buffer.split("@")[bi].split()[1])
                        #print("DEBUG - " +str(bone_structure_buffer.split("@")[bi].split()[0])+" NEXT POSITION: " + str(next_pos))            
                    elif ((i+2) > bind_pos_matrix_count-1):
                        next_pos=0

                    #Extra blender stuff for a later time
                    #dae_file.write("<extra>\n")
                    #dae_file.write("<technique profile=\"blender\">\n")
                    #dae_file.write("<layer sid=\"layer\" type=\"string\">0</layer>\n")
                    #dae_file.write("<roll sid=\"roll\" type=\"float\">-0.6829612</roll>\n")
                    #dae_file.write("<tip_x sid=\"tip_x\" type=\"float\">-1.817046</tip_x>\n")
                    #dae_file.write("<tip_y sid=\"tip_y\" type=\"float\">-0.9937923</tip_y>\n")
                    #dae_file.write("<tip_z sid=\"tip_z\" type=\"float\">-3.019416</tip_z>\n")
                    #dae_file.write("</technique>\n")
                    #dae_file.write("</extra>\n")





                #Close node if next bone is sibling
                if current_pos == next_pos and (i != (bind_pos_matrix_count-1)):
                    dae_file.write("</node>\n")
                #dont close if child.      
                #elif next_pos > current_pos:
                    #close_node_count+=1

                elif next_pos < current_pos and (i != (bind_pos_matrix_count-2)):
                    for close_count in range(int(current_pos) - int(next_pos) + 1):
                        dae_file.write("</node>\n")

                elif next_pos < current_pos and (i == (bind_pos_matrix_count-2)):
                    for close_count in range(int(current_pos) - int(next_pos)):
                        dae_file.write("</node>\n")
        #else:
            #print("ERROR - Bind Pose Name Doesnt Match" + Fore.RED + "[FAIL]" + Style.RESET_ALL)




        

        


    #dae_file.write("</node>\n")
    #dae_file.write("</node>\n")








def get_root_bone_name():
    for index in range(len(avatar_bone_name_hash_array)):
        if int(root_bone_name_hash) == int(avatar_bone_name_hash_array[index]):
            return get_avatar_bone_name(index)


def get_armature_name():
    for index in range(len(avatar_bone_name_hash_array)):
        if int(root_bone_name_hash) == int(avatar_bone_name_hash_array[index]):
            return avatar_bone_name_array.split()[index].split("/")[0]


def get_hash_from_index(bone_index):
    

    byte_1=bone_name_hash[bone_hash+6]+bone_name_hash[bone_hash+7]
    byte_2=bone_name_hash[bone_hash+4]+bone_name_hash[bone_hash+5]
    byte_3=bone_name_hash[bone_hash+2]+bone_name_hash[bone_hash+3]
    byte_4=bone_name_hash[bone_hash]+bone_name_hash[bone_hash+1]

    temp_bone_hash=int(byte_1+byte_2+byte_3+byte_4,16)
    for index in range(len(avatar_bone_name_hash_array)):
        if temp_bone_hash == avatar_bone_name_hash_array[index]:
            print("DEBUG - MATCH FOUND")
            return index


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


if asset_type == "goose" or asset_type == "npc":


#########################
# WRITE ROOT BONES
#########################









#########################
# WRITE CHILDREN BONES
#########################    




    draw_bone_stucture()
    write_bone_structure(collada_file)
          

#########################
# WRITE MESH NODES
#########################


    #collada_file.write("<node id=\"Node_000000000349DD80\" name=\"Node_000000000349DD80\" type=\"NODE\">\n")
    #collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
    #collada_file.write("</node>\n")
    #collada_file.write("<node id=\"Node_000000000349DD80_001\" name=\"Node_000000000349DD80.001\" type=\"NODE\">\n")
    #collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
    #collada_file.write("</node>\n")
    collada_file.write("<node id=\"" + str(asset_name) + "\" name=\"" + str(asset_name) + "\" type=\"NODE\">\n")
    collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
    collada_file.write("<instance_controller url=\"#" + str(collada_skin_id) + "\">\n")
    
    collada_skin_name

    collada_file.write("<skeleton>#" + str(collada_skin_name) + "</skeleton>\n")



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

if asset_type == "goose" or asset_type == "npc":
    collada_file.write("</instance_controller>\n")
    collada_file.write("</node>\n")

elif asset_type == "simple":
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



                

