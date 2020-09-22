#GooseTool's Obj to Asset Converter
major=0
minor=4

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
import numpy as np
from string import *



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
print("Raw Buffers")
#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)





##################################################################################################
#Read OBJ File








#open Object file from command line
object_file = open(sys.argv[2], "r")
#Read file line by line
OBJECT_LINE = object_file.readlines()

#extract vertex buffer size
obj_vertex_count_preprocess=0
obj_normal_count_preprocess=0
obj_uv_count_preprocess=0
obj_face_count_preprocess=0
for line in OBJECT_LINE:
    if "v " in line:
        obj_vertex_count_preprocess+=1
    if "vn " in line:
        obj_normal_count_preprocess+=1
    if "vt " in line:
        obj_uv_count_preprocess+=1
    if "f " in line:
        obj_face_count_preprocess+=1



#Return to beginng
object_file.seek(0)
#Read file line by line
OBJECT_LINE = object_file.readlines()

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
obj_vertex_array= np.zeros((obj_vertex_count_preprocess)*3, dtype=float)
obj_vertex_count_v=0




#Normals
obj_vertex_count_vn=0
obj_normal_array= np.zeros((obj_normal_count_preprocess)*3, dtype=float)

#Faces
obj_vertex_count_f=0
obj_face_array= np.zeros((obj_face_count_preprocess)*3, dtype=int)
#Object Header Information
obj_vert_count=0
obj_index_cound=0
obj_g1=''
obj_g2=''





#comb through file, line by line
print("Reading Object File...")
for line in OBJECT_LINE: 
    #check for Errors
    if fail_flag == 0:

        #Find Object name
        if g1_found == 0 and v_found == 0 and vn_found == 0 and g2_found == 0 and f_found == 0 and "g " in line:
            obj_g1=str(line.split(" ", maxsplit=1)[1].strip())
            g1_found=1


        #Collect Verticies
        elif g1_found == 1 and v_found == 0 and vn_found == 0 and g2_found == 0 and f_found == 0 and "v " in line:
            #print("Reading Verticies")
            v_found=1
            obj_vertex_array[obj_vertex_count_v*3]=float(str(line.split()[1]))
            obj_vertex_array[obj_vertex_count_v*3+1]=float(str(line.split()[2]))
            obj_vertex_array[obj_vertex_count_v*3+2]=float(str(line.split()[3]))
            obj_vertex_count_v+=1


            #obj_vertex_array+=temp_vertex
        elif g1_found == 1 and v_found == 1 and vn_found == 0 and g2_found == 0 and f_found == 0 and "v " in line:
            v_found=1
            obj_vertex_array[obj_vertex_count_v*3]=float(str(line.split()[1]))
            obj_vertex_array[obj_vertex_count_v*3+1]=float(str(line.split()[2]))
            obj_vertex_array[obj_vertex_count_v*3+2]=float(str(line.split()[3]))
            obj_vertex_count_v+=1




        #Collect Normals
        elif g1_found == 1 and v_found == 1 and vn_found == 0 and g2_found == 0 and f_found == 0 and "vn " in line: 
            #print("Reading Normals")
            vn_found=1
            obj_normal_array[obj_vertex_count_vn*3]=float(str(line.split()[1]))
            obj_normal_array[obj_vertex_count_vn*3+1]=float(str(line.split()[2]))
            obj_normal_array[obj_vertex_count_vn*3+2]=float(str(line.split()[3]))
            #obj_normal_array[obj_vertex_count_vn*3]=0
            #obj_normal_array[obj_vertex_count_vn*3+1]=0
            #obj_normal_array[obj_vertex_count_vn*3+2]=0

            obj_vertex_count_vn+=1
            #print(str(line))
        elif g1_found == 1 and v_found == 1 and vn_found == 1 and g2_found == 0 and f_found == 0 and "vn " in line:
            vn_found=1
            obj_normal_array[obj_vertex_count_vn*3]=float(str(line.split()[1]))
            obj_normal_array[obj_vertex_count_vn*3+1]=float(str(line.split()[2]))
            obj_normal_array[obj_vertex_count_vn*3+2]=float(str(line.split()[3]))
            #obj_normal_array[obj_vertex_count_vn*3]=0
            #obj_normal_array[obj_vertex_count_vn*3+1]=0
            #obj_normal_array[obj_vertex_count_vn*3+2]=0
            #obj_vertex_count_vn+=1
            #print(str(line))
            

        #Find G2
        elif g1_found == 1 and v_found == 1 and vn_found == 1 and g2_found == 0 and f_found == 0 and "g " in line: 
            #print("Reading G2")
            g2_found=1
            obj_g2=str(line.split(" ", maxsplit=1)[1].strip())

        #Find Faces, Stored in reverse order
        elif g1_found == 1 and v_found == 1 and vn_found == 1 and g2_found == 1 and f_found == 0 and "f " in line:
            #print("Reading Faces")        
            f_found=1

            face_buffer=line.split()
            data1=face_buffer[1].split("/")
            data2=face_buffer[2].split("/")
            data3=face_buffer[3].split("/")
            print(data1[0])
            print(data2[0])
            print(data3[0])
            
            obj_face_array[obj_vertex_count_f*3]=int(data1[0])
            obj_face_array[obj_vertex_count_f*3+1]=int(data2[0])
            obj_face_array[obj_vertex_count_f*3+2]=int(data3[0])

            #obj_face_array[obj_vertex_count_f*3]=int(str(line.split("/")[5]))
            #obj_face_array[obj_vertex_count_f*3+1]=int(str(line.split("/")[3]))
            #obj_face_array[obj_vertex_count_f*3+2]=int(str(line.split("/")[1]))
            obj_vertex_count_f+=1
            #print(str(line))
        elif g1_found == 1 and v_found == 1 and vn_found == 1 and g2_found == 1 and f_found == 1 and "f " in line:
            f_found=1
            face_buffer=line.split()
            data1=face_buffer[1].split("/")
            data2=face_buffer[2].split("/")
            data3=face_buffer[3].split("/")
            
            obj_face_array[obj_vertex_count_f*3]=int(data1[0])
            obj_face_array[obj_vertex_count_f*3+1]=int(data2[0])
            obj_face_array[obj_vertex_count_f*3+2]=int(data3[0])
            #obj_face_array[obj_vertex_count_f*3]=int(str(line.split("/")[5]))
            #obj_face_array[obj_vertex_count_f*3+1]=int(str(line.split("/")[3]))
            #obj_face_array[obj_vertex_count_f*3+2]=int(str(line.split("/")[1]))
            obj_vertex_count_f+=1
            #print(str(line))
        else:
            print("PARSE ERROR: "+Fore.RED + "Could not Parse: " +str(line) + Style.RESET_ALL)

