#GooseTools Asset to UABE FIle Converter
major=0
minor=3

import sys
from colorama import Fore, Back, Style, init
import time
import progressbar
import struct
import numpy as np
from textwrap import wrap
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


init()

print("Untitled Goose Game ASSET to UABE Resource")
print("Version: " + str(major) + "." + str(minor))
print("Written by Grant Hilgert")
print("https://github.com/GrantHilgert/GooseTools")

error_flag=0


#open asset file from command line
asset_file = open(sys.argv[1], "r")




#########################################################################
#PreProcessing





#Bind Pose Preprocessing
bind_pose_preprocess_flag=0
bind_pose_buffer_size=0




#Preprocess File - Extract Buffer sizes and such
YAML_LINE = asset_file.readlines()
for line in YAML_LINE:
    if "m_BindPose:" in line:
        bind_pose_preprocess_flag=1
    elif bind_pose_preprocess_flag == 1 and "m_BindPose:" not in line:
        #print("BUFFER COUNT: " +str(bind_pose_buffer_size)+" LINE: " + str(line))
        bind_pose_buffer_size+=1
    if "m_BoneNameHashes:" in line:
        bind_pose_buffer_size-=1
        bind_pose_preprocess_flag=0
        print("Pose Binding Preprocessing: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)



#return to beginning of file
asset_file.seek(0)
#########################################################################



asset_name='NA'
index_count='NA'
vertex_count='NA'
index_buffer=''
vertex_buffer='NA'
vertex_buffer_size='NA'
vertex_buffer_block_size='NA'


#Extended
center_buffer=''
center_x=0
center_y=0
center_z=0
extent_x=0
extent_y=0
extent_z=0

#Bind Pose
#eventually 
bind_pose_matrix_size=16
bind_pose_data= np.zeros(bind_pose_buffer_size, dtype=float)
bind_pose_text_array=''
bind_pose_flag=0
bind_pose_complete=0
bind_pose_size=0
bind_pose_index=0
bind_pose_local_e=0
bind_pose_max_e=0


#Root Bone Name 
root_bone_name_hash=''
bone_name_hash_array=''


#m_channels. I count 14 channels, is this dynamic? I dont know/dont care until it become a problem
m_channel_len=14
m_channel_array= np.zeros((m_channel_len)*4, dtype=int)
m_channel_flag=0
m_channel_fail_flag=0
m_channel_complete=0
m_channel_state="STREAM"
#line positon
m_channel_index=0
#Total number of channels
m_channel_count=0
#Number of channels used on this model
m_channel_used=0


#Other flags and such
mesh_usage_flag=0


#########################################################################
#Unity .Asset file parser
#comb through file, line by line
count=0
print("Reading File...")
YAML_LINE = asset_file.readlines()
for line in YAML_LINE: 
    #print("Line{}: {}".format(count, line.strip()))
    if "m_Name:" in line:
        asset_name=str(line.split(":", maxsplit=1)[1].strip())
        print("Asset Name: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "m_VertexCount:" in line:
        vertex_count=int(line.split(":", maxsplit=1)[1].strip())
        print("Vertex Count: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "indexCount" in line:
        index_count=int(line.split(":", maxsplit=1)[1].strip())
        print("Index Count "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "m_IndexBuffer:" in line:
        index_buffer+=str(line.split(":", maxsplit=1)[1].strip())
        print("Index Buffer: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "m_DataSize:" in line:
        vertex_buffer_size=int(line.split(":", maxsplit=1)[1].strip())
        print("Vertex Buffer Size: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
        print("Vertex Buffer: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "_typelessdata:" in line:
        vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())
        print("Vertex Data: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)


    #Extended Parsing - Center
    if "      m_Center: " in line:
        center_buffer=str(line.split(":", maxsplit=1)[1].strip("{}"))
        center_x=str(center_buffer.split(",")[0]).split(":")[1]
        center_y=str(center_buffer.split(",")[1]).split(":")[1]
        center_z=str(str(center_buffer.split(",")[2]).split(":")[1]).split("}")[0]
        print("Center Data: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
    if "      m_Extent: " in line:
        extent_buffer=str(line.split(":", maxsplit=1)[1].strip("{}"))
        extent_x=str(extent_buffer.split(",")[0]).split(":")[1]
        extent_y=str(extent_buffer.split(",")[1]).split(":")[1]
        extent_z=str(str(extent_buffer.split(",")[2]).split(":")[1]).split("}")[0]
        print("Extent Data: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)

    #Bind Pose - Check for data
    if "  m_BindPose: []" in line:
        print("No Bind Pose Data: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
        bind_pose_flag=0
        bind_pose_complete=1
    elif "  m_BindPose:" in line:
        print("Binding Pose Strucutre: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
        bind_pose_flag=1
    #Bind Pose - capture data
    if bind_pose_flag == 1 and bind_pose_complete == 0 and "m_BindPose:" not in line:
        if "  m_BoneNameHashes: " in line:
            bone_name_hash_array+=str(line).split(":")[1]
            bind_pose_complete=1
        else:
            #Fix Scientific Notation
            if "E-" in line:
                bind_pose_text_array+=str(line).split(":")[1].strip().split("E-")[0]+"e-0"+str(line).split(":")[1].strip().split("E-")[1]
            else:
                bind_pose_text_array+=str(line).split(":")[1].strip()
            bind_pose_size+=1
            
            bind_pose_data[bind_pose_index]=float(str(line).split(":")[1].strip())
            #print(str(bind_pose_data[bind_pose_index]))
            bind_pose_index+=1


    #Bone Name Hash
    if "  m_RootBoneNameHash: " in line:
        root_bone_name_hash=str(line.split(":", maxsplit=1)[1].strip())
        print("Root Bone Name Hash: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)

    #Vertex Data encoding Channels
    if "m_Channels:" in line:
        m_channel_flag=1

    if m_channel_flag == 1 and m_channel_complete == 0 and "    m_Channels:" not in line:
        if "stream:" in line and m_channel_state != "STREAM":
            m_channel_fail_flag=1

        elif "stream:" in line and m_channel_state == "STREAM":
            m_channel_array[m_channel_index]=int(str(line).split(":")[1])
            m_channel_state="OFFSET"
        if "offset:" in line and m_channel_state != "OFFSET":
            m_channel_fail_flag=1

        elif "offset:" in line and m_channel_state == "OFFSET":
            m_channel_array[m_channel_index]=int(str(line).split(":")[1])
            m_channel_state="FORMAT"

        if "format:" in line and m_channel_state != "FORMAT":
            m_channel_fail_flag=1
        elif "format:" in line and m_channel_state == "FORMAT":
            m_channel_array[m_channel_index]=int(str(line).split(":")[1])
            m_channel_state="DIM"

        if "dimension:" in line and m_channel_state != "DIM":
            m_channel_fail_flag=1

        elif "dimension:" in line and m_channel_state == "DIM":
            m_channel_array[m_channel_index]=int(str(line).split(":")[1])
            m_channel_state="STREAM"
            m_channel_count+=1
            #check if channel has dimensions. I.E. It is used and is relevant to decoding
            if m_channel_array[m_channel_index] > 0:
                m_channel_used+=1
        if ("m_DataSize:" in line and m_channel_state != "STREAM") or m_channel_fail_flag == 1:
            print("Vertex Channel Encoding: "+Fore.RED +"[FAIL]"+Style.RESET_ALL)
            m_channel_complete=1
        elif"m_DataSize:" in line and m_channel_state == "STREAM":
            print("Vertex Channel Encoding: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
            m_channel_complete=1
        #Incriment array index
        m_channel_index+=1

    if "m_MeshUsageFlags:" in line:
            mesh_usage_flag=int(line.split(":", maxsplit=1)[1].strip())
            print("Mesh Usage Flag: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)        
        

    #Incriement line count
    count+=1




################################################################
#Post Processing












#calculate vertex buffer data block size and check if valid.
vertex_buffer_block_size=(vertex_buffer_size/vertex_count)
if vertex_buffer_block_size.is_integer():        
    print("Vertex Buffer Block Size: "+Fore.GREEN +"[OK]"+Style.RESET_ALL)
else:
    print("Vertex Buffer Block Size: "+Fore.RED +"[FAIL]"+Style.RESET_ALL)



print("\n###################Extracted Header###################")
print("Asset Name: "+Fore.GREEN + str(asset_name)+Style.RESET_ALL)
if bind_pose_flag == 1:

    print("Root Bone Name Hash: " +Fore.GREEN + str(root_bone_name_hash)+Style.RESET_ALL)

    print("Binding Pose Buffer Size: " +Fore.GREEN + str(bind_pose_buffer_size)+Style.RESET_ALL)




print("Index Count: "+Fore.GREEN +str(index_count)+Style.RESET_ALL)
print("Vertex Count: "+Fore.GREEN +str(vertex_count)+Style.RESET_ALL)
print("Vertex Buffer Size: "+ Fore.GREEN +str(vertex_buffer_size)+Style.RESET_ALL)
if vertex_buffer_block_size.is_integer():
    print("Vertex Buffer Block Size: " +Fore.GREEN+ str(vertex_buffer_block_size)+Style.RESET_ALL)
else:
    print("Vertex Buffer Block Size: " +Fore.RED+ str(vertex_buffer_block_size)+Style.RESET_ALL)
print("Vertex Encoding Channels Found: "+ Fore.GREEN +str(m_channel_count)+Style.RESET_ALL)
print("Vertex Encoding CHannels Used: "+ Fore.GREEN +str(m_channel_used)+Style.RESET_ALL)                
                









print("Center X: "+Fore.GREEN+str(center_x)+Style.RESET_ALL +" Y: "+Fore.GREEN+str(center_y)+Style.RESET_ALL+" Z: "+Fore.GREEN+str(center_z)+Style.RESET_ALL)
print("Extent X: "+Fore.GREEN+str(extent_x)+Style.RESET_ALL +" Y: "+Fore.GREEN+str(extent_y)+Style.RESET_ALL+" Z: "+Fore.GREEN+str(extent_z)+Style.RESET_ALL)


print("#######################################################")




#Print Debug Info
#print("Raw Buffers")
#print("BONE HASH NAME BUFFER: " + Fore.RED + str(bone_name_hash_array)+Style.RESET_ALL)




#print("CHANNEL ENCODING:")
#for index_item in range(int(len(m_channel_array)/4)):
    #print("CHANNEL: " + str(index_item))
    #print("STREAM: " + str(m_channel_array[index_item*4]))
    #print("OFFSET: " + str(m_channel_array[index_item*4+1]))
    #print("FORMAT: " + str(m_channel_array[index_item*4+2]))
    #print("DIMENSION: " + str(m_channel_array[index_item*4+3]))
    

#print("INDEX BUFFER: " + Fore.RED + str(index_buffer)+Style.RESET_ALL)
#print("VERTEX BUFFER: "+ Fore.RED + str(vertex_buffer)+Style.RESET_ALL)









################################################################
#Write New File for UABE



bar = progressbar.ProgressBar(max_value=vertex_buffer_size*2+len(index_buffer)+vertex_count*24)
progress_bar_count=0

if error_flag == 0:
#Create new UABE Asset Dump
    UABE_asset_filename=str(sys.argv[1])+"_UABE.txt"
    print("Writing "+ UABE_asset_filename)
    UABE_asset = open(UABE_asset_filename, "w")
    progress_bar_count+=1
    bar.update(progress_bar_count)

    #Follwoing standard file structure, input out data when needed.
    UABE_asset.write("0 Mesh Base\n")
    UABE_asset.write(" 1 string m_Name = \""+str(asset_name)+"\"\n")
    UABE_asset.write(" 0 vector m_SubMeshes\n")
    UABE_asset.write("  1 Array Array (1 items)\n")
    UABE_asset.write("   0 int size = 1\n")
    UABE_asset.write("   [0]\n")
    UABE_asset.write("    0 SubMesh data\n")
    UABE_asset.write("     0 unsigned int firstByte = 0\n")
    UABE_asset.write("     0 unsigned int indexCount = "+str(index_count)+"\n")
    UABE_asset.write("     0 int topology = 0\n")
    UABE_asset.write("     0 unsigned int baseVertex = 0\n")
    UABE_asset.write("     0 unsigned int firstVertex = 0\n")
    UABE_asset.write("     0 unsigned int vertexCount = "+str(vertex_count)+"\n")
    UABE_asset.write("     0 AABB localAABB\n")
    UABE_asset.write("      0 Vector3f m_Center\n")
    UABE_asset.write("       0 float x = "+str(center_x)+"\n")
    UABE_asset.write("       0 float y = "+str(center_y)+"\n")
    UABE_asset.write("       0 float z = "+str(center_z)+"\n")
    UABE_asset.write("      0 Vector3f m_Extent\n")
    UABE_asset.write("       0 float x = "+str(extent_x)+"\n")
    UABE_asset.write("       0 float y = "+str(extent_y)+"\n")
    UABE_asset.write("       0 float z = "+str(extent_z)+"\n")



    #Binding Pose Data
    UABE_asset.write(" 0 BlendShapeData m_Shapes\n")
    UABE_asset.write("  0 vector vertices\n")
    UABE_asset.write("   1 Array Array (0 items)\n")
    UABE_asset.write("    0 int size = 0\n")
    UABE_asset.write("  0 vector shapes\n")
    UABE_asset.write("   1 Array Array (0 items)\n")
    UABE_asset.write("    0 int size = 0\n")
    UABE_asset.write("  0 vector channels\n")
    UABE_asset.write("   1 Array Array (0 items)\n")
    UABE_asset.write("    0 int size = 0\n")
    UABE_asset.write("  0 vector fullWeights\n")
    UABE_asset.write("   1 Array Array (0 items)\n")
    UABE_asset.write("    0 int size = 0\n")
    UABE_asset.write(" 0 vector m_BindPose\n")
    UABE_asset.write("  1 Array Array ("+str(int(bind_pose_buffer_size/bind_pose_matrix_size))+" items)\n")
    UABE_asset.write("   0 int size = "+str(int(bind_pose_buffer_size/bind_pose_matrix_size))+"\n")

    
    for index_item in range(int(bind_pose_buffer_size/bind_pose_matrix_size)):
        UABE_asset.write("   ["+str(index_item)+"]\n")
        UABE_asset.write("    0 Matrix4x4f data\n")
        UABE_asset.write("     0 float e00 = "+str(bind_pose_data[int(index_item*bind_pose_matrix_size)])+"\n")
        UABE_asset.write("     0 float e01 = "+str(bind_pose_data[int(index_item*bind_pose_matrix_size)+1])+"\n")
        UABE_asset.write("     0 float e02 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+2])+"\n")
        UABE_asset.write("     0 float e03 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+3])+"\n")

        UABE_asset.write("     0 float e10 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+4])+"\n")
        UABE_asset.write("     0 float e11 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+5])+"\n")
        UABE_asset.write("     0 float e12 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+6])+"\n")
        UABE_asset.write("     0 float e13 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+7])+"\n")

        UABE_asset.write("     0 float e20 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+8])+"\n")
        UABE_asset.write("     0 float e21 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+9])+"\n")
        UABE_asset.write("     0 float e22 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+10])+"\n")
        UABE_asset.write("     0 float e23 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+11])+"\n")

        UABE_asset.write("     0 float e30 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+12])+"\n")
        UABE_asset.write("     0 float e31 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+13])+"\n")
        UABE_asset.write("     0 float e32 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+14])+"\n")
        UABE_asset.write("     0 float e33 = "+str(bind_pose_data[index_item*bind_pose_matrix_size+15])+"\n")




    #Bone Name hashes
    UABE_asset.write(" 0 vector m_BoneNameHashes\n")
    UABE_asset.write("  1 Array Array ("+str(int(bind_pose_buffer_size/bind_pose_matrix_size))+" items)\n")
    UABE_asset.write("   0 int size = "+str(int(bind_pose_buffer_size/bind_pose_matrix_size))+"\n")

    for index_item in range(int(bind_pose_buffer_size/bind_pose_matrix_size)):
        UABE_asset.write("   ["+str(index_item)+"]\n")

        #Convert to big endian
        temp_string=str(wrap(bone_name_hash_array.strip(),8)[index_item])
        temp_string_H=temp_string[:4]
        temp_string_L=temp_string[-4:]
        big_endian_string=temp_string_L[-2:]+temp_string_L[:2]+temp_string_H[-2:]+temp_string_H[:2]
        #long_value = int(temp_string[:2],32)*65535 + int(temp_string[-2:],32)

        UABE_asset.write("    0 unsigned int data = "+str(int(big_endian_string,16))+"\n")







    UABE_asset.write(" 0 unsigned int m_RootBoneNameHash = "+str(root_bone_name_hash)+"\n")




    UABE_asset.write(" 0 UInt8 m_MeshCompression = 0\n")
    UABE_asset.write(" 0 bool m_IsReadable = true\n")
    UABE_asset.write(" 0 bool m_KeepVertices = false\n")
    UABE_asset.write(" 1 bool m_KeepIndices = false\n")
    UABE_asset.write(" 0 int m_IndexFormat = 0\n")
    UABE_asset.write(" 0 vector m_IndexBuffer\n")
    UABE_asset.write("  1 Array Array ("+str(index_count*2)+" items)\n")
    UABE_asset.write("   0 int size = "+str(index_count*2)+"\n")

    for UABE_index in range(index_count*2):
        #print("INDEX: " + str(UABE_index))
        UABE_asset.write("   ["+str(UABE_index )+"]\n    0 UInt8 data = ")
        UABE_value=str(index_buffer[UABE_index*2])+str(index_buffer[UABE_index*2+1])
        UABE_asset.write(str(int(UABE_value,16)))
        UABE_asset.write("\n")
        progress_bar_count+=1
        bar.update(progress_bar_count)



    #Write Vertex Data
    UABE_asset.write(" 1 VertexData m_VertexData\n")
    UABE_asset.write("  0 unsigned int m_VertexCount = "+str(vertex_count)+"\n")
    UABE_asset.write("  0 vector m_Channels\n")
    UABE_asset.write("   1 Array Array ("+str(m_channel_len)+" items)\n")
    UABE_asset.write("    0 int size = "+str(m_channel_len)+"\n")
    #Write Channel Infor
    for index_item in range(int(len(m_channel_array)/4)):
        UABE_asset.write("    ["+str(index_item)+"]\n")
        UABE_asset.write("     0 ChannelInfo data\n")
        UABE_asset.write("      0 UInt8 stream = "+str(m_channel_array[index_item*4])+"\n")
        UABE_asset.write("      0 UInt8 offset = "+str(m_channel_array[index_item*4+1])+"\n")
        UABE_asset.write("      0 UInt8 format = "+str(m_channel_array[index_item*4+2])+"\n")
        UABE_asset.write("      0 UInt8 dimension = "+str(m_channel_array[index_item*4+3])+"\n")



    
    #Write Vertex Data Buffer
    UABE_asset.write("  1 TypelessData m_DataSize ("+str(vertex_buffer_size)+" items)\n")
    UABE_asset.write("   0 int size = "+str(vertex_buffer_size)+"\n")

    for UABE_index in range(vertex_buffer_size):
        #print("INDEX: " + str(UABE_index))
        UABE_asset.write("   ["+str(UABE_index )+"]\n    0 UInt8 data = ")
        UABE_value=str(vertex_buffer[UABE_index*2])+str(vertex_buffer[UABE_index*2+1])
        UABE_asset.write(str(int(UABE_value,16)))
        UABE_asset.write("\n")
        progress_bar_count+=1
        bar.update(progress_bar_count)



    #Copy Paste File Structure. Wont change until it causes problems
    UABE_asset.write(" 0 CompressedMesh m_CompressedMesh\n")
    UABE_asset.write("  0 PackedBitVector m_Vertices\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 float m_Range = 0\n")
    UABE_asset.write("   0 float m_Start = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_UV\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 float m_Range = 0\n")
    UABE_asset.write("   0 float m_Start = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_Normals\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 float m_Range = 0\n")
    UABE_asset.write("   0 float m_Start = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_Tangents\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 float m_Range = 0\n")
    UABE_asset.write("   0 float m_Start = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_Weights\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_NormalSigns\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_TangentSigns\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_FloatColors\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 float m_Range = 0\n")
    UABE_asset.write("   0 float m_Start = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_BoneIndices\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 PackedBitVector m_Triangles\n")
    UABE_asset.write("   0 unsigned int m_NumItems = 0\n")
    UABE_asset.write("   0 vector m_Data\n")
    UABE_asset.write("    1 Array Array (0 items)\n")
    UABE_asset.write("     0 int size = 0\n")
    UABE_asset.write("   1 UInt8 m_BitSize = 0\n")
    UABE_asset.write("  0 unsigned int m_UVInfo = 0\n")
    UABE_asset.write(" 0 AABB m_LocalAABB\n")
    UABE_asset.write("  0 Vector3f m_Center\n")
    UABE_asset.write("   0 float x = "+str(center_x)+"\n")
    UABE_asset.write("   0 float y = "+str(center_y)+"\n")
    UABE_asset.write("   0 float z = "+str(center_z)+"\n")
    UABE_asset.write("  0 Vector3f m_Extent\n")
    UABE_asset.write("   0 float x = "+str(extent_x)+"\n")
    UABE_asset.write("   0 float y = "+str(extent_y)+"\n")
    UABE_asset.write("   0 float z = "+str(extent_z)+"\n")
    UABE_asset.write(" 0 int m_MeshUsageFlags = "+str(mesh_usage_flag)+"\n")
    UABE_asset.write(" 0 vector m_BakedConvexCollisionMesh\n")
    UABE_asset.write("  1 Array Array (0 items)\n")
    UABE_asset.write("   0 int size = 0\n")
    UABE_asset.write(" 0 vector m_BakedTriangleCollisionMesh\n")
    UABE_asset.write("  1 Array Array (0 items)\n")
    UABE_asset.write("   0 int size = 0\n")
    UABE_asset.write(" 0 float m_MeshMetrics[0] = 1\n")
    UABE_asset.write(" 1 float m_MeshMetrics[1] = 1\n")
    UABE_asset.write(" 0 StreamingInfo m_StreamData\n")
    UABE_asset.write("  0 unsigned int offset = 0\n")
    UABE_asset.write("  0 unsigned int size = 0\n")
    UABE_asset.write("  1 string path = \"\"\n")








































else:
    print(Fore.RED + "SCript Terminated. One or more Errors has prevented the asset from compiling" +Style.RESET_ALL)






#close all the files

asset_file.close()
UABE_asset.close()

















                

