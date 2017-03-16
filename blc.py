import bpy
import sys
import os
import urllib

########################################################
############### V import core + library V ##############
########################################################

#url = 'http://www.google.com1'

#try:
#	with urllib.request.urlopen(url) as file:
#		print(file.read())
#except:
#	print('URL Error ', url)

blcdir = os.path.dirname(bpy.context.space_data.text.filepath)

if not blcdir in sys.path:
    sys.path.append(blcdir)

#if not os.path.isfile(blcdir+'/blccore.py') or not os.path.isfile(blcdir+'/blclib.txt'):
#	sys.exit('BLC modules not found!')
	
#blclib = blcdir+'/blclib.tsv'
blclib = blcdir+'/blclib/'

import blccore

import importlib
importlib.reload(blccore)

blclist = list()

#with open(blclib, 'r') as file:
#	data = file.readlines()
#	for index in range(0, len(data)):
#		splitline = data[index].split()
#		line = str(index), splitline[0], splitline[1]
#		blclist.append(tuple(line))

#for index in range(0, len(os.listdir(blclibfolder))):
#	print(index)

fileindex = 0
for file in os.listdir(blclib):
	if file.endswith(".txt"):
		with open(blclib + file, 'r') as openfile:
			data = openfile.readline().strip()
			line = str(fileindex), file[:-4], data
			#print(line)
			blclist.append(tuple(line))
	fileindex += 1
#print('\n\tblclist created\n')

#############################################
############### V draw panel V ##############
#############################################

