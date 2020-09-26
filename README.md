# GooseTools
Mesh Replacment Modkit for Untitled Goose Game.
Written by: Grant Hilgert
Sepetember 2020


Mesh Extraction and Reimportation Toolkit for Untitled Goose Game.
Works with Utiny Ripper and UABE (Unity Asset Bundle Extractor)

Description: This tool kit will allow you to modify in game 3D models. You can also completely replace the 3d model with your own .obj file. Colors are supported. 


**LATEST RELEASE- V1.00 RELEASE**

Version 1.00 Release Features:

	-Convert Mesh .asset files into fully colored .obj and .mtl pair for easy import and modification with blender
	
	-Convert fully colored .obj and .mtl pair into .asset file
	
	-Convert .asset file into UABE (Unity Assit Bundle Extractor) dump file for easy import back into the game.
	
	-Tutorials coming soon. See below for high level example.

What Vaersion 1.00 Cannot do:
	
	-Edit the goose or NPC (Gardeners, Shopkeeper, Neightbors, etc). This is planned for Version 1.20 with work already being done.
	
	-Edit the map. Planned, no proof of concept
	
	-Edit the task. Planned, no proof of concept

Known bugs:
	
	-Material Error when importing large and complete model. May need some extra preprocessing to sort the vertex by color. This error will result in you importing model having corrupt colors. If you export it again, you will have x10 the materials of your original model. This may be caused by the conversion of face materials used in object files to vertex colors used in the game. The face list is sorted and the vertex list are not. When exporting back out of the game, the extractor creates a new material each time the material changes. Since the list is not sorted, the material changes often resulting is many duplicate materials being created in the .obj file.
	
	-There are probably other stuff. If you come across something, please report it.



About: This is a series of scripts used to encode and decode Unity .asset files used in the Untitled Goose Game.
This may work on other games. Let me know if you try! Feel free share your results/issues with me.





**Required Dependencies:**

1)Pyton 3: The scripts are python.

https://www.python.org/

Untitled goose game for PC. Build on Windows 10. Sorry. 
Please support developers of games you enjoy and aquire this legally.

https://goose.game/

2)To dump the UGG Unity .asset file.
Utiny Ripper

https://github.com/mafaca/UtinyRipper

3)For importing models into UGG Unity .asset files
Unity Asset Bundle Extractor

https://github.com/DerPopo/UABE

4)Your choice of 3D modeling Software. Must be able to edit .obj files
I use blender because it is free

https://www.blender.org/

**Setup:**

1) Download GooseTools (This repository)
2) Download Utiny Ripper
3) Download UBAE
3) Locate your installation of Untitled goosegame
4) Create a copy of your game for modding (Highly Recoommneded)



**Modifying a 3D Model:**


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




V.1.00
	-Convert Mesh .asset files into fully colored .obj and .mtl pair for easy import and modification with blender
	-Convert fully colored .obj and .mtl pair into .asset file
	-Convert .asset file into UABE (Unity Assit Bundle Extractor) dump file for easy import back into the game.
	-Material Error when importing large and complete model. May need some extra preprocessing to sort the vertex by color.
V.0.02
	-Added .object preprocessor to run on a model before you import it.
	-convert square face geometry to triangls to match UGG .asset structure
	-Uncompress mesh with 3 index Buffers into 1 single index buffer to match UGG .asset structure
	-Fixed previous normal issue.
	- Full mesh replacement supported. 
	-You can import your own 3D model. Faces and models 
	-All imported models are set to blue while I collect data.
	-Future goal to compile models with color defintion file
V.0.01
	-Normals Disabled: Blender does some type of compression on the normals in the obj file. 
	Currently all normals are stripped from imported models which causes them to be sort of transparents.
