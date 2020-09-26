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

init()

print("Untitled Goose Game OBJ to ASSET")
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
#comb through file, line by line
print("Reading File...")
for line in YAML_LINE: 
    #print("Line{}: {}".format(count, line.strip()))
    if "m_Name:" in line:
        asset_name=str(line.split(":", maxsplit=1)[1].strip())
    if "m_VertexCount:" in line:
        vertex_count=int(line.split(":", maxsplit=1)[1].strip())
    if "indexCount" in line:
        index_count=int(line.split(":", maxsplit=1)[1].strip())
    if "m_IndexBuffer:" in line:
        index_buffer+=str(line.split(":", maxsplit=1)[1].strip())
    if "m_DataSize:" in line:
        vertex_buffer_size=int(line.split(":", maxsplit=1)[1].strip())
    if "_typelessdata:" in line:
        vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())
    count+=1

print("Extracted Header")
print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
print("Index: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertex: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)
vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
#print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)











##################################################################################################
#Preprocess Object File


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






#Preprocess MTL file

obj_material_path_ok=0
obj_material_path=sys.argv[2].split(".")[0] + ".mtl"
mtl_material_count_preprocess=0
mtl_material_buffer=""

if path.exists(obj_material_path):
    obj_material_path_ok=1
    print("Preprocessing file : "+Fore.GREEN + str(obj_material_filename) +Style.RESET_ALL)
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
                    mtl_material_error_temp=1  
            
            if "Kd" == line_mtl.split()[0].strip() and mtl_material_error_temp == 0:
                #store diffused colore data
                mtl_kd_array[(mtl_material_index-1)*3]=line_mtl.split()[1].strip()
                mtl_kd_array[(mtl_material_index-1)*3+1]=line_mtl.split()[2].strip()
                mtl_kd_array[(mtl_material_index-1)*3+2]=line_mtl.split()[3].strip()

                print("Import .mtl Material: "+Fore.GREEN + "[ " + str(obj_material_list.split()[mtl_material_index-1])+ " ]" +Style.RESET_ALL) 

else:

    print(".MTL File Not Found : "+Fore.RED + str(obj_material_path) +Style.RESET_ALL)

print("DEBUG MATERIAL INDEX COUNT:" + str(mtl_material_index))



print(".Obj Info")
print("Number of Objects: "+Fore.GREEN + str(obj_count_preprocess)+Style.RESET_ALL)
print("Object Names: "+Fore.GREEN + str(obj_name)+Style.RESET_ALL)
print("Number of Materials: "+Fore.GREEN + str(obj_material_count_preprocess)+Style.RESET_ALL)
print("Materials: "+Fore.GREEN +str(obj_material_list)+Style.RESET_ALL)
print("Total Vertex: "+Fore.GREEN +str(obj_vertex_array_size_preprocess)+Style.RESET_ALL)
print("Total Normal: "+Fore.GREEN +str(obj_normal_array_size_preprocess)+Style.RESET_ALL)
print("Total UV: "+Fore.GREEN +str(obj_uv_array_size_preprocess)+Style.RESET_ALL)
print("Total Face: "+Fore.GREEN +str(obj_face_array_size_preprocess)+Style.RESET_ALL)






##################################################################################################
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
obj_vertex_array= np.zeros((obj_count_preprocess*obj_vertex_array_size_preprocess)*3, dtype=float)





#Normals

obj_normal_array= np.zeros((obj_count_preprocess*obj_normal_array_size_preprocess)*3, dtype=float)

#UV

obj_uv_array= np.zeros((obj_count_preprocess*obj_uv_array_size_preprocess)*3, dtype=float)

#Faces

obj_face_array= np.zeros((obj_count_preprocess*obj_face_array_size_preprocess)*3, dtype=int)


#Colors

obj_color_array= np.zeros((obj_count_preprocess*obj_vertex_array_size_preprocess)*3, dtype=float)


#Object Header Information
obj_vert_count=0
obj_index_cound=0
obj_g1=''
obj_g2=''


obj_next_index=1
object_index=0

debug_count=0




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
                print("Linking Face to Material: "+ Fore.GREEN + str(line.split()[1]) +Style.RESET_ALL)
                obj_face_material=str(line.split()[1])
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

            #print("FACE 1: " +str(int(data1[0])))

            #print("FACE 2: " +str(int(data2[0])))

            #print("FACE 3: " +str(int(data3[0])))

            
            obj_face_array[obj_face_count*3]=int(data1[0])
            obj_face_array[obj_face_count*3+1]=int(data2[0])
            obj_face_array[obj_face_count*3+2]=int(data3[0])

            #print(str((int(data1[0])-1)*3) +"=="+ str(mtl_kd_array[(mtl_material_index-1)*3]))
            #Write Vertex Color Data
            

            #Write Vertex Color Data for face 1
            obj_color_array[(int(data1[0])-1)*3]=mtl_kd_array[(mtl_material_index-1)*3]
            obj_color_array[(int(data1[0])-1)*3+1]=mtl_kd_array[(mtl_material_index-1)*3+1]
            obj_color_array[(int(data1[0])-1)*3+2]=mtl_kd_array[(mtl_material_index-1)*3+2]

            #Write Vertex Color Data for face 2
            obj_color_array[(int(data2[0])-1)*3]=mtl_kd_array[(mtl_material_index-1)*3]
            obj_color_array[(int(data2[0])-1)*3+1]=mtl_kd_array[(mtl_material_index-1)*3+1]
            obj_color_array[(int(data2[0])-1)*3+2]=mtl_kd_array[(mtl_material_index-1)*3+2]


            #Write Vertex Color Data for face 3
            obj_color_array[(int(data3[0])-1)*3]=mtl_kd_array[(mtl_material_index-1)*3]
            obj_color_array[(int(data3[0])-1)*3+1]=mtl_kd_array[(mtl_material_index-1)*3+1]
            obj_color_array[(int(data3[0])-1)*3+2]=mtl_kd_array[(mtl_material_index-1)*3+2]



            #obj_face_array[obj_vertex_count_f*3]=int(str(line.split("/")[5]))
            #obj_face_array[obj_vertex_count_f*3+1]=int(str(line.split("/")[3]))
            #obj_face_array[obj_vertex_count_f*3+2]=int(str(line.split("/")[1]))
            obj_face_count+=1

        elif "#" in line:
            print("COMMENT: "+Fore.YELLOW +str(line.strip("\n")) + Style.RESET_ALL)

        else:
            print("PARSE ERROR: "+Fore.RED + "Could not Parse: " +str(line) + Style.RESET_ALL)
            print(str(obj_material_list.split()[obj_next_index]))

    #progress_bar_count+=1
    #bar.update(progress_bar_count)

    debug_count+=1

            

           
            

    
print("Object Info")
print("Number of Objects: "+Fore.GREEN + str(obj_count_preprocess)+Style.RESET_ALL)
for object_num in range(obj_count_preprocess):
    print("#######################################################")
    print("Object Number: " + str(object_num+1))
    print("Object Name: "+Fore.GREEN + str(obj_g1)+Style.RESET_ALL)
    print("Material: "+Fore.GREEN + str(obj_g2)+Style.RESET_ALL)
    print("Total Vertexs(v): "+Fore.GREEN +str(obj_vertex_count_preprocess)+Style.RESET_ALL)
    print("Total Normal(vn): "+Fore.GREEN +str(obj_normal_count_preprocess)+Style.RESET_ALL)
    print("Total Faces(f): "+Fore.GREEN +str(obj_face_count_preprocess)+Style.RESET_ALL)

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

if error_flag == 0:
#Create new Unity Asset File


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
            new_asset.write("    m_DataSize: "+ str(obj_vertex_count_preprocess*44)+"\n")
            print("    m_DataSize: "+ str(obj_vertex_count_preprocess*44)+"\n")
            print("Writting Vertex Buffer Data Size: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "_typelessdata:" in line:
            print("Typeless Data")
            new_asset.write("    _typelessdata: ")


            #Default for now is 44 bytes
            loop_byte = vertex_buffer_block_size
            loop_count=0
            vertex_decode="POS"
            for vertex_pointer in range(obj_vertex_count_preprocess):
                #print(str(vertex_pointer))
                #Write Vertex
                if vertex_decode=="POS":
                    #print("Writing Vector: " + str(vertex_pointer) +" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_vertex_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_vertex_array[vertex_pointer*3])))


                    new_asset.write(str(float_to_hex(obj_vertex_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(obj_vertex_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(obj_vertex_array[vertex_pointer*3+2])))



                    vertex_decode="NORM"
                #Write Normals
                if vertex_decode=="NORM":
                    #print("Writing Normal: " + str(vertex_pointer)+" Loop: " + str(loop_count))
                    #print("X RAW: " + str(obj_normal_array[vertex_pointer*3])+ " X CALC: "+ str(float_to_hex(obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(obj_normal_array[vertex_pointer*3])))
                    new_asset.write(str(float_to_hex(obj_normal_array[vertex_pointer*3+1])))
                    new_asset.write(str(float_to_hex(obj_normal_array[vertex_pointer*3+2])))
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


                    color_red_hex=hex(int(obj_color_array[vertex_pointer*3]*255/2)).split("x")[1]
                    color_green_hex=hex(int(obj_color_array[vertex_pointer*3+1]*255/2)).split("x")[1]
                    color_blue_hex=hex(int(obj_color_array[vertex_pointer*3+2]*255/2)).split("x")[1]



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

        else:
            new_asset.write(line)













else:
    print(Fore.RED + "Script Terminated. One or more Errors has prevented the asset from compiling" +Style.RESET_ALL)






#close all the files
object_file.close()
asset_file.close()


















                

