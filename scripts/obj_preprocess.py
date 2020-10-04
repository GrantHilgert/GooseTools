#Object PreProcessor
major=1
minor=1

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
import numpy as np
from string import *
from shutil import copyfile


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



def replace_color(vertex_num,new_color):


    return "63aacsff"


def get_material_name(raw_material_data):

    return "ugg_material.00"+ str(material_count_index)

init()

print("GooseTools .Obj Preprocessor")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")




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

count=0




##################################################################################################
#Preprocess
#Get Size of Buffers









#open Object file from command line
object_file = open(sys.argv[1], "r")


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
print("Preprocessing file : "+Fore.GREEN + str(sys.argv[1].split("\\")[len(sys.argv[1].split("\\"))-1]) +Style.RESET_ALL)
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


print("Source Object file preprocessing: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

print("Preprocess Vertex Count(v): "+Fore.GREEN +str(obj_vertex_count_preprocess)+Style.RESET_ALL)
print("Preprocess Normal Count(vn): "+Fore.GREEN +str(obj_normal_count_preprocess)+Style.RESET_ALL)
print("Preprocess UV Count(vt): "+Fore.GREEN +str(obj_uv_count_preprocess)+Style.RESET_ALL)
print("Preprocess FACE Count(f): "+Fore.GREEN +str(obj_face_count_preprocess)+Style.RESET_ALL)

#Return to beginng
object_file.seek(0)

##################################################################################################









#Copy new Material File
copyfile(sys.argv[1].split(".")[0] + ".mtl", sys.argv[1].split(".")[0] +"_processed.mtl")


#Parse Control
g1_found=0
g2_found=0
v_found=0
vn_found=0
f_found=0
fail_flag=0
error_flag=0





#object Name
object_name=''
object_name_flag=0

#object Materials
object_material_path=''
object_material_path_flag=0

#Verticies
obj_vertex_array= np.zeros((obj_vertex_count_preprocess)*3, dtype=float)
obj_vertex_count=0

#Normals
obj_normal_array= np.zeros((obj_normal_count_preprocess+3)*3, dtype=float)
obj_normal_count=0

#Regenerated

if obj_vertex_count_preprocess > obj_normal_count_preprocess:
    new_obj_normal_array= np.zeros((obj_vertex_count_preprocess+3)*3, dtype=float)
else:
    new_obj_normal_array= np.zeros((obj_normal_count_preprocess+3)*3, dtype=float)
new_obj_normal_count=0


#UV
obj_uv_array= np.zeros((obj_uv_count_preprocess)*2, dtype=float)
obj_uv_count=0

#Faces
obj_face_array= np.zeros((obj_face_count_preprocess*2)*3, dtype=int)
obj_face_count=0

#open Object file from command line
face_temp_file = open("preprocess_temp.txt", "w")





#materials
material_buffer=""
material_buffer_count=0


current_material=""
old_material=""

#comb through file, line by line
print("Reading Object File...")
#Read file line by line
OBJECT_LINE = object_file.readlines()
for line in OBJECT_LINE: 
    #check for Errors
    if fail_flag == 0 and " " in line:
        #print(line)
        #Find Object name
        if  object_name_flag == 0 and ("g " in line.split()[0] or "o" in line.split()[0]):
            obj_g1=str(line.split(" ", maxsplit=1)[1].strip()).split(".")[0]
            object_name_flag=1
            print("Object Name: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        if object_material_path_flag == 0 and "mtllib" in line.split()[0]:
            object_material_path=line.split()[1]
            object_material_path_flag=1
            print("Object Material Path: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "v " in line:
            #print(str(obj_vertex_count))
            obj_vertex_array[obj_vertex_count*3]=float(str(line.split()[1]))
            obj_vertex_array[obj_vertex_count*3+1]=float(str(line.split()[2]))
            obj_vertex_array[obj_vertex_count*3+2]=float(str(line.split()[3]))
            obj_vertex_count+=1


        #Collect Normals
        elif "vn" in line.split()[0] and len(line.split()) > 4: 
            #print(str(obj_normal_count)+ line)
            obj_normal_array[obj_normal_count*3]=float(str(line.split()[1]))
            obj_normal_array[obj_normal_count*3+1]=float(str(line.split()[2]))
            obj_normal_array[obj_normal_count*3+2]=float(str(line.split()[3]))
            obj_normal_count+=1

        #collect UV
        elif "vt" in line.split()[0]:
            #print(str(obj_uv_count))
            obj_uv_array[obj_uv_count*2]=float(str(line.split()[1]))
            obj_uv_array[obj_uv_count*2+1]=float(str(line.split()[2]))
            obj_uv_count+=1
            
        #collect material
        elif "usemtl" in line.split()[0]:
            current_material=line.split()[1]
            if current_material != old_material:
                old_material=current_material
                print("Linking Material: " + Fore.GREEN + "[RAW: " + current_material + " ]" +Style.RESET_ALL)

        #collect Faces
        elif "f" in line.split()[0]:


            if len(line.split()) > 4 :
                new_face_1=line.split()[1]+" "+line.split()[2]+" "+line.split()[3]
                new_face_2=line.split()[1]+" "+line.split()[3]+" "+line.split()[4]
                face_temp_file.write(str(new_face_1) + "\n")
                face_temp_file.write(str(new_face_2) + "\n")
                obj_face_count+=2               

                #Write Face Materials    
                material_buffer+=current_material + " " + current_material + " "
                material_buffer_count+=2



            else:
                face_temp_file.write(line.split(" ",1)[1])
                obj_face_count+=1
                #Write Face Materials  
                material_buffer+=current_material + " "
                material_buffer_count+=1




face_temp_file.close()
debug_count=0

face_temp_file = open("preprocess_temp.txt", "r")
new_face_temp_file = open("face_temp.txt", "w")

new_face_index=0
#Recompile file with one index buffer
#Read file line by line. 
FACE_LINE = face_temp_file.readlines()
for line in FACE_LINE:
    if fail_flag == 0:

        #Break apart into 3 Vertex Components
        v1=line.split()[0]
        v2=line.split()[1]
        v3=line.split()[2]

#VERTEX 1
        #print(str(debug_count)+" V1: " + str(v1) + " V2: " + str(v2) + " V3: " + str(v3))
        debug_count+=1
        
        if len(v1.split("/")) > 2:

            if v1.split("/")[0] == v1.split("/")[2]:
                # OK to copy current entry to new normal buffer
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+1]=obj_normal_array[(int(v1.split("/")[0])-1)*3+1]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+2]=obj_normal_array[(int(v1.split("/")[0])-1)*3+2]
                
            elif v1.split("/")[0] != v1.split("/")[2]:
                #Move entry to new buffer
                if new_obj_normal_array[(int(v1.split("/")[0])-1)*3] != 0 and new_obj_normal_array[(int(v1.split("/")[0])-1)*3] != obj_normal_array[(int(v1.split("/")[2])-1)*3]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)                               
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[2])-1)*3]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+1]=obj_normal_array[(int(v1.split("/")[2])-1)*3+1]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+2]=obj_normal_array[(int(v1.split("/")[2])-1)*3+2]


        elif len(v1.split("/")) == 2:

            if v1.split("/")[0] == v1.split("/")[1]:
                #also ok, just different split
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[0])-1)*3]


            elif v1.split("/")[0] != v1.split("/")[1]:
                if new_obj_normal_array[(int(v1.split("/")[0])-1)*3] != 0 and new_obj_normal_array[(int(v1.split("/")[0])-1)*3] != obj_normal_array[(int(v1.split("/")[1])-1)*3]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)                                                                  
                #Move entry to new buffer
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3]=obj_normal_array[(int(v1.split("/")[1])-1)*3]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+1]=obj_normal_array[(int(v1.split("/")[1])-1)*3+1]
                new_obj_normal_array[(int(v1.split("/")[0])-1)*3+2]=obj_normal_array[(int(v1.split("/")[1])-1)*3+2]
                





