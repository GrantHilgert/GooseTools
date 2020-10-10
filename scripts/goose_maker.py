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





########################################################################################################################################
#FUNCTION DEFINITIONS
########################################################################################################################################


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
    v=get_complex_vertex_buffer_size()+vertex_number*get_complex_color_buffer_block_size()*2 
    word_s=vertex_buffer[v]+vertex_buffer[v+1]+vertex_buffer[v+2]+vertex_buffer[v+3]+vertex_buffer[v+4]+vertex_buffer[v+5]+vertex_buffer[v+6]+vertex_buffer[v+7]
    word_t=vertex_buffer[v+8]+vertex_buffer[v+9]+vertex_buffer[v+10]+vertex_buffer[v+11]+vertex_buffer[v+12]+vertex_buffer[v+13]+vertex_buffer[v+14]+vertex_buffer[v+15]

    float_s=round(float(str(struct.unpack('f', bytes.fromhex(word_s))).strip('(),')),7)
    float_t=round(float(str(struct.unpack('f', bytes.fromhex(word_t))).strip('(),')),7)

    return str(float_s) + " " + str(float_t)


def get_obj_color(vertex_number,vertex_buffer_size):
    v=get_complex_vertex_buffer_size()+vertex_number*get_complex_color_buffer_block_size()*2
    
    byte_red=vertex_buffer[v+16]+vertex_buffer[v+17]
    byte_green=vertex_buffer[v+18]+vertex_buffer[v+19]
    byte_blue=vertex_buffer[v+20]+vertex_buffer[v+21]
    #error check
    color_terminator=vertex_buffer[v+22]+vertex_buffer[v+23]
    if color_terminator != "ff":
        print(Fore.RED + "Data Error: Vertex: " + str(vertex_number) + " color buffer Corrupt" +Style.RESET_ALL)








    data_pos_index="UV X"
    for long_index in range(int(get_complex_color_buffer_block_size()/4)):
        #print("POS: " + data_pos_index + " : " + str(long_index))
        temp_string=""
        #Create a LONG string from 8 characters
        for temp_index in range(8):
            #collect one double from the string
            temp_string+=vertex_buffer[(int(get_complex_vertex_buffer_block_size()/4)+long_index)*8+temp_index]

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
    print("Complex Vertex Buffer Block Size: " +Fore.GREEN+ str(get_complex_vertex_buffer_size(vertex_count))+Style.RESET_ALL)
    print("Complex Color and UV Buffer Block Size: " +Fore.GREEN+ str(get_complex_color_buffer_size(vertex_count))+Style.RESET_ALL)
    print("Complex Bone Buffer Block Size: " +Fore.GREEN+ str(get_complex_bone_buffer_size(vertex_count))+Style.RESET_ALL)

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
print("DEBUG - SIMPLE COLOR for loop size:" + str(int(vertex_count*get_complex_vertex_buffer_block_size()/4)))
material_buffer_write_count=0
if asset_type == "simple":
    data_pos_index="POS X"
    for long_index in range(int(vertex_count*get_complex_vertex_buffer_block_size()/4)):

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
    for long_index in range(int(get_complex_color_buffer_block_size()/4)):
        #print("POS: " + data_pos_index + " : " + str(long_index))
        temp_string=""
        #Create a LONG string from 8 characters
        for temp_index in range(8):
            #collect one double from the string
            temp_string+=vertex_buffer[(int(get_complex_vertex_buffer_block_size()/4)+long_index)*8+temp_index]

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
# Write COLLADA FILE
########################################################################################################################################



#####################
# SIMPLE STRUCTURE
#####################
# Variables
collada_gemotery_id=str(asset_name)+"-mesh"
collada_name=str(asset_name)


collada_vertex_array_name=str(asset_name)+"-mesh-positions-array"
collada_vertex_source_id=str(asset_name)+"-mesh-positions"
collada_vertex_source_name=str(asset_name)+"-positions"
collada_vetex_count=vertex_count

collada_normal_array_name=str(asset_name)+"-mesh-normals-array"
collada_normal_source_id=str(asset_name)+"-mesh-normals"
collada_normal_source_name=str(asset_name)+"-normals"
collada_normal_count=vertex_count


collada_color_array_name=str(asset_name)+"-mesh-colors-array"
collada_color_source_id=str(asset_name)+"-mesh-colors"
collada_color_source_name=str(asset_name)+"-colors"
collada_color_count=vertex_count



collada_face_array_name=""
collada_face_source_name=""
collada_face_count=index_count







