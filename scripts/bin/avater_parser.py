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

print("GooseTool's Avatar Parser")
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
# AVATAR CLASS
########################################################################################################################################

class parse_avater():
        
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
    
    avatar_bone_name_array=""
    avatar_bone_name_array_count=0

    avatar_root_motion_bone_index=0


    avatar_tos_flag=0


    avatar_bone_name_hash_array
    avatar_skeleton_pose_array
    avatar_default_pose_array
    avatar_human_root_bone_array
    avatar_human_bone_mass_array
    avatar_root_motion_bone_array

    avatar_skeleton_pose_flag=0
    avatar_default_pose_flag=0
    avatar_root_bone_flag=0
    avatar_tos_flag=0

    avatar_skeleton_pose_index=0
    avatar_default_pose_index=0
    avatar_bone_name_hash_index=0


    def get_avatar_bone_name(self,bone_number):

        if bone_number <= len(self.avatar_bone_name_array.split()):
            chain_length=len(self.avatar_bone_name_array.split()[bone_number].split("/"))
            return str(self.avatar_bone_name_array.split()[bone_number].split("/")[chain_length-1])

        else:

            print(Fore.RED + "ERROR - Bone Index "  + str(bone_number) + "out of range!" + Style.RESET_ALL)
            return "<error>"

    def get_avatar_bone_id(self,bone_number):

        if bone_number <= len(self.avatar_bone_name_array.split()):
            chain_length=len(self.avatar_bone_name_array.split()[bone_number].split("/"))
            return "Armature_" +str(self.avatar_bone_name_array.split()[bone_number].split("/")[chain_length-1])

        else:

            print(Fore.RED + "ERROR - Bone Index "  + str(bone_number) + "out of range!" + Style.RESET_ALL)
            return "<error>"




    def __init__(self, filename):
        self.filename = filename

        avatar_file = open(filename, "r")

        AVATAR_LINE = avatar_file.readlines()


        print("Preprocessing File...")
        for line in AVATAR_LINE: 

            if "m_name:" in line:
                self.avatar_name=line.split(":")[1].strip()

            elif "m_AvatarSize:" in line:  
                self.avatar_size=int(line.split(":")[1].strip())

            elif "m_ID:" in line:
                self.avatar_skelton_ID=line.split(":")[1].strip()

            elif "m_AvatarSkeletonPose:" in line:
                self.avatar_skeleton_pose_flag=1
                self.avatar_default_pose_flag=0
            
            elif "- t:" in line and avatar_skeleton_pose_flag == 1:
                self.avatar_skeleton_pose_count+=1
            
            elif "m_DefaultPose:" in line:
                self.avatar_default_pose_flag=1
                self.avatar_skeleton_pose_flag=0
            
            elif "- t:" in line and avatar_default_pose_flag == 1:
                self.avatar_default_pose_count+=1     

            elif "m_SkeletonNameIDArray:" in line:
                self.avatar_skelton_name_ID_array=line.split(":")[1].strip()

            elif "m_LeftHand:" in line:
                self.avatar_left_hand_bone_index_flag=1
                self.avatar_right_hand_bone_index_flag=0 
                
            elif "m_RightHand:" in line:
                self.avatar_left_hand_bone_index_flag=0
                self.avatar_right_hand_bone_index_flag=1
                

            elif "m_HandBoneIndex:" in line and self.avatar_left_hand_bone_index_flag == 1:
                self.avatar_left_hand_bone_inde=line.split(":")[1].strip()

            elif "m_HandBoneIndex:" in line and self.avatar_right_hand_bone_index_flag == 1:
                self.avatar_right_hand_bone_index=line.split(":")[1].strip()

            elif "m_HumanBoneIndex:" in line:
                self.avatar_human_hand_bone_index=line.split(":")[1].strip()

            elif "m_HumanBoneMass:" in line:
                self.avatar_human_bone_mass_array_flag=1

            elif "-" in line and self.avatar_human_bone_mass_array_flag==1:
                self.avatar_human_bone_mass_array_count+=1

            elif "m_ColliderIndex:" in line:
                self.avatar_human_bone_mass_array_flag=0


            elif "m_TOS:" in line:
                self.avatar_tos_flag=1

            elif ":" in line and self.avatar_tos_flag == 1:
                if line.split(":")[1].strip() == "":
                    self.avatar_bone_name_array+= "unnamed_bone "
                else:
                    self.avatar_bone_name_array+= line.split(":")[1].strip() + " "
                self.avatar_bone_name_array_count+=1







        ########################################################################################################################################
        #  Extract Data
        ########################################################################################################################################

        # Array Data Allocation
        self.avatar_bone_name_hash_array=np.zeros(avatar_bone_name_array_count, dtype=np.int64)
        self.avatar_skeleton_pose_array=np.zeros((avatar_skeleton_pose_count*10), dtype=float)
        self.avatar_default_pose_array=np.zeros((avatar_default_pose_count*10), dtype=float)
        self.avatar_human_root_bone_array=np.zeros(10, dtype=float)
        self.avatar_human_bone_mass_array=np.zeros(avatar_human_bone_mass_array_count, dtype=float)
        self.avatar_root_motion_bone_array=np.zeros(10, dtype=float)

        self.avatar_skeleton_pose_flag=0
        self.avatar_default_pose_flag=0
        self.avatar_root_bone_flag=0
        self.avatar_tos_flag=0

        self.avatar_skeleton_pose_index=0
        self.avatar_default_pose_index=0
        self.avatar_bone_name_hash_index=0

        avatar_file.seek(0)
        AVATAR_LINE = avatar_file.readlines()

        print("Reading Avatar File...")
        for line in AVATAR_LINE: 
    
            if "m_AvatarSkeletonPose:" in line:
                self.avatar_skeleton_pose_flag=1
                self.avatar_default_pose_flag=0
                self.avatar_root_bone_flag=0
            elif "t:" in line and self.avatar_skeleton_pose_flag == 1:
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+1] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and self.avatar_skeleton_pose_flag == 1:
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+3] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+4] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+5] = float(line.split("z:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and self.avatar_skeleton_pose_flag == 1:
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+7] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+8] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_skeleton_pose_array[self.avatar_skeleton_pose_index*10+9] = float(line.split("z:")[1].split("}")[0].strip())
                self.avatar_skeleton_pose_index+=1


            elif "m_DefaultPose:" in line:
                self.avatar_default_pose_flag=1
                self.avatar_skeleton_pose_flag=0
                self.avatar_root_bone_flag=0
            elif "t:" in line and self.avatar_default_pose_flag == 1:
                self.avatar_default_pose_array[self.avatar_default_pose_index*10] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+1] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and self.avatar_default_pose_flag == 1:
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+3] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+4] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+5] = float(line.split("z:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and self.avatar_default_pose_flag == 1:
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+7] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+8] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_default_pose_array[self.avatar_default_pose_index*10+9] = float(line.split("z:")[1].split("}")[0].strip())
                self.avatar_default_pose_index+=1


            elif "m_RootX:" in line:
                self.avatar_default_pose_flag=0
                self.avatar_skeleton_pose_flag=0
                self.avatar_root_bone_flag=1
            elif "t:" in line and self.avatar_root_bone_flag == 1:
                self.avatar_human_root_bone_array[0] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[1] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[2] = float(line.split("z:")[1].split("}")[0].strip())


            elif "q:" in line and self.avatar_root_bone_flag == 1:
                self.avatar_human_root_bone_array[3] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[4] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[5] = float(line.split("z:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[6] = float(line.split("w:")[1].split("}")[0].strip())

            elif "s:" in line and self.avatar_root_bone_flag == 1:
                self.avatar_human_root_bone_array[7] = float(line.split("{x:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[8] = float(line.split("y:")[1].split(",")[0].strip())
                self.avatar_human_root_bone_array[9] = float(line.split("z:")[1].split("}")[0].strip())
                self.avatar_root_bone_flag=0       





            elif "m_TOS:" in line:
                self.avatar_tos_flag=1

            elif ":" in line and self.avatar_tos_flag == 1:
                self.avatar_bone_name_hash_array[self.avatar_bone_name_hash_index] = np.int64(line.split(":")[0].strip())
                self.avatar_bone_name_hash_index+=1



