#check for errors
if g1_found == 0:
    print("PARSE ERROR: "+Fore.RED + "No verticies array name found!" +Style.RESET_ALL)
    error_flag=1
if v_found == 0:
    print("PARSE ERROR: "+Fore.RED + "No verticies array found!" +Style.RESET_ALL)
    error_flag=1
if vn_found == 0:
    print("PARSE ERROR: "+Fore.RED + "No normal array found!" +Style.RESET_ALL)
    error_flag=1
if g2_found == 0:
    print("PARSE ERROR: "+Fore.RED + "No face array name found!" +Style.RESET_ALL)
    error_flag=1
if f_found == 0:
    print("PARSE ERROR: "+Fore.RED + "No face array found!" +Style.RESET_ALL)
    error_flag=1
            

           
            

    
print("Extracted Object Header")
print("Asset Mesh Name: "+Fore.GREEN + str(obj_g1)+Style.RESET_ALL)
print("Asset Face Name: "+Fore.GREEN + str(obj_g2)+Style.RESET_ALL)
print("Vertex Count(v): "+Fore.GREEN +str(obj_vertex_count_v)+Style.RESET_ALL)
print("Normal Count(vn): "+Fore.GREEN +str(obj_vertex_count_vn)+Style.RESET_ALL)
print("Face Count(f): "+Fore.GREEN +str(obj_vertex_count_f*3)+Style.RESET_ALL)


print("Vertex Data")
#for vertex_data in range(obj_vertex_count_v):
    #print("Vertex: " + str(vertex_data) + " X: " + str(obj_vertex_array[vertex_data*3]) + " Y: " + str(obj_vertex_array[vertex_data*3+1]) + " Z: " + str(obj_vertex_array[vertex_data*3+2]))
for vertex_data in range(obj_vertex_count_vn):
    print("Normal: " + str(vertex_data) + " X: " + str(obj_normal_array[vertex_data*3]) + " Y: " + str(obj_normal_array[vertex_data*3+1]) + " Z: " + str(obj_normal_array[vertex_data*3+2]))
#for vertex_data in range(obj_vertex_count_f):
    #print("Face " + str(vertex_data) + ": " + str(obj_face_array[vertex_data*3]) + " " + str(obj_face_array[vertex_data*3+1]) + " " + str(obj_face_array[vertex_data*3+2]))





#Verify data

