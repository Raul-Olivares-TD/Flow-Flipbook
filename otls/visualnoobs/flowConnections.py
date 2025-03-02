import flipbookGenerator
import os
import shotgun_api3


class Flow:
	def __init__(self):
		self.sg = shotgun_api3.Shotgun("https://labpro.shotgrid.autodesk.com",
									   script_name="tdlab",
									   api_key="0Wqebldthin_dyeiogfkvqfqf")

	def projects(self):
		"""Get the project on the user is assigned to.

		:return: List with a dictionary with the name, id and type of the projects.
		:rtype: list
		"""
		# os.environ["FLOW_USER"]
		SG_USER = "raultd379@outlook.es" 

		filters = [["email", "is", SG_USER]]
		
		# Gets the HumanUser type, id and the projects for the user	
		project_response = self.sg.find("HumanUser", filters=filters, 
									fields=["projects"])

		self.user_data = project_response[0]

		# Gets the project id, name and type
		projects = self.user_data["projects"]

		return projects

	def tasks(self):
		"""Get the tasks on the user is assigned to.

		:return: List with a dictionary with the name, 
		id, shot and project of each task.
		:rtype: list
		"""
		tasks = []
		for project_id in self.projects():

			filters = [
				["project", "is", {"type": "Project", "id": project_id["id"]}],
				["task_assignees", "is", self.user_data]
			]

			fields = ["content", "entity", "project"]

			# Gets the name, shot and project of the tasks
			tasks_response = self.sg.find("Task", filters, fields)

			tasks += [task for task in tasks_response]

		return tasks

	def shots(self):
		"""Creates the shots names from the tasks.
		
		:return: A list with the shots names.
		:rtype: list
		"""
		# Gets the id, name, type of the shots
		shots = [shot["entity"] for shot in self.tasks()]

		return shots

	def sequences(self):
		"""Creates the sequences names from the tasks.
		
		:return: A list with the sequences names.
		:rtype: list
		"""
		sequence = [sequence["entity"]["name"].split("_")[0]
				    for sequence in self.tasks()]
  		
		return sequence

	def tasks_name(self):
		"""Creates the tasks name from the tasks.
		
		:return: A list with the tasks names.
		:rtype: list
		"""
		# task = [task["content"] for task in self.tasks()]
		task = {task["content"] : task["id"] for task in self.tasks()}

		return task

	def project_name(self):
		"""Creates the projects name from the tasks.
		
		:return: A list with the projects names.
		:rtype: list
		"""
		# project = [project["project"]["name"] for project in self.tasks()]
		project = {project["name"] : project["id"] 
             	   for project in self.projects()}

		return project

	def upload_flipbook(self):
     
		project_name = hou.pwd().parm("project").evalAsString()		
		task_name = hou.pwd().parm("task").evalAsString()
		description = hou.pwd().parm("desc").evalAsString()
		outpath = hou.pwd().parm("out").evalAsString()
		basename = flipbookGenerator.WalkIntoDirs().version_increment_flipbook()
  
		project_id = Flow().project_name()[project_name]
		task_id = Flow().tasks_name()[task_name]
		self.projects()
		user_id = self.user_data["id"]
  
		data = {
			"project": {"type": "Project", "id": project_id},
			"sg_task": {"type": "Task", "id": task_id},
			"code": "fxDesintegracion_v004",
			"description": description,
			"user": {"type": "HumanUser", "id": user_id}
		}
  
		r = self.sg.create("Version",data, return_fields=["id"])
    
		movie = f"{outpath}{basename}"
  
		up = self.sg.upload("Version", r["id"], movie, field_name="sg_uploaded_movie")