#VERTEX2

        if len(v2.split("/")) > 2:

            if v2.split("/")[0] == v2.split("/")[2]:
                # OK to copy current entry to new normal buffer
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3]=obj_normal_array[(int(v2.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1]=obj_normal_array[(int(v2.split("/")[0])-1)*3+1]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+2]=obj_normal_array[(int(v2.split("/")[0])-1)*3+2]

            elif v2.split("/")[0] != v2.split("/")[2]:
                #Move entry to new buffer
                if new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1] != 0 and new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1] != obj_normal_array[(int(v2.split("/")[2])-1)*3+1]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)

                new_obj_normal_array[(int(v2.split("/")[0])-1)*3]=obj_normal_array[(int(v2.split("/")[2])-1)*3]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1]=obj_normal_array[(int(v2.split("/")[2])-1)*3+1]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+2]=obj_normal_array[(int(v2.split("/")[2])-1)*3+2]


        elif len(v2.split("/")) == 2:
            if v2.split("/")[0] == v2.split("/")[1]:
                print(v2.split("/")[0] +"=="+ v2.split("/")[1])
                #also ok, just different split
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3]=obj_normal_array[(int(v2.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1]=obj_normal_array[(int(v2.split("/")[0])-1)*3+1]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+2]=obj_normal_array[(int(v2.split("/")[0])-1)*3+2]

            elif v2.split("/")[0] != v2.split("/")[1]:
                print(v2.split("/")[0] +"!="+ v2.split("/")[1])
                if new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1] != 0 and new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1] != obj_normal_array[(int(v2.split("/")[1])-1)*3+1]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)

                #Move entry to new buffer
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3]=obj_normal_array[(int(v2.split("/")[1])-1)*3]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+1]=obj_normal_array[(int(v2.split("/")[1])-1)*3+1]
                new_obj_normal_array[(int(v2.split("/")[0])-1)*3+2]=obj_normal_array[(int(v2.split("/")[1])-1)*3+2]     

