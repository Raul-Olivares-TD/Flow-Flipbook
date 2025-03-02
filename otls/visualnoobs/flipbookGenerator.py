import ffmpeg
import flowConnections
import hou
import os
from pathlib import Path


class Elements:
    def __init__(self):
        # Gets an Instance of Scene Viewer
        self.scene_viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        # Gets an Instance of the Viewport
        self.viewport = self.scene_viewer.curViewport()
        # Gets an Instance of the Viewport Settings
        self.view_settings = self.viewport.settings()
    
    def camera_set(self):
        """Sets the camera at the viewport view."""

        # Gets the camera node at the HDA
        cam = hou.pwd().parm("cam").evalAsNode()
        # Sets the camera
        self.view_settings.setCamera(cam)
    
    def hide_elements(self):
        """Hide elements that shows at the viewport on top and bottom sides."""

        # Hide camera
        self.view_settings.showsCameraName(False)
        # Hide view persp
        self.view_settings.showsName(False)
        self.view_settings.enableGuide( hou.viewportGuide.FloatingGnomon,
                                        False)
        # Hide the fps
        self.view_settings.enableGuide(hou.viewportGuide.ShowDrawTime, False)
        # Hide the geo info
        self.view_settings.geometryInfo(hou.viewportGeometryInfo.Off)
        # Hide gnomon
        plane = self.scene_viewer.referencePlane()
        # Hide grid
        plane.setIsVisible(False)        
        
    def show_elements(self):
        """Show elements that shows at the viewport on top and bottom sides."""

        # Shows camera
        self.view_settings.showsCameraName(True)
        # Shows view persp
        self.view_settings.showsName(True)
        # Shows gnomon
        self.view_settings.enableGuide( hou.viewportGuide.FloatingGnomon,
                                        True)
        # Shows the fps
        self.view_settings.enableGuide(hou.viewportGuide.ShowDrawTime, True)
        # Shows the geo info
        self.view_settings.geometryInfo(hou.viewportGeometryInfo.AlwaysOn)
        plane = self.scene_viewer.referencePlane()
        # Shows grid
        plane.setIsVisible(True)
                

class Flipbook:
    def __init__(self):
        # Gets an Instance of Scene Viewer
        self.scene_viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        # Gets an Instance of the flipbook Settings
        self.fb_settings = self.scene_viewer.flipbookSettings()
        # Creating a copy of the flipbook settings
        self.fb_stash = self.fb_settings.stash()
        
    def flipbook_settings(self, output_path):
        """Creates the settings for generate a flipbook.
        
        :param output_path: Path to save the flipbook, images...
        """

        # Gets the output path argument
        out = output_path
        # Gets the settings of the frame range from the HDA
        frame_range = hou.pwd().parmTuple("frames").eval()
        # Sets the frame range
        self.fb_stash.frameRange(frame_range)
        # Gets the settings of the resolution from the HDA
        res = hou.pwd().parmTuple("res").eval()
        # Sets the resolution
        self.fb_stash.resolution(res)
        # Sets the output from export the files
        self.fb_stash.output(f"{out}test_$F4.png")
        # MPlay deactivate
        self.fb_stash.outputToMPlay(False)
        # Exec the flipbook with the stash settings
        self.scene_viewer.flipbook(settings=self.fb_stash)
            

class Converter:
    def convert_mp4(self, output_path):
        """Convert the images to an mp4.        

        :param output_path: Path to save the flipbook, images...
        """

        # Gets the output path argument
        out = output_path
        # Gets the basename with correct version from WalkIntoDirs class
        version = WalkIntoDirs().version_increment_flipbook()
        # Fuse the out paths with the version and video extension
        file_mp4 = f"{out}_{version}.mp4"
        # Gets the path to search the images
        input_file = ffmpeg.input(f"{out}test_%04d.png")
        # Sets the path to export the flipbook video
        output_file = input_file.output(file_mp4)
        # Exec the convert
        output_file.run()
                
        
