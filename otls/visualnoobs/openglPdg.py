import flipbookGenerator
import hou
import os
import time


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
				# Get the top node
				top = children

		return top

	def wedge_activate(self):
		"""Activates/deactivate the wedge node depending the wedge check.

		:return: A wedge node
		:rtype: <Instance of wedge node>
		"""

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
			hou.pwd().parm("wdgatt").set(0)
		else:
			wedge.bypass(False)	

		return wedge

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
			hou.pwd().parm("wdgatt").set(0)

	def wedging(self):
		""" Pass the parameters to creates wedges from the HDA to the wedge node."""
		wdgatt = hou.pwd().parm("wdgatt").eval()
		wedge_node = self.wedge_activate()

		for i in range(wdgatt):
			# Attribute Name from HDA to wedge node
			wdgatt_name = hou.pwd().parm(f"wdgatt_name{str(i+1)}").eval()
			wedge_node.parm(f"name{i+1}").set(wdgatt_name)
			# Attribute Type from HDA to wedge node
			wdgatt_type = hou.pwd().parm(f"wdgatt_type{str(i+1)}").eval()
			wedge_node.parm(f"type{i+1}").set(wdgatt_type)
			# Wedge Type from HDA to wedge node
			wdg_type = hou.pwd().parm(f"wdg_type{str(i+1)}").eval()
			wedge_node.parm(f"wedgetype{i+1}").set(wdg_type)
			# Gets the wedge type number iteration
			type_iteration = hou.pwd().parm(f"wdg_type{str(i+1)}").name()[-1]

			try:
				# Random Samples from HDA to wedge node
				random_samples = hou.pwd().parm(f"rndsamples{str(i+1)}").eval()
				wedge_node.parm(f"random{str(i+1)}").set(random_samples)

				# Float Attribute Types
				if wdgatt_type == 0 and wdg_type == 0:
					# Range values from HDA to wedge node
					float_start_end = hou.pwd().parmTuple(f"wdg_fstr_fend{type_iteration}").eval()
					wedge_node.parmTuple(f"floatrange{type_iteration}").set(float_start_end)

				elif wdgatt_type == 0 and wdg_type == 1:
					# Value from HDA to wedge node
					float_value = hou.pwd().parm(f"wdg_float_value{type_iteration}").eval()
					wedge_node.parm(f"floatvalue{type_iteration}").set(float_value)

				elif wdgatt_type == 0 and wdg_type == 2:
					# Value List from HDA to wedge node
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parm(f"floatvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parm(f"floatvalue{type_iteration}_{str(i+1)}").set(value)

				elif wdgatt_type == 0 and wdg_type == 3:
					# Bracket values from HDA to wedge node
					bracket = hou.pwd().parmTuple(f"wdg_float_bracket{type_iteration}").eval()
					wedge_node.parmTuple(f"floatbracket{type_iteration}").set(bracket)

				# Float Vector Attribute Types
				if wdgatt_type == 1 and wdg_type == 0:
					# Range values from HDA to wedge node
					start4 = hou.pwd().parmTuple(f"wdg_fstart_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"floatrangestart{type_iteration}").set(start4)
					end4 = hou.pwd().parmTuple(f"wdg_fend_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"floatrangeend{type_iteration}").set(end4)

				elif wdgatt_type == 1 and wdg_type == 1:
					# Value from HDA to wedge node
					float_value4 = hou.pwd().parmTuple(f"wdg_fvalue_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"floatvectorvalue{type_iteration}").set(float_value4)

				elif wdgatt_type == 1 and wdg_type == 2:
					# Values List from HDA to wedge node
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parmTuple(f"fvectorvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parmTuple(f"floatvector{type_iteration}_{str(i+1)}").set(value)

				elif wdgatt_type == 1 and wdg_type == 3:
					# Bracket Values from HDA to wedge node
					center4 = hou.pwd().parmTuple(f"wdg_fcenter_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"floatvectorcenter{type_iteration}").set(center4)
					offset4 = hou.pwd().parmTuple(f"wdg_foffset_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"floatvectoroffset{type_iteration}").set(offset4)

				# Integer Attribute Types
				if wdgatt_type == 2 and wdg_type == 0:
					# Range values from HDA to wedge node
					int_start_end = hou.pwd().parmTuple(f"wdg_istr_iend{type_iteration}").eval()
					wedge_node.parmTuple(f"intrange{type_iteration}").set(int_start_end)

				elif wdgatt_type == 2 and wdg_type == 1:
					# Value from HDA to wedge node
					int_value = hou.pwd().parm(f"wdg_ivalue{type_iteration}").eval()
					wedge_node.parm(f"intvalue{type_iteration}").set(int_value)

				elif wdgatt_type == 2 and wdg_type == 2:
					# Values List from HDA to wedge node
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parm(f"intvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parm(f"intvalue{type_iteration}_{str(i+1)}").set(value)
                    
				elif wdgatt_type == 2 and wdg_type == 3:
					# Brackets values from HDA to wedge node
					bracket = hou.pwd().parmTuple(f"wdg_ibracket{type_iteration}").eval()
					wedge_node.parmTuple(f"intbracket{type_iteration}").set(bracket)      

				# Integer Vector Attributes Types
				if wdgatt_type == 3 and wdg_type == 0:
					# Range values from HDA to wedge node
					start4 = hou.pwd().parmTuple(f"wdg_istart_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"intrangestart{type_iteration}").set(start4)
					end4 = hou.pwd().parmTuple(f"wdg_iend_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"intrangeend{type_iteration}").set(end4)

				elif wdgatt_type == 3 and wdg_type == 1:
					# Value from HDA to wedge node
					int_value4 = hou.pwd().parmTuple(f"wdg_ivalue_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"intvectorvalue{type_iteration}").set(int_value4)

				elif wdgatt_type == 3 and wdg_type == 2:
					# Values List from HDA to wedge node
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parmTuple(f"ivectorvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parmTuple(f"intvector{type_iteration}_{str(i+1)}").set(value)

				elif wdgatt_type == 3 and wdg_type == 3:
					#Bracket Values from HDA to wedge node
					center4 = hou.pwd().parmTuple(f"wdg_icenter_v4{type_iteration}").eval()
					wedge_node.parmTuple(f"intvectorcenter{type_iteration}").set(center4)
					offset4 = hou.pwd().parmTuple(f"wdg_ioffset_v4{t}").eval()
					wedge_node.parmTuple(f"intvectoroffset{type_iteration}").set(offset4)

				# String Attributes Types
				if wdgatt_type == 4:
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parmTuple(f"stringvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parmTuple(f"strvalue{type_iteration}_{str(i+1)}").set(value)

				# Color Attributes Types
				if wdgatt_type == 5 and wdg_type == 0:
					# Range values from HDA to wedge node
					start4 = hou.pwd().parmTuple(f"wdg_cstart{type_iteration}").eval()
					wedge_node.parmTuple(f"colorrangestart{type_iteration}").set(start4)
					end4 = hou.pwd().parmTuple(f"wdg_cend{type_iteration}").eval()
					wedge_node.parmTuple(f"colorrangeend{type_iteration}").set(end4)

				elif wdgatt_type == 5 and wdg_type == 1:
					# Value from HDA to wedge node
					color_value = hou.pwd().parmTuple(f"wdg_cvalue{type_iteration}").eval()
					wedge_node.parmTuple(f"colorvalue{type_iteration}").set(color_value)

				elif wdgatt_type == 5 and wdg_type == 2:
					# Values List from HDA to wedge node
					list_value = hou.pwd().parm(f"wdg_values_list{type_iteration}").eval()
					wedge_node.parm(f"values{type_iteration}").set(list_value)

					for i in range(list_value):
						value = hou.pwd().parmTuple(f"colorvalue{type_iteration}_{str(i+1)}").eval()
						wedge_node.parmTuple(f"colorvalue{type_iteration}_{str(i+1)}").set(value)

				elif wdgatt_type == 5 and wdg_type == 3:
					# Bracket Values from HDA to wedge node
					center4 = hou.pwd().parmTuple(f"wdg_center_cbracket{type_iteration}").eval()
					wedge_node.parmTuple(f"colorcenter{type_iteration}").set(center4)
					offset4 = hou.pwd().parmTuple(f"wdg_offset_cbracket{type_iteration}").eval()
					wedge_node.parmTuple(f"coloroffset{type_iteration}").set(offset4)

			except:
				pass


class FlipbookPdg:
	def ffmpeg_basename(self, output_path):
		out = output_path
		name = flipbookGenerator.WalkIntoDirs().version_increment_flipbook()

		for pdg in TopsOperations().top_node().children():
			if "ffmpegencodevideo" == pdg.type().name():
				ffmpeg = pdg

		# Output path for the ffmpeg top node
		ffmpeg.parm("outputfilepath").set(f"{out}{name}.mp4")

	def cook_nodes(self):
		TopsOperations().top_node().generateStaticWorkItems(block=True)
		time.sleep(0.5)
		TopsOperations().top_node().cookOutputWorkItems(block=True)
		TopsOperations().top_node().dirtyAllWorkItems(False)

