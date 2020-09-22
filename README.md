# GooseTools
Mesh Replacment Modkit for Untitled Goose Game.
Written by: Grant Hilgert
Sepetember 2020




About: This is a series of scripts used to encode and decode Unity .asset files used in the Untitled Goose Game.
This may work on other games. Let me know if you try! Feel free share your results/issues with me.


V.0.01 -

	Full Mesh Replacement Supported.
	-Colors not currently supported. [They are next on the list]. 

Current Bugs and Limitations:
	-Still working on decoding color data. Currently all imported models will be blue. 
	-Future goal to include a material defintion file when compiling
	-You can change the color on line 470 of in obj_to_asset.py
	-The goose and people arnt supported. They use a differemt file structure and have bones. Working on adding support.
	-Preprocessing algorithm needs improvement to reduce loss.



Required Dependencies:

Untitled goose game for PC. 
I havent tested this on other platforms 
Please support developers of games you enjoy and aquire this legally.
https://goose.game/

To dump the UGG Unity .asset file.
Utiny Ripper
https://github.com/mafaca/UtinyRipper

For importing models into UGG Unity .asset files
Unity Asset Bundle Extractor
https://github.com/DerPopo/UABE

Your choice of 3D modeling Software. Must be able to edit .obj files
I use blender because it is free
https://www.blender.org/

Setup:

1) Download GooseTools (This repository)
2) Download Utiny Ripper
3) Download UBAE
3) Locate your installation of Untitled goosegame
4) Create a copy of your game for modding (Highly Recoommneded)



Modifying a 3D Model:


1) Create a dump of game files using Utiny Ripper

2) Use GooseTool's asset_to_obj script extract 3D model in .obj form from mesh. 

	python asset_to_obj.py <utiny_mesh_dump.asset>


3) Use Program such as blender to edit the 3d model. Use the exported .obj as a size and position reference if importing a 3rd party model

4) Export your 3D model from blender as an .OBJ file

5) Run your new .Obj thorugh the preprocessor.

	python object_preprocess.py <your_object.obj>

7) Use GooseTool's obj_to_asset script to reimport your edited .obj file. Include your original asset file.

	python obj_to_asset.py <utiny_mesh_dump.asset> <your_object_preprocessed.py>

8) Use GooseTool's asset_to_UABE script to convert the Unity .asset file to an UABE asset dump file.
	
	python asset_to_UABE.py <your_recompiled_asset.asset>

9) Use Unity Asset Bundel Extractor to replace the in game model with your UABE asset dump file.

10) Start the game and check out your work.







 

V.0.01

- Added .object preprocessor to run on a model before you import it.
	1) convert square face geometry to triangls to match UGG .asset structure
	2) Uncompress mesh with 3 index Buffers into 1 single index buffer to match UGG .asset structure
	3) Fixed previous normal issue.
- Full mesh replacement supported. 
	You can import your own 3D model. Faces and models 
	All imported models are set to blue while I collect data.
	Future goal to compile models with color defintion file


V.0.01 - beta release
Known issues and Limitations:

	1)Normals Disabled: Blender does some type of compression on the normals in the obj file. 
	Currently all normals are stripped from imported models which causes them to be sort of transparents.


	2) I havent decoded how the colors are encoded yet. My attempts still crash the game.
	As a result, you can only edit the models by changing the vertex positon.
	You can not create addtional vertexs or faces at this time.

3) You cant edit colors at this time

4) Havent looked into bone structures
##############################################################################################