class WalkIntoDirs:
    def remove_images(self, output_path):
        """Remove the temp images generates to create the flipbook.
        
        :param output_path: Path where the images are
        """ 
        
        # Gets the output path argument
        out = output_path      
        for image in Path(out).glob(f"test_*.png"):
            # Remove images
            image.unlink()
            
    def version_increment_flipbook(self):
        """Increment the version of each flipbook generated.

        :return: The name and version correctly
        :rtype: str 
        """

        # Gets the basename without the extension .hip
        file = os.path.splitext(hou.hipFile.basename())
        file_split = file[0].split("_")
        # Gets the name of the file
        name = file_split[-2]
        # Gets the version of the file
        version = file_split[-1]
        # Merge the name and the version correctly
        flipbook_file = f"{name}_{version}"
        
        return flipbook_file      
       

class Parameters:
    def menu_project(self):
        projects = flowConnections.Flow().projects()

        token = []
        label = []

        for project in projects:
            name = project["name"]
            token.append(name)
            label.append(name)

        node_type = hou.pwd().type().definition()
        group = node_type.parmTemplateGroup() 

        project_menu = hou.pwd().parm("project").parmTemplate()
        project_menu.setMenuItems(token)
        project_menu.setMenuLabels(label)

        group.replace("project", project_menu)
        node_type.setParmTemplateGroup(group)    
            
    
    def menu_sequence(self):
        sequences = flowConnections.Flow().sequences()

        token = []
        label = []

        for sequence in sequences:
            token.append(sequence)
            label.append(sequence)

        node_type = hou.pwd().type().definition()
        group = node_type.parmTemplateGroup() 

        tokens = list(dict.fromkeys(token))
        labels = list(dict.fromkeys(label))

        sequence_menu = hou.pwd().parm("seq").parmTemplate()
        sequence_menu.setMenuItems(tokens)
        sequence_menu.setMenuLabels(labels)

        group.replace("seq", sequence_menu)
        node_type.setParmTemplateGroup(group)
    
    def menu_shot(self):
        shots = flowConnections.Flow().shots()

        token = []
        label = []

        for shot in shots:
            name = shot["name"]
            token.append(name)
            label.append(name)

        tokens = list(dict.fromkeys(token))
        labels = list(dict.fromkeys(label))

        node_type = hou.pwd().type().definition()
        group = node_type.parmTemplateGroup() 

        shot_menu = hou.pwd().parm("shot").parmTemplate()
        shot_menu.setMenuItems(tokens)
        shot_menu.setMenuLabels(labels)

        group.replace("shot", shot_menu)
        node_type.setParmTemplateGroup(group)
    
    def menu_task(self):
        tasks = flowConnections.Flow().tasks()

        token = []
        label = []

        for task in tasks:
            name = task["content"]
            token.append(name)
            label.append(name)

        node_type = hou.pwd().type().definition()
        group = node_type.parmTemplateGroup() 

        sequence_menu = hou.pwd().parm("task").parmTemplate()
        sequence_menu.setMenuItems(token)
        sequence_menu.setMenuLabels(label)

        group.replace("task", sequence_menu)
        node_type.setParmTemplateGroup(group)
        
    def menu_parameters_default(self):
        basename = hou.hipFile.basename()
        basename_split = basename.split("_")
        project = basename_split[0]
        seq = basename_split[1]
        shot = basename_split[2]+"_"+basename_split[3]
        task = basename_split[4]

        # Project
        label_project = hou.pwd().parm("project").menuLabels()
        index_project = label_project.index(project)
        sets_project = hou.pwd().parm("project").set(index_project)

        # Seq
        label_seq = hou.pwd().parm("seq").menuLabels()
        index_seq = label_seq.index(seq)
        sets_seq = hou.pwd().parm("seq").set(index_seq)

        # Shot
        label_shot = hou.pwd().parm("shot").menuLabels()
        index_shot = label_shot.index(shot)
        sets_shot = hou.pwd().parm("shot").set(index_shot)    

        # Task
        label_task = hou.pwd().parm("task").menuLabels()
        index_task = label_task.index(task)
        sets_task = hou.pwd().parm("task").set(index_task) 