collada_file = open(sys.argv[1].split(".")[0]+".dae", "w")
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
#collada_file.write("<camera id=\"Camera-camera\" name=\"Camera\">\n")
#collada_file.write("<optics>\n")
#collada_file.write("<technique_common>\n")
#collada_file.write("<perspective>\n")
#collada_file.write("<xfov sid="xfov">49.13434</xfov>\n")
#collada_file.write("<aspect_ratio>1.777778</aspect_ratio>\n")
#collada_file.write("<znear sid=\"znear\">0.1</znear>\n")
#collada_file.write("<zfar sid=\"zfar\">100</zfar>\n")
#collada_file.write("</perspective>\n")
#collada_file.write("</technique_common>\n")
#collada_file.write("</optics>\n")
#collada_file.write("<extra>\n")
#collada_file.write("<technique profile="blender">\n")
#collada_file.write("<YF_dofdist>0</YF_dofdist>\n")
#collada_file.write("<shiftx>0</shiftx>\n")
#collada_file.write("<shifty>0</shifty>\n")
#collada_file.write("</technique>\n")
#collada_file.write("</extra>\n")
#collada_file.write("</camera>\n")
#collada_file.write("</library_cameras>\n")
#collada_file.write("<library_images>\n")
#collada_file.write("<image id="character_Texture_png" name="character_Texture_png">\n")
#collada_file.write("<init_from>character%20Texture.png</init_from>\n")
#collada_file.write("</image>\n")
#collada_file.write("</library_images>\n")


collada_file.write("<library_effects>\n")
collada_file.write("<effect id=\"Material-effect\">\n")
collada_file.write("<profile_COMMON>\n")
#collada_file.write("<newparam sid="character_Texture_png-surface">\n")
#collada_file.write("<surface type="2D">\n")
#collada_file.write("<init_from>character_Texture_png</init_from>\n")
#collada_file.write(" </surface>\n")
#collada_file.write("</newparam>\n")
#collada_file.write("<newparam sid="character_Texture_png-sampler">\n")
#collada_file.write("<sampler2D>\n")
#collada_file.write("<source>character_Texture_png-surface</source>\n")
#collada_file.write("</sampler2D>\n")
#collada_file.write("</newparam>\n")

collada_file.write("<technique sid=\"common\">\n")
collada_file.write("<phong>\n")
#collada_file.write("<emission>\n")
#collada_file.write("<color sid="emission">0 0 0 1</color>\n")
#collada_file.write("</emission>\n")
#collada_file.write("<ambient>\n")
#collada_file.write("<color sid="ambient">0 0 0 1</color>\n")
#collada_file.write("</ambient>\n")
#collada_file.write("<diffuse>\n")
#collada_file.write("<texture texture="character_Texture_png-sampler" texcoord="UVMap"/>\n")
#collada_file.write("</diffuse>\n")
#collada_file.write("<specular>\n")
#collada_file.write("<color sid="specular">0.5 0.5 0.5 1</color>\n")
#collada_file.write("</specular>\n")
#collada_file.write("<shininess>\n")
#collada_file.write("<float sid="shininess">50</float>\n")
#collada_file.write("</shininess>\n")
#collada_file.write("<index_of_refraction>\n")
#collada_file.write("<float sid="index_of_refraction">1</float>\n")
#collada_file.write("</index_of_refraction>\n")


collada_file.write("</phong>\n")
collada_file.write("</technique>\n")
collada_file.write("</profile_COMMON>\n")
collada_file.write("</effect>\n")
collada_file.write("</library_effects>\n")
collada_file.write("<library_materials>\n")
collada_file.write("<material id\"Material-material\" name=\"Material\">\n")
collada_file.write("<instance_effect url=\"#Material-effect\"/>\n")
collada_file.write("</material>\n")
collada_file.write("</library_materials>\n")
collada_file.write("<library_geometries>\n")

collada_file.write("<geometry id=\"" + collada_gemotery_id + "\" name=\"" + collada_name + "\">\n")
collada_file.write("<mesh>\n")


#########################
# Write COLLADA Vertex
#########################
collada_normal_array_name
collada_normal_source_id

collada_file.write("<source id=\"" + collada_vertex_source_id + "\">\n")
collada_file.write("<float_array id=\"" + collada_vertex_array_name + "\" count=\""+str(collada_vetex_count*3)+"\"> ")



#Vertex go here
for collada_vertex in range(int(collada_vetex_count)):
    collada_file.write(get_obj_vertex(collada_vertex,collada_vetex_count) + " ")




collada_file.write("</float_array>\n")

collada_file.write("<technique_common>\n")
collada_file.write("<accessor count=\""+str(collada_vetex_count)+"\" offset=\"0\" source=\"#" + collada_vertex_source_id + "\" stride=\"3\">\n")
collada_file.write("<param name=\"X\" type=\"float\" />\n")
collada_file.write("<param name=\"Y\" type=\"float\" />\n")
collada_file.write("<param name=\"Z\" type=\"float\" />\n")
collada_file.write("</accessor>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</source>\n")

