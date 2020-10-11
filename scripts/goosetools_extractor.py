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



########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################



#Returns whether the asset is simple(i.g. Pumpkin) or has bone(i.g. Goose)
def get_asset_type(num_of_vertex, size_of_vertex_buffer):
    
    # Simple Structure (Type-A)
    if (size_of_vertex_buffer/num_of_vertex).is_integer():
        print("Model Structure: "+ Fore.YELLOW + "[SIMPLE]" +Style.RESET_ALL)
        return "simple"

    # Complex Structure (Type-B)
    else:

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





#Creates a blender friendly material name
def get_material_name(raw_material_data):

    return "ugg_material.00"+ str(material_count_index)



global material_vertex_count_array
material_vertex_count_array=""

current_material_count=0
def get_material_list(num_of_vertex, size_of_vertex_buffer):
    asset_type=get_asset_type(num_of_vertex, size_of_vertex_buffer)
    global material_vertex_count_array
    material_vertex_count_array=""
    
    global material_vertex_start_array
    material_vertex_start_array="0 "

    already_counted_vertex_array=""

    temp_material_list=""
    current_material=""
    previous_material=""
    current_material_count=1
    if asset_type == "simple":
        for vertex in range(num_of_vertex):
            
            current_material_buffer = get_simple_obj_color_hex(vertex, size_of_vertex_buffer)
            current_material=current_material_buffer.split()[0] + current_material_buffer.split()[1] + current_material_buffer.split()[2] + "ff"
            
            if previous_material.strip() != current_material.strip() and previous_material.strip() != "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
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

                

    
    elif asset_type == "complex":
        for vertex in range(num_of_vertex):
            
            current_material_buffer = get_obj_color_hex(vertex, size_of_vertex_buffer)
            current_material=current_material_buffer.split()[0] + current_material_buffer.split()[1] + current_material_buffer.split()[2] + "ff"
            
            if previous_material.strip() != current_material.strip() and previous_material.strip() != "":
                print("Processing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
                temp_material_list+=current_material + " "
                material_vertex_count_array+=str(current_material_count) + " "
                material_vertex_start_array+=str(vertex) + " "
                current_material_count=0
            else:
                current_material_count+=1              
            previous_material=current_material  
    
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
def get_complex_vertex_buffer_size(vertex_buffer_size):
    return vertex_buffer_size*get_complex_vertex_buffer_block_size()

def get_complex_color_buffer_block_size():
    return 12
def get_complex_color_buffer_size(vertex_buffer_size):
    return vertex_buffer_size*get_complex_color_buffer_block_size()

def get_complex_bone_buffer_block_size():
    return 32
def get_complex_bone_buffer_size(vertex_buffer_size):
    return vertex_buffer_size*get_complex_bone_buffer_block_size()
  

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
    
    byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]
    #error check
    color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

    return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)

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
        print("DEBUG - BIND POSE MATRIX")
        #bind_pose_buffer=str(line.split(":", maxsplit=1)[1].strip())







########################################################################################################################################
#PROCESS ASSET
########################################################################################################################################


asset_type=get_asset_type(vertex_count,vertex_buffer_size)

material_list=get_material_list(vertex_count,vertex_buffer_size)

if len(material_list.split()) == len(material_vertex_count_array.split()):
    print("Vertex Colors Optimization: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("WARNING: Assert Vertex Colors Not Optimized"+ Fore.YELLOW + "[WARNING]" +Style.RESET_ALL)    







########################################################################################################################################
#PRINT INFO
########################################################################################################################################



print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)


if asset_type == "simple":
    vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
    print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
elif asset_type == "complex":
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

collada_effect_id="tempMAT-fx"
collada_effect_name="tempMAT"

collada_library_material_id=collada_effect_name
collada_library_material_name=collada_effect_name





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

for material_num in range(len(material_list.split())+1):
    
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

for material_num in range(len(material_list.split())+1):
    
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
    if asset_type == "complex":
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
    if asset_type == "complex":
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
collada_color_source_name=str(asset_name)+"-mesh-colors"
collada_color_count=vertex_count

collada_file.write("<source id=\"" + collada_color_source_id + "\" name=\"" + collada_color_source_name + "\">\n")
collada_file.write("<float_array id=\"" + collada_color_array_name + "\" count=\""+str(collada_color_count*4)+"\"> ")

