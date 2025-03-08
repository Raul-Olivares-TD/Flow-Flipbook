# FLIPBOOK TO FLOW.
- This tool is an HDA for upload flipbooks from Houdini to Flow/Shotgun/ShotGrid.
- This tool creates a flipbook in Houdini upload it to Flow and Notify via Discord.
- This tool is complemented by the Scene Builder to continue with the small development of the pipeline.
	- Creates a scene with all configured for the artist. (Scene Builder)
	- Upload flipbooks to review at Flow. (Flipbook to Flow)
	- Upload assets to Flow. (Coming Soon)
- This tool allows you to create two types of flipbooks.
	- Traditional flipbook.
	- OpenGL flipbook that allows you to create wedges to create variants and use image magic.

## HOW TO INSTALL.
##### DIRECTORY MANAGEMENT

- Put the directory visualnoobs inside the directory otls at the path at the directory *$HFS* it is the documents directory, something like this: *"C:/Users/User/Documents/houdini20.5/"*.
- The result should be something like: *"C:/Users/User/Documents/houdini20.5/otls/visualnoobs"*.
	- This directory contains inside him 4 scripts to use the tool correctly:
		- **discordNotifier.py** -> This scripts notify via discrod.
		- **flipbookGenerator.py** ->  This scripts create the traditional flipbook manage the incremental version and all directories and files.
		- **flowConnections.py** -> Creates the connections with Flow and gets all the data from Flow to Houdini.
		- **openglPdg.py** -> This scripts create the OpenGL flipbook and manage all the work items and pdg functions.
- Put the HDA inside the directory otls at the path at the directory *$HFS* it is the documents directory, something like this: *"C:/Users/User/Documents/houdini20.5/"*.
- The result should be something like: *"C:/Users/User/Documents/houdini20.5/otls/td_flipbook.otlIc"*.

##### HOUDINI.ENV

- Houdini have a houdini.env file in that we need to add this lines.
- Python Path -> For use the scpripts properly at Houdini.
		PYTHONPATH = "C:\Users\User\Documents\houdini20.5\otls\visualnoobs;C:\Users\User\Python\Python311\Lib\site-packages;C:\Users\User\Documents\houdini20.5\otls"
- Flow user -> In that line we must write the user that we have in Flow/ShotGrid/ShotGun.
		FLOW_USER = "email register at flow of each user" # Ex: "jj2inline@gmail.com"
- Discord user -> In that line we must write the user that we have in Discord.
		DISCORD_USER = "raul"
- Discord channel ->  In that line we must write the Discrod channel id to notify.
		DISCORD_CHANNEL = "1231231231231231223123"

