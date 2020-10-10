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

# returns #num1 #num2 #num3
# face_number is zero indexed
def get_obj_face(face_number):

    f=face_number
    vertex_1=index_buffer[f*12+10] + index_buffer[f*12+11] + index_buffer[f*12+8] + index_buffer[f*12+9]
    vertex_2=index_buffer[f*12+6] + index_buffer[f*12+7] + index_buffer[f*12+4] + index_buffer[f*12+5]
    vertex_3=index_buffer[f*12+2] + index_buffer[f*12+3] + index_buffer[f*12+0] + index_buffer[f*12+1]

    pos_a=int((pos_a_msb+pos_a_lsb),16)+1
    pos_b=int((pos_b_msb+pos_b_lsb),16)+1
    pos_c=int((pos_c_msb+pos_c_lsb),16)+1

    return str(int(vertex_1,16)) + " " + str(int(vertex_2,16)) + " " + str(int(vertex_3,16))

















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
collad_normal_source_id=str(asset_name)+"-mesh-normals"
collad_normal_source_name=str(asset_name)+"-normals"
collada_normal_count=vertex_count


collada_color_array_name=str(asset_name)+"-mesh-colors-array"
collad_color_source_id=str(asset_name)+"-mesh-colors"
collad_color_source_name=str(asset_name)+"-colors"
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
collada_file.write("<authoring_tool>GooseTool's version: " + str(major) + "." + str(minor)"</authoring_tool>\n")
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

collada_file.write("<geometry id=\"" + collada_gemotery_id + " \" name=\"" + collada_name + "\">\n")
collada_file.write("<mesh>\n")


#########################
# Write COLLADA Vertex
#########################
collada_normal_array_name
collada_normal_source_id

collada_file.write("<source id=\"" + collada_vertex_source_id + "\">\n")
collada_file.write("<float_array id=\"" + collada_vertex_array_name + "\" count=\""+str(collada_vetex_count*3)+"\">")



#Vertex go here



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

collada_file.write("<source id=\"" + collada_normal_source_id + "\" name=\"" + collada_vertex_source_name + "\">\n")
collada_file.write("<float_array id=\"" + collada_normal_array_name + "\" count=\""+str(collada_normal_count*3)+"\">")



#Normals go here

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



#Write number of vertex for each face. Our data is 3 all the time because triangles
collada_file.write("<vcount>\n")
for vcount in int(index_count):
    collada_file.write("3 ")
collada_file.write("</vcount>\n")


#Write the index buffer
collada_file.write("<p>")
for face in int(index_count/3):
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
collada_file.write("<visual_scene id=\"Root\" name=\"Root\">\n")
collada_file.write("<node id=\"jam\"  name=\"jam\" type=\"NODE\">\n")
collada_file.write("<matrix sid=\"matrix\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
collada_file.write("<instance_geometry url=\"#meshId0\">\n")
collada_file.write("<bind_material>\n")
collada_file.write("<technique_common>\n")
collada_file.write("<instance_material symbol=\"defaultMaterial\" target=\"#m0mat\">\n")
collada_file.write("</instance_material>\n")
collada_file.write("</technique_common>\n")
collada_file.write("</bind_material>\n")
collada_file.write("</instance_geometry>\n")
collada_file.write("</node>\n")
collada_file.write("<node id=\"Node_000000000349DD80\"  name=\"Node_000000000349DD80\" type=\"NODE\">\n")
collada_file.write("<matrix sid=\"matrix\">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>\n")
collada_file.write(" </node>\n")
collada_file.write("</visual_scene>\n")
collada_file.write("</library_visual_scenes>\n")


collada_file.write("<scene>\n")
collada_file.write("<instance_visual_scene url=\"#Root\" />\n")
collada_file.write("</scene>\n")

collada_file.write("</COLLADA>\n")





#########################
# End of COLLADA File
#########################
collada_file.close()




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



                