class blc_panel(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'BLC'
	bl_label = 'Bravais Lattices Creator'
	bl_context = 'objectmode'
	
	def draw(self, context):
		
		scene = context.scene		
		layout = self.layout
		
		layout.label(text='All sizes - nm', icon='QUESTION')
		layout.label(text='Emitter properties:', icon='MESH_CUBE')

		layout.prop(scene, 'blc_emitter_name', toggle=True)
		
		row = layout.row()
		row.label(text='Domain: ')
		row.prop_search(scene, 'blc_selected_domain', scene, 'objects')
		row.operator('wm.blc_set_domain')
 
		layout.prop(scene, 'blc_molecule')

		split = layout.split()
		col = split.column()
		sub = col.column(align=True)
		sub.label(text='Emitter size:', icon='ARROW_LEFTRIGHT')
		sub.prop(scene, 'blc_emitter_size_x', text='X')
		sub.prop(scene, 'blc_emitter_size_x', text='Y')
		sub.prop(scene, 'blc_emitter_size_x', text='Z')
		
		row = layout.row()
		row.label(text='Domain:')
		row.label(text=scene.blc_domain_name, icon='RETOPO')

		layout.operator('wm.blc_building', icon='FORCE_LENNARDJONES')

#################################################
############### V start building V ##############
#################################################

class blc_building(bpy.types.Operator):
	bl_idname = 'wm.blc_building'
	bl_label = 'Building'
    
	def execute(self, context):
		
		scene = context.scene
		objects = bpy.data.objects
		ops = bpy.ops
		
		domain = scene.blc_selected_domain
		emitter_name = scene.blc_emitter_name
		
		# save original cursor location
		scene.blc_original_cursor_location = scene.cursor_location
		
		if check_domain(context):
			# with domain
			reset_domain_rotation(domain) # del recommend
			#scn['flagsh'] = False
			# set domain size
			domain_size_x = objects[domain].dimensions[0]
			domain_size_y = objects[domain].dimensions[1]
			domain_size_z = objects[domain].dimensions[2]	
			# activated domain
			scene.objects.active = objects[domain]
			# move cursor to boundingbox center of domain
			ops.object.editmode_toggle()
			ops.mesh.select_all(action='SELECT')
			bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
			ops.view3d.snap_cursor_to_selected()
			ops.object.editmode_toggle()
			# save domain boundingbox center location
			scene.blc_domain_location = scene.cursor_location
			# move cursor to 0.0.0 of domain boundingbox center
			scene.cursor_location[0] = scene.blc_domain_location[0]-domain_size_x/2
			scene.cursor_location[1] = scene.blc_domain_location[1]-domain_size_y/2
			scene.cursor_location[2] = scene.blc_domain_location[2]-domain_size_z/2
			# set start location of bulding process
			atom_location_x = scene.cursor_location[0]
			atom_location_y = scene.cursor_location[1]
			atom_location_z = scene.cursor_location[2]
		else:
			# without domain
			# set domain size			
			domain_size_x = scene.blc_emitter_size_x
			domain_size_y = scene.blc_emitter_size_y
			domain_size_z = scene.blc_emitter_size_z
			# set start location of bulding process
			atom_location_x = 0
			atom_location_y = 0
			atom_location_z = 0
			
		##################################
			
		x = domain_size_x
		y = domain_size_y
		z = domain_size_z
		
		ax = atom_location_x
		ay = atom_location_y
		az = atom_location_z
		
		obj = domain
		name = emitter_name
				
		#######################################################################

		# get file name through selected molecule from blclist
		file_name = blclist[int(scene.blc_molecule)][1]+'.txt'		
		
		# get molecule parameters from blclib
		parameters = get_blclib(file_name)
				
		# if parameters are correctness then start building
		# else print the warning
		if parameters != False:
			print(parameters)
			
			
			
			
			
			
			
			# loop for every in count of chemical elements 
#			for EVERY in parameters['element_count']:
#			
#			
#				# create array of verticles
#				building_verts(parameters)


#				# create emitter
#				create_emitter()



#				# create partsys
#				create_partsys()	
			
			
			
			
		# else print the warning			
		else:
			print(file_name+' file with molecule parameters in '+blclib+' not found!')
		

		

		
		
		
		
		
		
		
		#######################################################################
		# ending
		
		# restore original cursor location
		scene.cursor_location = scene.blc_original_cursor_location
		# restore original value of existing particle variable
		scene.blc_existing_particle = True

		return{'FINISHED'}

############################################
############################################

# leadup domain to building
class blc_set_domain(bpy.types.Operator):
	bl_idname = 'wm.blc_set_domain'
	bl_label = 'Set domain'
    
	def execute(self, context):
        
		scene = context.scene
		objects = bpy.data.objects
		domain = scene.blc_selected_domain
		
		if check_domain(context):
			scene.blc_domain_name = domain
			scene.blc_emitter_size_x = objects[domain].dimensions[0]
			scene.blc_emitter_size_y = objects[domain].dimensions[1]
			scene.blc_emitter_size_z = objects[domain].dimensions[2]
			scene.blc_existing_domain = True
			#scn['flagsh'] = False
			
		return{'FINISHED'}

# check to correctness of domain	
def check_domain(context):
	scene = context.scene
	objects = bpy.data.objects
	domain = scene.blc_selected_domain
	
	correctness = False
	
	if not domain == '' and objects.find(domain) == 0 and objects[domain].type == 'MESH':
		correctness = True
	else:
		correctness = False
		scene.blc_selected_domain = ''
		scene.blc_domain_name = 'No domain'
		scene.blc_existing_domain = False
		
	return correctness

# reset domain rotation
def reset_domain_rotation(domain):
	#bpy.data.objects[domain].hide = False
	bpy.data.objects[domain].rotation_euler[0] = 0    
	bpy.data.objects[domain].rotation_euler[1] = 0
	bpy.data.objects[domain].rotation_euler[2] = 0

# get molecule parameters from blclib	
def get_blclib(file_name):

	# found molecule file
	for root, dirs, files in os.walk(blclib):
		if file_name in files:
			with open(blclib + file_name, 'r') as openfile:
				data = openfile.readlines()

			lines = list()
			
			index = 0
			while index < len(data):
				splitline = data[index].split()
				lines.append(splitline)
				index += 2
	
			#print(parameters)
	
			data = None
						
			parameters = {}
			parameters['element_count']		= lines[1]
			parameters['atom_names']		= lines[2]
			parameters['period']			= lines[3]
			parameters['atom_radiuses']		= lines[4]
			parameters['atom_count']		= lines[5]
#			parameters['atom_positions']	= lines[6]

			del lines
					
		else:
			parameters = False
				
	return parameters

def building_verts(parameters):
	
	verts = []

	window_manager = bpy.context.window_manager
	load = (domain_size_x/period)*(domain_size_y/period)*(domain_size_z/period)
	window_manager.progress_begin(0, load)
	
	
	
	
	verts.append((ex,ey,ez))
	
	
	
#	
#	
#	perh = per/2
#	perhh = perh/2



#	perc = 0
#	ex = ax
#	ey = ay
#	ez = az
#	ix = 1
#	iy = 1
#	iz = 1
#	while (iz-1 < z/(per+zfault)):
#		while (iy-1 < y/(per+yfault)):
#			while (ix-1 < x/per):
#				if type == ('Cube'):
#					buildcube(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('C'):
#					buildc(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('CubeC'):
#					buildcubec(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('CubeM'):
#					buildcubem(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('FeCr-Fe'):
#					buildfecrfe(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('FeCr-Cr'):
#					buildfecrcr(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('WC-W'):
#					buildwcw(ex,ey,ez,verts,per,perh,perhh,scn)
#				elif type == ('WC-C'):
#					buildwcc(ex,ey,ez,verts,per,perh,perhh,scn)
#				ex = ex+per
#				ix = ix+1
#				window_manager.progress_update(perc)
#				perc = perc+1
#			ex = ax
#			ey = ay+(per+yfault)*iy
#			iy = iy+1
#			ix = 1
#		ey = ay
#		ez = az+(per+zfault)*iz
#		iz = iz+1
#		iy = 1  



 
	window_manager.progress_end()
	
	del verts
		
	return{'FINISHED'}	
					
#############################################
############# v initialization v ############
#############################################

classes = (
	blc_panel,
	blc_set_domain,
	blc_building,
)

def register():
	
	scene = bpy.types.Scene
	props = bpy.props

	for cls in classes:
		bpy.utils.register_class(cls)

############################################################ имя источника # emname 
	scene.blc_emitter_name = props.StringProperty(
		name = 'Name',
		description = 'Emitter name',
		default = 'Emitter')
		
############################################################ выбор домена # chobj 
	scene.blc_selected_domain = props.StringProperty(
		name = '',
		description = 'Selected domain')
		
############################################################ тип решётки # lattice
	scene.blc_molecule = props.EnumProperty(
		items = blclist,
		name = 'Molecule',
		default = '0')		
		
############################################################ размеры источника # emx emy emz 
	scene.blc_emitter_size_x = props.FloatProperty(
		name = 'x', 
		description = 'X Emitter size',
		precision = 2,
		min = 0.1,
		max = 20,
		default = 0.4)

	scene.blc_emitter_size_y = props.FloatProperty(
		name = 'y', 
		description = 'Y Emitter size',
		precision = 2,
		min = 0.1,
		max = 20,
		default = 0.4)

	scene.blc_emitter_size_z = props.FloatProperty(
		name = 'z', 
		description = 'Z Emitter size',
		precision = 2,
		min = 0.1,
		max = 20,
		default = 0.4)

############################################################ метка домена # sname 
	scene.blc_domain_name = props.StringProperty(
		name = 'Domain name',
		description = 'Domain name',
		default = 'No domain')

############################################################ флаг наличия домена # flagem 
	scene.blc_existing_domain = props.BoolProperty(
    	default = False)

############################################################ координаты домена # emloc 
	scene.blc_domain_location = props.FloatVectorProperty(
		name = 'Domain location ')  

############################################################ флаг существования частицы # flagat 
	scene.blc_existing_particle = props.BoolProperty(
		default = True)

############################################################ координата 3D курсора # cutemp 
	scene.blc_original_cursor_location = props.FloatVectorProperty(
		name = 'Original cursor location')

############################################################ временные координаты # partemp 
	scene.blc_temp_location = props.FloatVectorProperty(
		name = 'Temp location')

#########################################
############# v unregister v ############
#########################################

def unregister():
	
	scene = bpy.types.Scene
	props = bpy.props
	
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
	del scene.blc_emitter_name
	del scene.blc_selected_domain
	del scene.blc_molecule
	del scene.blc_emitter_size_x
	del scene.blc_emitter_size_y
	del scene.blc_emitter_size_z
	del scene.blc_domain_name
	del scene.blc_existing_domain
	del scene.blc_domain_location
	del scene.blc_existing_particle
	del scene.blc_original_cursor_location
	del scene.blc_temp_location

if __name__ == '__main__':
	register()