#########################
# Write COLLADA Normal
#########################

collada_file.write("<source id=\"" + collada_normal_source_id + "\" name=\"" + collada_normal_source_name + "\">\n")
collada_file.write("<float_array id=\"" + collada_normal_array_name + "\" count=\""+str(collada_normal_count*3)+"\"> ")

#Normals go here
for collada_normal in range(int(collada_normal_count)):
    collada_file.write(get_obj_normal(collada_normal,collada_normal_count) + " ")

collada_file.write("</float_array>\n")
collada_file.write("<technique_common>\n")
collada_file.write("<accessor count=\""+str(collada_normal_count)+"\" offset=\"0\" source=\"#" + collada_normal_source_id + "\" stride=\"3\">\n")
collada_file.write("<param name=\"X\" type=\"float\" />\n")
collada_file.write("<param name=\"Y\" type=\"float\" />\n")
collada_file.write("<param name=\"Z\" type=\"float\" />\n")
collada_file.write("</accessor>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</source>\n")



#########################
# Write COLLADA Colors
#########################

#collada_color_array_name
#collad_color_source_id
#collad_color_source_name
#collada_color_count






#######################################
# Write COLLADA Polylist (.OBJ Faces)
#######################################

collada_file.write("<polylist count=\""+str(index_count)+"\" material=\"defaultMaterial\">\n")
collada_file.write("<input offset=\"0\" semantic=\"VERTEX\" source=\"#" + collada_vertex_source_id + "\" />\n")
collada_file.write("<input offset=\"0\" semantic=\"NORMAL\" source=\"#" + collada_normal_source_id + "\" />\n")
#COLOR PLACEHOLDER 
#collada_file.write("<input offset=\"0\" semantic=\"COLOR\" source=\"#" + collada_color_source_id + "\" />\n")
#UV PLACEHOLDER 
#collada_file.write("<input offset=\"0\" semantic=\"TEXCOORD\" source=\"#" + collada_uv_source_id + "\" />\n")


#Write number of vertex for each face. Our data is 3 all the time because triangles
collada_file.write("<vcount>")
for vcount in range(int(index_count/3)):
    collada_file.write("3 ")
collada_file.write("</vcount>\n")


#Write the index buffer
collada_file.write("<p>")
for face in range(int(index_count/3)):
    #Write Vertex
    collada_file.write(get_obj_face(face) + " ")
    #Write Normal (Shares position with vertex)
    collada_file.write(get_obj_face(face) + " ")
    #Write Colors
    #TBD

collada_file.write("</polylist>\n")
collada_file.write("</mesh>\n")
collada_file.write("</geometry>\n")
collada_file.write("</library_geometries>\n")

#########################
# COLLADA CONTROLELRS
#########################


collada_file.write("<library_controllers>\n")















collada_file.write("</library_controllers>\n")

#########################
# COLLADA BINDING
#########################

collada_file.write("<library_visual_scenes>\n")
#collada_file.write("<visual_scene id=\"Root\" name=\"Root\">\n")
#collada_file.write("<node id=\"jam\"  name=\"jam\" type=\"NODE\">\n")
#collada_file.write("<matrix sid=\"matrix\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
#collada_file.write("<instance_geometry url=\"#meshId0\">\n")
#collada_file.write("<bind_material>\n")
#collada_file.write("<technique_common>\n")
#collada_file.write("<instance_material symbol=\"defaultMaterial\" target=\"#m0mat\">\n")
#collada_file.write("</instance_material>\n")
#collada_file.write("</technique_common>\n")
#collada_file.write("</bind_material>\n")
#collada_file.write("</instance_geometry>\n")
#collada_file.write("</node>\n")
#collada_file.write("<node id=\"Node_000000000349DD80\"  name=\"Node_000000000349DD80\" type=\"NODE\">\n")
#collada_file.write("<matrix sid=\"matrix\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
#collada_file.write(" </node>\n")
#collada_file.write("</visual_scene>\n")
collada_file.write("</library_visual_scenes>\n")


#collada_file.write("<scene>\n")
#collada_file.write("<instance_visual_scene url=\"#Root\" />\n")
#collada_file.write("</scene>\n")

collada_file.write("</COLLADA>\n")





#########################
# End of COLLADA File
#########################
collada_file.close()




########################################################################################################################################
#WRITE VERTEX
########################################################################################################################################









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



    #print(kd_red_hex + " " + kd_green_hex + " " + kd_blue_hex)

    kd_red=(int(kd_red_hex,16))/255
    kd_green=(int(kd_green_hex,16))/255
    kd_blue=(int(kd_blue_hex,16))/255
    #print(str(kd_red) + " " + str(kd_green) + " " + str(kd_blue))

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



                

