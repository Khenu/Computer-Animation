# N3 muscle pose creation v3.py
# Created by Laushon Neferkara on 3/15/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# 1. Set Based On attribute to pose
# 2. Duplicate cross sections
# 3. Unlock attributes
# 4. Parent cross section targets to pose group
# 5. Create blend shape node
# 6. Connect driver outputs to blend shape node



scriptName = 'N3 muscle pose creation v3.py'
print '\r' + scriptName + ' running'

# Import function module
import nm




# Create simple group
def makeSimpleGrp(grpName, parent):
	
	hideList = [
		'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ']
	
	mc.group(
		em=True, 
		r=True, 
		n=grpName)
	
	for hidden in hideList:
		mc.setAttr(
			grpName + '.' + hidden, 
			keyable=False, 
			lock=True, 
			cb=False)
	
	mc.parent(
		grpName, 
		parent)


# Unlock cross section
def unlockCS(node):
	
	attrList = [
		'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ']
	
	for attr in attrList:
		mc.setAttr(
			node + '.' + attr, 
			lock=False)

	
	visibility = node + '.visibility'
	
	mc.setAttr(
		visibility, 
		keyable=True)	
	
	if mc.connectionInfo(visibility, isDestination=True):
		source = mc.connectionInfo(visibility, sourceFromDestination=True)
		mc.disconnectAttr(
			source, 
			visibility)



# System name
mx = 'N3'

# Existing scene objects
latData = mx + '_humerus_lat_data'
twistData = mx + '_humerus_twist_data'
muscleSdkDriver = 'N3_muscleSdk_driver'
muscleShapeDriver = 'N3_muscleShape_driver'

# New scene objects


# Attribute lists
longList = [
	'x0', 'x22h', 'x45', 'x67h', 'x90', 'x112h', 'x135', 'x157h', 'x180', 'xn157h', 
	'xn22h']

latList = [
	'y0', 'y17', 'y34', 'y51', 'y68', 'y85', 'y102', 'y119', 'y136', 'y153', 'y170']

twistList = [
	'w0', 'w30', 'w60', 'w90', 'wn30', 'wn60', 'wn90']

# Pose values
longitudes = [
	0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, -157.5, -22.5]

latitudes = [
	0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170]

twists = [
	0, 30, 60, 90, -30, -60, -90]

# Character controls
longCtrl = 'L_arm_ctrl.rotateY'
latCtrl = 'L_arm_ctrl.rotateX' # neg values
twistCtrl = 'L_arm_ctrl.twist'



# Muscle
muscle = 'teresMajor'
muscleNode = 'cMuscleCreatorMus_L_teresMajor1'

crossSectionList = [
	'iControlMidMus_L_teresMajor11_crossSectionREST',
	'iControlMidMus_L_teresMajor21_crossSectionREST',
	'iControlMidMus_L_teresMajor31_crossSectionREST',
	'iControlMidMus_L_teresMajor41_crossSectionREST',
	'iControlMidMus_L_teresMajor51_crossSectionREST']



# 1. Set Based On attribute to pose
mc.setAttr(muscleNode + '.basedOn', 1)



# Create groups to hold poses
mainPoseGrp = muscle + '_pose_grp'
makeSimpleGrp(mainPoseGrp, 'gina')
for long in longList: 
	longPoseGrp = muscle + '_' + long + '_grp'
	makeSimpleGrp(longPoseGrp, mainPoseGrp)
	for lat in latList:
		latPoseGrp = muscle + '_' + long + '_' + lat + '_grp'
		makeSimpleGrp(latPoseGrp, longPoseGrp)
		for twist in twistList:
			twistPoseGrp = muscle + '_' + long + '_' + lat + '_' + twist + '_grp'
			makeSimpleGrp(twistPoseGrp, latPoseGrp)
			#
			mc.setAttr(
				twistPoseGrp + '.visibility', 
				False)



# Move character to pose position
# and duplicate cross sections for twist 0
for i in range(len(longList)): 
	mc.setAttr(longCtrl, longitudes[i])
	for j in range(len(latList)):
		mc.setAttr(latCtrl, -latitudes[j])
		k = 0
		# 2. Duplicate cross sections
		for r in range(len(crossSectionList)):
			
			targetName = (muscle + '_crossSection' + str(r + 1) + '_' + 
				longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
			twistPoseGrp = (muscle + '_' + longList[i] + '_' + latList[j] + '_' + 
				twistList[k] + '_grp')
			
			mc.duplicate(
				crossSectionList[r], 
				n=targetName)
			
			unlockCS(targetName)
			
			mc.parent(
				targetName, 
				twistPoseGrp)
				
					
# Move the arm control back to home position.					
mc.setAttr(longCtrl, 0)
mc.setAttr(latCtrl, 0)
mc.setAttr(twistCtrl, 0)


# 5. Create blend shapes and connect to driver (for twist 0)

for r in range(len(crossSectionList)):
	for i in range(len(longList)): 
		for j in range(len(latList)):
			k = 0
			targetName = (muscle + '_crossSection' + str(r + 1) + '_' + 
				longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
			crossSection = crossSectionList[r]
			
			blendShapeNode = crossSection + '_blendShape'
			
			# Create blend shape node with 1st target. 
			# Add to blend shape node for additional targets.
			if i == 0 and j == 0 and k == 0:
				mc.blendShape(
					targetName, 
					crossSection, 
					name = blendShapeNode)
				bIndex = 1
			else:
				mc.blendShape(
					blendShapeNode, 
					edit=True, 
					t=(crossSection, bIndex, targetName, 1.0))
				bIndex += 1
			
			# 6. Connect driver outputs to blend shape node
			mc.connectAttr(
				muscleShapeDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
					twistList[k], 
				blendShapeNode + '.' + targetName)



print '\r\r' + scriptName + ' completed Successfully\r\r'

