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

print("GooseTool's Asset Parser")
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









########################################################################################################################################
# PREPROCESS ASSET 
########################################################################################################################################

class asset_parser:
    asset_name="N/A"
    asset_type="N/A"
    
    index_count=0
    index_buffer=""
    
    vertex_count=0
    self.vertex_buffer=""
    self.vertex_buffer_size=0
    #self.vertex_buffer_block_size='NA'  


    bind_pose_buffer=""
    bind_pose_count=0


    bone_name_hash=""
    root_bone_name_hash=""


    def __init__(self, filename):
        self.filename = filename

        material_count_index=0
        material_count=0
        #open asset file from command line
        asset_file = open(filename, "r")
        YAML_LINE = asset_file.readlines()


        bind_pose_flag=0
        bind_pose_complete=0

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
                    self.asset_type="simple"           
                elif "m_BindPose:" in line:
                    bind_pose_flag=1

            if "m_BoneNameHashes:" in line:
                if len(line.strip().split(":")) > 1:
                    self.bone_name_hash=str(line.strip().split(":")[1]).strip()
                    bind_pose_complete=1
                    print("Bone Name Hashes: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
                elif bind_pose_flag == 1 and len(line.split(":")) == 1:
                    print("Pose Binding Data"+ Fore.RED + "[FAIL]" +Style.RESET_ALL)     

            if "m_RootBoneNameHash:" in line:
                if line.strip().split(":")[1].strip() != str(0):
                    self.root_bone_name_hash=str(line.strip().split(":")[1]).strip()
                    print("Root Bone Name Hashes: "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)

                else:
                    print("Root Bone Name Hashes: "+ Fore.YELLOW + "[NO DATA]" +Style.RESET_ALL)  

            
            #Name of Asset File
            if "m_Name:" in line:
                self.asset_name=str(line.split(":", maxsplit=1)[1].strip())
                print("Asset Name "+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
            
            #Number of Vertexs
            if "m_VertexCount:" in line:
                self.vertex_count=int(line.split(":", maxsplit=1)[1].strip())
                print("Vertex Count"+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
            

            #index Buffer size
            if "indexCount" in line:
                self.index_count=int(line.split(":", maxsplit=1)[1].strip())
                print("Index Count"+ Fore.GREEN + "[OK]" +Style.RESET_ALL)
            #Copy Index Buffer
            if "m_IndexBuffer:" in line:
                self.index_buffer+=str(line.split(":", maxsplit=1)[1].strip())
            
                #Vertex Buffer Size
            if "m_DataSize:" in line:
                self.self.vertex_buffer_size=int(line.split(":", maxsplit=1)[1].strip())
            
            #Copy Vertex Buffer 
            if "_typelessdata:" in line:
                self.self.vertex_buffer=str(line.split(":", maxsplit=1)[1].strip())
                count+=1    #Copy Vertex Buffer 
            
            #Copy Bind Pose Data
            if bind_pose_flag == 1 and bind_pose_complete != 1:   
                if len(str(str(line).split("e")[1].split(":")[0].strip())) > 0:
                    if str(str(line).split("e")[1].split(":")[0].strip())[0].isdigit():
                        matrix_id=int(str(matrix_col)+str(matrix_row))
                        test_value=int(str(line).split("e")[1].split(":")[0].strip())
                        if int(matrix_id) == int(test_value):
                            self.bind_pose_buffer+=line.split(":")[1].strip()+" "
                            matrix_row+=1
                        if matrix_row == 4:
                            matrix_row = 0
                            matrix_col+=1
                        if matrix_col == 4:
                            matrix_row=0
                            matrix_col=0
                            self.bind_pose_count+=1


                #print("DEBUG - BIND POSE MATRIX")
                #bind_pose_buffer=str(line.split(":", maxsplit=1)[1].strip())
        asset_file.close()
        asset_type=self.get_asset_type()

        preprocess_complete_flag=1





    def print_data():
        print("Asset Name: "+Fore.GREEN + str(self.asset_name)+Style.RESET_ALL)
        print("Indexs: "+Fore.GREEN +str(self.index_count)+Style.RESET_ALL)
        print("Vertexs: "+Fore.GREEN +str(self.vertex_count)+Style.RESET_ALL)
        print("Vertex Buffer Size: "+ Fore.GREEN +str(self.self.vertex_buffer_size)+Style.RESET_ALL)
        print("Bind Pose Count: "+ Fore.GREEN +str(self.bind_pos_matrix_count)+Style.RESET_ALL)







    #Returns whether the asset is simple(i.g. Pumpkin) or has bone(i.g. Goose)
    def get_asset_type():
     
        # Complex Structure (Type-B)
        complex_self.vertex_buffer_size=40*self.vertex_count
        complex_color_buffer_size=12*self.vertex_count
        complex_bone_buffer_size=32*self.vertex_count
        complex_bone_lable_size=12
        complex_buffer_combined_size=complex_self.vertex_buffer_size+complex_color_buffer_size+complex_bone_buffer_size 

        if (complex_buffer_combined_size == self.self.vertex_buffer_size) and (self.bind_pose_count > 0): 

            print("Model Structure: "+ Fore.YELLOW + "[NPC]" +Style.RESET_ALL)        
            return "npc"
        

        elif (complex_buffer_combined_size + complex_bone_lable_size == size_of_self.vertex_buffer) and (self.bone_count > 0): 

            print("Model Structure: "+ Fore.YELLOW + "[GOOSE]" +Style.RESET_ALL)        
            return "goose"

        # Simple Structure (Type-A)
        elif (self.self.vertex_buffer_size/self.vertex_count).is_integer():
            print("Model Structure: "+ Fore.YELLOW + "[SIMPLE]" +Style.RESET_ALL)
            return "simple"

            #This buffer is something else and we cant decode it, throw an error.
        else:
            print("Model Structure: "+ Fore.RED + "[UNKNOWN]" +Style.RESET_ALL) 
            return "fail"





    #Creates a blender friendly material name
    def get_material_name(raw_material_data):

        return "ugg_material.00"+ str(self.material_count_index)



    global material_vertex_count_array
    material_vertex_count_array=""


    current_material_count=0
    def get_material_list(num_of_vertex, size_of_self.vertex_buffer,bone_count):
        asset_type=get_asset_type(num_of_vertex, size_of_self.vertex_buffer,bone_count)
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

    def get_complex_self.vertex_buffer_block_size():
        return 40
    def get_complex_self.vertex_buffer_size():
        return self.vertex_count*self.get_complex_self.vertex_buffer_block_size()

    def get_complex_color_buffer_block_size():
        return 12
    def get_complex_color_buffer_size():
        return self.vertex_count*self.get_complex_color_buffer_block_size()

    def get_complex_bone_buffer_block_size():
        return 32
    def get_complex_bone_buffer_size():
        return self.vertex_count*self.get_complex_bone_buffer_block_size()
      

    # returns #num1 #num2 #num3
    # face_number is zero indexed
    def get_obj_face(face_number):

        f=face_number
        vertex_1=self.index_buffer[f*12+10] + self.index_buffer[f*12+11] + self.index_buffer[f*12+8] + self.index_buffer[f*12+9]
        vertex_2=self.index_buffer[f*12+6] + self.index_buffer[f*12+7] + self.index_buffer[f*12+4] + self.index_buffer[f*12+5]
        vertex_3=self.index_buffer[f*12+2] + self.index_buffer[f*12+3] + self.index_buffer[f*12+0] + self.index_buffer[f*12+1]

        return str(int(vertex_1,16)) + " " + str(int(vertex_2,16)) + " " + str(int(vertex_3,16))



    def get_obj_vertex(vertex_number):
        v=vertex_number*get_complex_self.vertex_buffer_block_size()*2   
        word_vertex_x=self.self.vertex_buffer[v]   +self.self.vertex_buffer[v+1] +self.self.vertex_buffer[v+2] +self.self.vertex_buffer[v+3] +self.self.vertex_buffer[v+4] +self.self.vertex_buffer[v+5] +self.self.vertex_buffer[v+6] +self.self.vertex_buffer[v+7]
        word_vertex_y=self.self.vertex_buffer[v+8] +self.self.vertex_buffer[v+9] +self.self.vertex_buffer[v+10]+self.self.vertex_buffer[v+11]+self.self.vertex_buffer[v+12]+self.self.vertex_buffer[v+13]+self.self.vertex_buffer[v+14]+self.self.vertex_buffer[v+15]
        word_vertex_z=self.self.vertex_buffer[v+16]+self.self.vertex_buffer[v+17]+self.self.vertex_buffer[v+18]+self.self.vertex_buffer[v+19]+self.self.vertex_buffer[v+20]+self.self.vertex_buffer[v+21]+self.self.vertex_buffer[v+22]+self.self.vertex_buffer[v+23]

        float_vertex_x=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_x))).strip('(),')),7)
        float_vertex_y=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_y))).strip('(),')),7)
        float_vertex_z=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_z))).strip('(),')),7)

        return str(float_vertex_x) + " " + str(float_vertex_y) + " " + str(float_vertex_z)



    def get_obj_normal(vertex_number):
        v=vertex_number*get_complex_self.vertex_buffer_block_size()*2   
        word_normal_x=self.self.vertex_buffer[v+24]+self.self.vertex_buffer[v+25]+self.self.vertex_buffer[v+26]+self.self.vertex_buffer[v+27]+self.self.vertex_buffer[v+28]+self.self.vertex_buffer[v+29]+self.self.vertex_buffer[v+30]+self.self.vertex_buffer[v+31]
        word_normal_y=self.self.vertex_buffer[v+32]+self.self.vertex_buffer[v+33]+self.self.vertex_buffer[v+34]+self.self.vertex_buffer[v+35]+self.self.vertex_buffer[v+36]+self.self.vertex_buffer[v+37]+self.self.vertex_buffer[v+38]+self.self.vertex_buffer[v+39]
        word_normal_z=self.self.vertex_buffer[v+40]+self.self.vertex_buffer[v+41]+self.self.vertex_buffer[v+42]+self.self.vertex_buffer[v+43]+self.self.vertex_buffer[v+44]+self.self.vertex_buffer[v+45]+self.self.vertex_buffer[v+46]+self.self.vertex_buffer[v+47]

        float_normal_x=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_x))).strip('(),')),7)
        float_normal_y=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_y))).strip('(),')),7)
        float_normal_z=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_z))).strip('(),')),7)

        return str(float_normal_x) + " " + str(float_normal_y) + " " + str(float_normal_z)


    def get_obj_uv(vertex_number):
        v=get_complex_self.vertex_buffer_size(self.vertex_buffer_size)+vertex_number*get_complex_color_buffer_block_size()*2 
        word_s=self.vertex_buffer[v]+self.vertex_buffer[v+1]+self.vertex_buffer[v+2]+self.vertex_buffer[v+3]+self.vertex_buffer[v+4]+self.vertex_buffer[v+5]+self.vertex_buffer[v+6]+self.vertex_buffer[v+7]
        word_t=self.vertex_buffer[v+8]+self.vertex_buffer[v+9]+self.vertex_buffer[v+10]+self.vertex_buffer[v+11]+self.vertex_buffer[v+12]+self.vertex_buffer[v+13]+self.vertex_buffer[v+14]+self.vertex_buffer[v+15]

        float_s=round(float(str(struct.unpack('f', bytes.fromhex(word_s))).strip('(),')),7)
        float_t=round(float(str(struct.unpack('f', bytes.fromhex(word_t))).strip('(),')),7)

        return str(float_s) + " " + str(float_t)

    def get_obj_color(vertex_number):
        v=get_complex_self.vertex_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
        
        byte_red=self.vertex_buffer[v+16]+self.vertex_buffer[v+17]
        byte_green=self.vertex_buffer[v+18]+self.vertex_buffer[v+19]
        byte_blue=self.vertex_buffer[v+20]+self.vertex_buffer[v+21]


        #error check
        color_terminator=self.vertex_buffer[v+22]+self.vertex_buffer[v+23]

        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(vertex_number) + " == "+ str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)+" "+ str(color_terminator)+" color buffer Corrupt" +Style.RESET_ALL)

        #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
        normalized_red=(int(byte_red,16))/255
        normalized_green=(int(byte_green,16))/255
        normalized_blue=(int(byte_blue,16))/255

        return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)



    def get_obj_color_hex(vertex_number):
        v=get_complex_self.vertex_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
        #print("DEBUG - V: " + str(v))
        byte_red=self.vertex_buffer[v+16]+self.vertex_buffer[v+17]
        byte_green=self.vertex_buffer[v+18]+self.vertex_buffer[v+19]
        byte_blue=self.vertex_buffer[v+20]+self.vertex_buffer[v+21]
        #error check


        color_terminator=self.vertex_buffer[v+22]+self.vertex_buffer[v+23]

        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(vertex_number) + " == "+ str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)+" "+ str(color_terminator)+" color buffer Corrupt" +Style.RESET_ALL)

        return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)





    def get_obj_bone_root():
        v=get_complex_self.vertex_buffer_size(self.self.vertex_buffer_size)*2+get_complex_color_buffer_size(self.self.vertex_buffer_size)*2
        temp_string=""
        for index in range(24):
            temp_string+=self.vertex_buffer[v+index]
        return str(temp_string)

    def get_obj_bone_buffer(vertex_number):
        v=(get_complex_self.vertex_buffer_size(self.vertex_buffer_size)*2+get_complex_color_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_bone_buffer_block_size()*2)+24
        temp_string=""
        for index in range(get_complex_bone_buffer_block_size()*2):
            temp_string+=self.vertex_buffer[v+index]
        return str(temp_string)





    def get_obj_vertex_weight(weight_position,vertex_number):
        bone_weight_string=""
        bone_num_string=""
        if ((asset_type == "npc") or (asset_type == "goose")) and weight_position < 4:

            if self.asset_type == "npc":
                v=(get_complex_self.vertex_buffer_size(self.vertex_count)*2+get_complex_color_buffer_size(self.vertex_count)*2)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position   
            elif self.asset_type == "goose":
                unknown_goose_data=24
                v=(get_complex_self.vertex_buffer_size(self.vertex_count)*2+get_complex_color_buffer_size(self.vertex_count)*2+unknown_goose_data)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position

            for bone_char_index in range(8):
                bone_weight_string+=self.vertex_buffer[v+bone_char_index]

            for bone_num_char_index in range(8):
                bone_num_string+=self.vertex_buffer[v+bone_num_char_index+32]

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

    def get_obj_vertex_weight_count(vertex_number):
        if ((self.asset_type == "npc") or (self.asset_type == "goose")):
            for weight_position in range(4):
                bone_weight_string=""
                bone_num_string=""
                if self.asset_type == "npc":
                    v=(get_complex_self.vertex_buffer_size(self.vertex_count)*2+get_complex_color_buffer_size(self.vertex_count)*2)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position   
                elif self.asset_type == "goose":
                    unknown_goose_data=24
                    v=(get_complex_self.vertex_buffer_size(self.vertex_count)*2+get_complex_color_buffer_size(self.vertex_count)*2+unknown_goose_data)+get_complex_bone_buffer_block_size()*vertex_number*2+8*weight_position

                for bone_char_index in range(8):
                    bone_weight_string+=self.vertex_buffer[v+bone_char_index]

                for bone_num_char_index in range(8):
                    bone_num_string+=self.vertex_buffer[v+bone_num_char_index+32]

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




    def get_bone_hash(bone_number):
        temp_string=""
        temp_index=bone_number*int(len(self.bone_name_hash)/self.bind_pose_count)
        for bone_hash_string_index in range(int(len(self.bone_name_hash)/self.bind_pose_count)):
            temp_string+=self.bone_name_hash[temp_index+bone_hash_string_index]
        
        return str(temp_string)


    def get_bone_name_buffer():
        temp_bone_name_buffer="Body_Armature_Bone "
        for bone_index in range(self.bind_pose_count):
            temp_bone_name_buffer+="Body_Armature_Bone_"+str("{0:0=3d}".format(bone_index)) + " "
        return temp_bone_name_buffer


    def get_bone_name(bone_number):
        if bone_number == 1:
            temp_bone_name="Body_Armature_Bone "
        elif bone_number <= self.bind_pose_count:
            temp_bone_name+="Body_Armature_Bone_"+str("{0:0=2d}".format(bone_number)) + " "
        return temp_bone_name



    #######################
    # NPC ASSETS
    #######################


    def get_obj_npc_color_hex(vertex_number,):
        v=get_complex_vertex_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
        #print("DEBUG - V: " + str(v))
        #byte_red=self.vertex_buffer[v+16]+self.vertex_buffer[v+17]
        #byte_green=self.vertex_buffer[v+18]+self.vertex_buffer[v+19]
        #byte_blue=self.vertex_buffer[v+20]+self.vertex_buffer[v+21]
        #error check

        byte_red=self.vertex_buffer[v]+self.vertex_buffer[v+1]
        byte_green=self.vertex_buffer[v+2]+self.vertex_buffer[v+3]
        byte_blue=self.vertex_buffer[v+4]+self.vertex_buffer[v+5]
        #error check
        #color_terminator=self.vertex_buffer[v+22]+self.vertex_buffer[v+23]
        color_terminator=self.vertex_buffer[v+6]+self.vertex_buffer[v+7]
        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

        return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)



    def get_obj_npc_color(vertex_number,):
        v=get_complex_vertex_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_color_buffer_block_size()*2
        
        #byte_red=self.vertex_buffer[v+16]+self.vertex_buffer[v+17]
        #byte_green=self.vertex_buffer[v+18]+self.vertex_buffer[v+19]
        #byte_blue=self.vertex_buffer[v+20]+self.vertex_buffer[v+21]

        byte_red=self.vertex_buffer[v]+self.vertex_buffer[v+1]
        byte_green=self.vertex_buffer[v+2]+self.vertex_buffer[v+3]
        byte_blue=self.vertex_buffer[v+4]+self.vertex_buffer[v+5]
        #error check
        #color_terminator=self.vertex_buffer[v+22]+self.vertex_buffer[v+23]
        color_terminator=self.vertex_buffer[v+6]+self.vertex_buffer[v+7]
        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(v) + "===>"+ str(vertex_number) + ": " + str(color_terminator) + " != \"ff\" color buffer Corrupt" +Style.RESET_ALL)

        #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
        normalized_red=(int(byte_red,16))/255
        normalized_green=(int(byte_green,16))/255
        normalized_blue=(int(byte_blue,16))/255

        return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)

    def get_obj_npc_bone_buffer(vertex_number):
        v=(get_complex_vertex_buffer_size(self.vertex_buffer_size)*2+get_complex_color_buffer_size(self.vertex_buffer_size)*2+vertex_number*get_complex_bone_buffer_block_size()*2)
        temp_string=""
        for index in range(self.get_complex_bone_buffer_block_size()*2):
            temp_string+=self.vertex_buffer[v+index]
        return str(temp_string)













    #######################
    # SIMPLE ASSETS
    #######################

    def get_simple_self.vertex_buffer_block_size():
        return 44


    def get_simple_obj_vertex(vertex_number):
        v=vertex_number*get_simple_vertex_buffer_block_size()*2   
        word_vertex_x=self.vertex_buffer[v]+self.vertex_buffer[v+1]+self.vertex_buffer[v+2]+self.vertex_buffer[v+3]+self.vertex_buffer[v+4]+self.vertex_buffer[v+5]+self.vertex_buffer[v+6]+self.vertex_buffer[v+7]
        word_vertex_y=self.vertex_buffer[v+8]+self.vertex_buffer[v+9]+self.vertex_buffer[v+10]+self.vertex_buffer[v+11]+self.vertex_buffer[v+12]+self.vertex_buffer[v+13]+self.vertex_buffer[v+14]+self.vertex_buffer[v+15]
        word_vertex_z=self.vertex_buffer[v+16]+self.vertex_buffer[v+17]+self.vertex_buffer[v+18]+self.vertex_buffer[v+19]+self.vertex_buffer[v+20]+self.vertex_buffer[v+21]+self.vertex_buffer[v+22]+self.vertex_buffer[v+23]

        float_vertex_x=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_x))).strip('(),')),7)
        float_vertex_y=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_y))).strip('(),')),7)
        float_vertex_z=round(float(str(struct.unpack('f', bytes.fromhex(word_vertex_z))).strip('(),')),7)

        return str(float_vertex_x) + " " + str(float_vertex_y) + " " + str(float_vertex_z)



    def get_simple_obj_normal(vertex_number):
        v=vertex_number*get_simple_vertex_buffer_block_size()*2   
        word_normal_x=self.vertex_buffer[v+24]+self.vertex_buffer[v+25]+self.vertex_buffer[v+26]+self.vertex_buffer[v+27]+self.vertex_buffer[v+28]+self.vertex_buffer[v+29]+self.vertex_buffer[v+30]+self.vertex_buffer[v+31]
        word_normal_y=self.vertex_buffer[v+32]+self.vertex_buffer[v+33]+self.vertex_buffer[v+34]+self.vertex_buffer[v+35]+self.vertex_buffer[v+36]+self.vertex_buffer[v+37]+self.vertex_buffer[v+38]+self.vertex_buffer[v+39]
        word_normal_z=self.vertex_buffer[v+40]+self.vertex_buffer[v+41]+self.vertex_buffer[v+42]+self.vertex_buffer[v+43]+self.vertex_buffer[v+44]+self.vertex_buffer[v+45]+self.vertex_buffer[v+46]+self.vertex_buffer[v+47]

        float_normal_x=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_x))).strip('(),')),7)
        float_normal_y=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_y))).strip('(),')),7)
        float_normal_z=round(float(str(struct.unpack('f', bytes.fromhex(word_normal_z))).strip('(),')),7)

        return str(float_normal_x) + " " + str(float_normal_y) + " " + str(float_normal_z)


    def get_simple_obj_uv(vertex_number):
        #This probably isnt correct.
        v=vertex_number*get_simple_vertex_buffer_block_size()*2 
        word_s=self.vertex_buffer[v+48]+self.vertex_buffer[v+49]+self.vertex_buffer[v+50]+self.vertex_buffer[v+51]+self.vertex_buffer[v+52]+self.vertex_buffer[v+53]+self.vertex_buffer[v+54]+self.vertex_buffer[v+55]
        word_t=self.vertex_buffer[v+56]+self.vertex_buffer[v+57]+self.vertex_buffer[v+58]+self.vertex_buffer[v+59]+self.vertex_buffer[v+60]+self.vertex_buffer[v+61]+self.vertex_buffer[v+62]+self.vertex_buffer[v+63]

        float_s=round(float(str(struct.unpack('f', bytes.fromhex(word_s))).strip('(),')),7)
        float_t=round(float(str(struct.unpack('f', bytes.fromhex(word_t))).strip('(),')),7)

        return str(float_s) + " " + str(float_t)


    def get_simple_obj_color(vertex_number):
        v=vertex_number*get_simple_vertex_buffer_block_size()*2
        
        byte_red=self.vertex_buffer[v+80]+self.vertex_buffer[v+81]
        byte_green=self.vertex_buffer[v+82]+self.vertex_buffer[v+83]
        byte_blue=self.vertex_buffer[v+84]+self.vertex_buffer[v+85]
        #error check
        color_terminator=self.vertex_buffer[v+86]+self.vertex_buffer[v+87]
        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(vertex_number) + "=="+ str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)+ str(color_terminator)+" color buffer Corrupt" +Style.RESET_ALL)

        #convert Hex to RGG (0 - 255), then normalize to (0 - 1)
        normalized_red=(int(byte_red,16))/255
        normalized_green=(int(byte_green,16))/255
        normalized_blue=(int(byte_blue,16))/255

        return str(normalized_red) + " " + str(normalized_green) + " " + str(normalized_blue)

    def get_simple_obj_color_hex(vertex_number):
        v=vertex_number*get_simple_vertex_buffer_block_size()*2
        
        byte_red=self.vertex_buffer[v+80]+self.vertex_buffer[v+81]
        byte_green=self.vertex_buffer[v+82]+self.vertex_buffer[v+83]
        byte_blue=self.vertex_buffer[v+84]+self.vertex_buffer[v+85]
        #error check
        color_terminator=self.vertex_buffer[v+86]+self.vertex_buffer[v+87]
        if color_terminator != "ff":
            print(Fore.RED + "Data Error: Vertex: " + str(vertex_number) + "=="+ str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)+ str(color_terminator)+" color buffer Corrupt" +Style.RESET_ALL)

        return str(byte_red) + " " + str(byte_green) + " " + str(byte_blue)









    def get_inverse_bind_transform(bone_number):
        
        bind_matrix=np.zeros(shape=(4,4), dtype=float)


        for row in range(4):
            for col in range(4):
                bind_matrix[row][col]=float(self.bind_pose_buffer.split()[bone_number*16+row+col])
        #Calculate inverse matrix
        
        #print(str(bind_matrix))
        inverse_matrix=np.linalg.inv(bind_matrix)

        return inverse_matrix
        



    def get_int_hash_from_index(bone_index):
        

        byte_4=self.bone_name_hash[bone_index*8+6]+self.bone_name_hash[bone_index*8+7]
        byte_3=self.bone_name_hash[bone_index*8+4]+self.bone_name_hash[bone_index*8+5]
        byte_2=self.bone_name_hash[bone_index*8+2]+self.bone_name_hash[bone_index*8+3]
        byte_1=self.bone_name_hash[bone_index*8]  +self.bone_name_hash[bone_index*8+1]
        temp_bone_hash=byte_4+byte_3+byte_2+byte_1
        #temp_bone_hash=byte_1+byte_2+byte_3+byte_4
        #print("TEMP STRING: " + str(temp_bone_hash ))
        #return str(struct.unpack('I', bytes.fromhex(temp_bone_hash))).strip('(),')
        return int(temp_bone_hash,16)
        #return int(byte_4,16)*255*255*255 + int(byte_3,16)*255*255 + int(byte_2,16)*255 + int(byte_1,16)


    #def get_bone_name_from_bind_pose_index(bone_index):

       # temp_hash=get_int_hash_from_index(bone_index)
        #for index in range(len(avatar_bone_name_hash_array)):
                #if avatar_bone_name_hash_array[index] == temp_hash:
                    #bone_name=get_avatar_bone_name(index)
                    #print("Matched Bone to Bind Pose: " + Fore.CYAN + "[" + str(bone_name) + "]" + Style.RESET_ALL)
                    #return avatar_bone_name_array.split()[index]               
                    #chain_length=len(avatar_bone_name_array.split()[index].split("/"))
                   # return str(avatar_bone_name_array.split()[index].split("/")[chain_length-1])

            