#Verify Asset Name
if asset_name == obj_g1:
    print("Asset Name: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("Asset Name: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
    #error_flag=1

#Verify Vertex Count
if vertex_count == obj_vertex_count_v:
    print("Vertex Data: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("Vertex Data: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
    #error_flag=1

#Verify Normal Count
if vertex_count == obj_vertex_count_vn:
    print("Normal Data: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("Normal Data: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
    #no normals
    #error_flag=1

#Verify Face Count
if index_count == obj_vertex_count_f*3:
    print("Face Data: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
else:
    print("Face Data: "+Fore.RED + "[FAIL]" +Style.RESET_ALL)
    #error_flag=1




bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2+len(index_buffer)+vertex_count*24)
progress_bar_count=0

if error_flag == 0:
#Create new Unity Asset File
    new_asset = open("compiled_asset_"+str(obj_g1)+".asset", "w")

    #return to beggining of file
    asset_file.seek(0)
    YAML_LINE = asset_file.readlines()
    for line in YAML_LINE:
        if "m_Name:" in line:
            new_asset.write("  m_Name: "+ asset_name+ "\n")
            print("Writting Asset Name: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_VertexCount:" in line:
            new_asset.write("    m_VertexCount: "+ str(int(obj_vertex_count_v))+ "\n")
            print("Writting Vertex Count Main: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "    vertexCount: " in line:
            new_asset.write("    vertexCount: "+ str(int(obj_vertex_count_v))+ "\n")
            print("Writting Vertex Count Sub: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "indexCount" in line:
            new_asset.write("    indexCount: "+ str(int(obj_vertex_count_f*3))+ "\n")
            print("Writting Index COunt: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "m_IndexBuffer:" in line:
            print("Writting Index Buffer: "+Fore.RED + "[IN PROGRESS]" +Style.RESET_ALL)
            new_asset.write("  m_IndexBuffer: ")
            for byte in range(obj_vertex_count_f):
                byte1 =format(obj_face_array[byte*3]-1,"04x")
                #print("Byte1: " + str(byte1))
                #print("First: " +str(byte1[:2]))
                #print("Second: " +str(byte1[-2:]))

                byte2 =format(obj_face_array[byte*+3+1]-1,"04x")
                #print("Byte2: " + str(byte2))
                #print("First: " +str(byte2[:2]))
                #print("Second: " +str(byte2[-2:]))

                byte3 =format(obj_face_array[byte*3+2]-1,"04x")
                #print("Byte3: " + str(byte3))
                #print("First: " +str(byte3[:2]))
                #print("second: " +str(byte3[-2:]))

                #write first byte first
                new_asset.write(str(byte1[-2:])+str(byte1[:2]))
                new_asset.write(str(byte2[-2:])+str(byte2[:2]))
                new_asset.write(str(byte3[-2:])+str(byte3[:2]))
            new_asset.write("\n")
            print("Writting Index Buffer: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)

        elif "m_DataSize:" in line:
            new_asset.write("    m_DataSize: "+ str(obj_vertex_count_v*20)+"\n")
            print("Writting Vertex Buffer Data Size: "+Fore.GREEN + "[OK]" +Style.RESET_ALL)
        elif "_typelessdata:" in line:
            print("Typeless Data")
            new_asset.write("    _typelessdata: ")
            print("Writting Vertex Buffer: "+Fore.RED + "[IN PROGRESS]" +Style.RESET_ALL)

            #Default for now is 44 bytes
            loop_byte = vertex_buffer_block_size
            loop_count=0
            vertex_decode="POS"
            for vertex_pointer in range(obj_vertex_count_v):
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
                    
                #Write Model Colors
                if vertex_decode=="COLOR":
                    #print("Writing COLOR: " + str(vertex_pointer)+" Loop: " + str(loop_count))
                    #just copy from source asset since its not decoded yet
                    data_position=int(vertex_pointer*vertex_buffer_block_size*2+80)

                    temp_string=''
                    #for index in range(8):
                     #   temp_string+=vertex_buffer[data_position+index]
                    #if temp_string in "ed5341ff":
                     #   color_string="63AAC2FF"
                     #   print("Replaced Color")
                   # else:
                     #   color_string=temp_string



                    #new_asset.write(str(color_string))

                    new_asset.write("63AAC2FF")


                    vertex_decode="POS"
                    









                if loop_count == loop_byte:
                    #print("Loop count reset")
                    vertex_decode="POS"
                    loop_count=0
                loop_count+=1
            new_asset.write("\n")












            print("Writting Vertex Buffer: "+Fore.GREEN + "[COMPLETE]" +Style.RESET_ALL)

        else:
            new_asset.write(line)
        progress_bar_count+=1
        bar.update(progress_bar_count)












else:
    print(Fore.RED + "SCript Terminated. One or more Errors has prevented the asset from compiling" +Style.RESET_ALL)






#close all the files
object_file.close()
asset_file.close()


















                

