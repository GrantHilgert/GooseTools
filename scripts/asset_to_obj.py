#GooseTools Asset to .Obj Converter
major=0
minor=5

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
print("September 2020")


def get_material_name(raw_material_data):

    return "ugg_material.00"+ str(material_count_index)



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

print("Extracted Header")
print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Indexs: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertexs: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)
vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
#print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)


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

####################################################################
#New .OBJ and .MTL Creation Routine



# 11 Double file structure
# long 1: X
# long 2: Y
# DOuble 3: Z
# Double 4: Normal X
# Double 5: Normal Y
# DOuble 6: Normal Z
# Double 7: Unknown
# Double 8: Unknown
# Double 9: Unknown
# Doublw 10: Unknown
# Double 12: 3 Byte COlOR + "FF" TERMINATOR?


#POS: Positon
#NORM: Normal
#SKIP: Unknown
#COLOR: COLOR
#USEMTL: MATERIAL




data_pos_index="POS X"

#number of bytes to skip until next write
skip_count=0
#Dont write on the same loop
write_flag=0
#Write Vertex Data and collect material data at the same time to save time
print("VERTEX RANGE: " + str(int(vertex_count*vertex_buffer_block_size/4)))
for long_index in range(int(vertex_count*vertex_buffer_block_size/4)):
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
            data_pos_index="SKIP"
            write_flag=1

    if data_pos_index.split()[0].strip() == "SKIP":
        skip_count+=1
    if data_pos_index.split()[0] =="SKIP" and skip_count==9 and write_flag == 0:
        data_pos_index="COLOR"
        skip_count=0
        write_flag=1

        #Add Material to buffer
        current_material=str(temp_string)        
        material_buffer+=current_material + " "

        if current_material != old_material:
            old_material=current_material
            material_list+=current_material + " "
            print("Found Material"+ Fore.GREEN + "[RAW: " + current_material + " ]" +Style.RESET_ALL)
        data_pos_index="POS X"

    write_flag=0
    #print(data_pos_index + str(skip_count))


#End New Vertex Write and Color Extraction Routine
####################################################################
#Being New Normal Write Routine


data_pos_index="NORM X"
#Write Normal Data
normal_offset=12
print("NORMAL RANGE: " + str(int(vertex_count*vertex_buffer_block_size/4)))
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
    if data_pos_index.split()[0] =="SKIP":
        skip_count+=1
    if data_pos_index.split()[0] =="SKIP" and skip_count==6:
        data_pos_index="POS X"
        skip_count=0
    write_flag=0


        

#End New Normal Write Routine
####################################################################
#Begin Face Write






binary_file.write("g " + str(asset_name) + "_0\n")




current_face_color=""
old_face_color=""




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

for item in range(len(material_buffer.split())):
    print("item " + str(item) + " : "+ material_buffer.split()[item])
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

            print(str(pos_a)+" "+str(pos_b))
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

material_count_index=0
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



                