#VERTEX3


        if len(v3.split("/")) > 2:
            if v3.split("/")[0] == v3.split("/")[2]:
                # OK to copy current entry to new normal buffer
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3]=obj_normal_array[(int(v3.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+1]=obj_normal_array[(int(v3.split("/")[0])-1)*3+1]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2]=obj_normal_array[(int(v3.split("/")[0])-1)*3+2]

            elif v3.split("/")[0] != v3.split("/")[2]:
                #Move entry to new buffer
                if new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2] != 0 and new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2] != obj_normal_array[(int(v3.split("/")[2])-1)*3+2]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)                               
                #print("Copy Vertex w3 3 : " + str(obj_normal_array[int(v3.split("/")[2])*3+2]))

                new_obj_normal_array[(int(v3.split("/")[0])-1)*3]=obj_normal_array[(int(v3.split("/")[2])-1)*3]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+1]=obj_normal_array[(int(v3.split("/")[2])-1)*3+1]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2]=obj_normal_array[(int(v3.split("/")[2])-1)*3+2]


        elif len(v3.split("/")) == 2:

            if v3.split("/")[0] == v3.split("/")[1]:
                #also ok, just different split
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3]=obj_normal_array[(int(v3.split("/")[0])-1)*3]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+1]=obj_normal_array[(int(v3.split("/")[0])-1)*3+1]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2]=obj_normal_array[(int(v3.split("/")[0])-1)*3+2]
                #print("Keep Vertex w2 3 " + str(new_obj_normal_array[int(v3.split("/")[0])*3+2]))
            if v3.split("/")[0] != v3.split("/")[1]:
                if new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2] != 0 and new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2] != obj_normal_array[(int(v3.split("/")[1])-1)*3+2]:
                    print("COPY ERROR: "+Fore.RED + "Face Buffer not empty" +Style.RESET_ALL)                                                                  
                #Move entry to new buffer
                #print("Copy Vertex w3 3: " + v3.split("/")[0] +"!=" +v3.split("/")[1])
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3]=obj_normal_array[(int(v3.split("/")[1])-1)*3]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+1]=obj_normal_array[(int(v3.split("/")[1])-1)*3+1]
                new_obj_normal_array[(int(v3.split("/")[0])-1)*3+2]=obj_normal_array[(int(v3.split("/")[1])-1)*3+2]    
            





    new_v1=v1.split("/")[0]
    new_v2=v2.split("/")[0]
    new_v3=v3.split("/")[0]

    #new_uv1=v1.split("/")[0]
    #new_uv2=v2.split("/")[0]
    #new_uv3=v3.split("/")[0]

    new_uv1=""
    new_uv2=""
    new_uv3=""


    new_vn1=v1.split("/")[0]
    new_vn2=v2.split("/")[0]
    new_vn3=v3.split("/")[0]

    new_face_temp_file.write(new_v1+"/"+new_uv1+"/"+new_vn1+" ")
    new_face_temp_file.write(new_v2+"/"+new_uv2+"/"+new_vn2+" ")
    new_face_temp_file.write(new_v3+"/"+new_uv3+"/"+new_vn3+" ")
    new_face_temp_file.write("\n")
    new_face_index+=1