#Normals go here
for collada_color in range(int(collada_color_count)):
    
    if asset_type == "complex":
        collada_file.write(get_obj_color(collada_color,collada_color_count) + " 1 " )
    if asset_type == "simple":
         collada_file.write(get_simple_obj_color(collada_color,collada_color_count) + " 1 ")       
collada_file.write("</float_array>\n")


collada_file.write("<technique_common>\n")
collada_file.write("<accessor source=\"#" + str(collada_color_array_name) + "\" count=\"" + str(collada_color_count*4) + "\" stride=\"4\">\n")
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
for material_num in range(len(material_list.split())):
    print("DEBUG - MATERIAL NUM: " + str(material_num))
    new_material_flag=0
    collada_library_material_id=generate_material_name(material_num) + "-material"
    material_vertex_start=int(material_vertex_start_array.split()[material_num])
    material_vertex_end=int(material_vertex_count_array.split()[material_num])+material_vertex_start-1
    
    current_face_count=0
    for face in range(int(index_count/3)):
        temp_face=get_obj_face(face)
        v1=temp_face.split()[0]
        v2=temp_face.split()[1]
        v3=temp_face.split()[2]

        if (int(v1) <= int(material_vertex_end)) and (int(v2) <= int(material_vertex_end)) and (int(v3) <= int(material_vertex_end)):
            if ((int(v1) >= int(material_vertex_start)) and (int(v2) >= int(material_vertex_start)) and (int(v3) >= int(material_vertex_start))):
                current_face_count+=1

    collada_triangle_vertex_count=current_face_count

    collada_file.write("<triangles material=\"" + str(collada_library_material_id) + "\" count=\""+str(collada_triangle_vertex_count) + "\">\n")
    collada_file.write("<input semantic=\"VERTEX\" source=\"#" + collada_vertex_source_id + "\" offset=\"0\"/>\n")
    collada_file.write("<input semantic=\"NORMAL\" source=\"#" + collada_normal_source_id + "\" offset=\"1\"/>\n")
    collada_file.write("<input semantic=\"COLOR\" source=\"#" + collada_color_source_id + "\" offset=\"2\" set=\"0\"/>\n")

    #Write the index buffer
    collada_file.write("<p>")




    for face in range(int(index_count/3)):
        temp_face=get_obj_face(face)
        v1=temp_face.split()[0]
        v2=temp_face.split()[1]
        v3=temp_face.split()[2]
        
        if ((int(v1) > int(material_vertex_end)) or (int(v2) > int(material_vertex_end)) or (int(v3) > int(material_vertex_end))) and new_material_flag != 1:
            #print("Writing Material: "+ Fore.YELLOW + "["+ str(current_material)+"]" +Style.RESET_ALL)
            material_index+=1
            new_material_flag=1
        elif ((int(v1) >= int(material_vertex_start)) and (int(v2) >= int(material_vertex_start)) and (int(v3) >= int(material_vertex_start))) and new_material_flag != 1:
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

#########################
# COLLADA CONTROLELRS
#########################


collada_file.write("<library_controllers>\n")

collada_file.write("</library_controllers>\n")












collada_visual_scene_id="Scene"
collada_visual_scene_name="Scene"
collada_visual_scene_url="Scene"

collada_visual_scene_node_id=str(asset_name)
collada_visual_scene_node_name=str(asset_name)
"+str(collada_library_material_name) + "

#########################
# COLLADA BINDING
#########################
collada_file.write("<library_visual_scenes>\n")
collada_file.write("<visual_scene id=\"" + str(collada_visual_scene_id) + "\" name=\"" + str(collada_visual_scene_name) +"\">\n")
collada_file.write("<node id=\"Node_000000000349DD80\" name=\"Node_000000000349DD80\" type=\"NODE\">\n")
collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
collada_file.write("</node>\n")
collada_file.write("<node id=\"" + str(collada_visual_scene_node_id) + "\" name=\"" + str(collada_visual_scene_node_name) + "\" type=\"NODE\">\n")
collada_file.write("<matrix sid=\"transform\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
collada_file.write("<instance_geometry url=\"#"+str(collada_gemotery_id)+"\" name=\""+str(collada_name)+"\">\n")
collada_file.write("<bind_material>\n")
collada_file.write("<technique_common>\n")



#########################
# COLLADA BIND MATERIALS
#########################

for material_num in range(len(material_list.split())):
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





#########################
# End of COLLADA File
#########################
collada_file.close()









#print("Script Complete")
asset_file.close



                

