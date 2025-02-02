import hou


class TopsOperations:
	def top_node(self):
		"""Finds the wedge node inside the HDA.

		:return: The wedge node 
		:rtype:	<Instance of top node>
		"""

		# The children nodes in the HDA
		fb_nodes = hou.pwd().children()
		# Search at each children node
		for children in fb_nodes:
			# Find the top node type
			if "topnetmgr" == children.type().name():
				# Get the wedge node
				top = children

		return top

	def wedge_activate(self):
		"""Activates/deactivate the wedge node depending the wedge check."""

		# Gets the check wedge
		wedging = hou.pwd().parm("wdg").eval()

		# Gets the wedge node
		for pdg in self.top_node().children():
			if "wedge" == pdg.type().name():
				wedge = pdg

		# Activate or deactivate the wedge node       
		if wedging == 0:
			wedge.bypass(True)
			hou.pwd().parm("image").set(0)
		else:
			wedge.bypass(False)	

	def image_magick_activate(self):
		"""Activates/deactivate the image magick node."""

		# Gets the check image
		image = hou.pwd().parm("image").eval()

		# Gets the image magick node and the partition frame node
		for pdg in self.top_node().children():
			if "partitionbyframe" == pdg.type().name():
				by_frame = pdg

			if "imagemagick" == pdg.type().name():
				img_magick = pdg   

		# Activate or deactivate the nodes
		if image == 0:
			img_magick.bypass(True)
			by_frame.bypass(True)
		else:
			by_frame.bypass(False)
			img_magick.bypass(False)

	def hide_cheks(self):
		"""Activate/deactivate the image and wedge nodes by opengl check."""

		# Get the opengl chek
		open_gl = hou.pwd().parm("opengl").eval()

		# Activate/deactivate the nodes
		if open_gl == 0:
			hou.pwd().parm("image").set(0)
			hou.pwd().parm("wdg").set(0)