new_face_temp_file.close()

########################################################################################################
#Write new processed .OBJ file.
new_obj_file = open(str(sys.argv[1]).split(".")[0] + "_processed.obj", "w")
new_obj_file.write("# GooseTools .OBJ Preprocessor V." + str(major) + "." + str(minor))
new_obj_file.write("\n# https://github.com/GrantHilgert/GooseTools\n")



#########################
#write Material file name
new_obj_file.write("mtllib " + str(obj_material_filename) + "\n")

#########################
#Write .OBJ filename 
new_obj_file.write("o " + str(obj_g1) + "\n")



#########################
#Write Vertex
vertex_write_count=0
for index in range(int(len(obj_vertex_array)/3)):
    new_obj_file.write("v " + str(obj_vertex_array[index*3]) + " "+ str(obj_vertex_array[index*3+1]) +" "+ str(obj_vertex_array[index*3+2]) + "\n")
    vertex_write_count+=1


########################
#Write Normals



normal_write_count=0
for index in range(int(len(obj_normal_array)/3)):
    #print("Writing Normal: "+str(index)+"vn " + str(new_obj_normal_array[index*3]) + " "+ str(new_obj_normal_array[index*3+1]) +" "+ str(new_obj_normal_array[index*3+2]))

    new_obj_file.write("vn " + str(new_obj_normal_array[(index)*3]) + " "+ str(new_obj_normal_array[(index)*3+1]) +" "+ str(new_obj_normal_array[(index)*3+2]) + "\n")
    normal_write_count+=1



########################
#Write Object Face name?
new_obj_file.write("g " + str(obj_g1) + "_0\n")






########################
#Write Face Material
current_material=""
old_material=""












face_temp_file.close()

material_buffer_index=0
old_material=""
current_material=""

new_face_temp_file = open("face_temp.txt", "r")
face_write_count=0
NEW_FACE_LINE = new_face_temp_file.readlines()

for line in NEW_FACE_LINE:
    

    current_material=material_buffer.split()[material_buffer_index].strip()
    material_buffer_index+=1
    #print(str(current_material))
    if current_material != old_material:
        old_material=current_material
        print("Writting Material: "+ Fore.GREEN + "[ "+ current_material + " ]" +Style.RESET_ALL)
        new_obj_file.write("usemtl " + current_material+"\n")


    new_obj_file.write("f " + str(line))
    face_write_count+=1












           
            

    
print("Proccessed .OBJ Parameters")
print("Asset Mesh Name: "+Fore.GREEN + str(obj_g1)+Style.RESET_ALL)
print("Asset Material File: "+Fore.GREEN + str(object_material_path)+Style.RESET_ALL)

#print("Asset Face Name: "+Fore.GREEN + str(obj_g2)+Style.RESET_ALL)
print("New Vertex Count(v): "+Fore.GREEN +str(vertex_write_count)+Style.RESET_ALL)
print("New Normal Count(vn): "+Fore.GREEN +str(normal_write_count)+Style.RESET_ALL)
print("New Face Count(f): "+Fore.GREEN +str(face_write_count)+Style.RESET_ALL)













#close all the files
object_file.close()
new_obj_file.close()
asset_file.close()
face_temp_file.close()

















                

