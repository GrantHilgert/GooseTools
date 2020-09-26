@echo off
REM GOOSETOOLS TEST SCRIPT


echo Extracting %1

copy %1 "build\"
python ..\scripts\get_asset_name.py %1 > Output
SET /p asset_name=<Output
echo %asset_name%
PAUSE
DEL Output



echo ###############################################################################################
echo EXTRACT ASSSET
echo ###############################################################################################
python "..\scripts\asset_to_obj.py"  "build\%asset_name%.asset"

echo ###############################################################################################
echo PREPROCESSED ASSET
echo ###############################################################################################
python "..\scripts\obj_preprocess.py" "build\%asset_name%.obj"


echo ###############################################################################################
echo RECOMPILE ASSET
echo ###############################################################################################

python "..\scripts\obj_to_asset.py" "build\%asset_name%.asset" "build\%asset_name%_processed.obj"


echo ###############################################################################################
echo EXTRACT ASSSET AGAIN
echo ###############################################################################################
python "..\scripts\asset_to_obj.py"  "build\%asset_name%_processed_GooseTools_Compiled.asset"