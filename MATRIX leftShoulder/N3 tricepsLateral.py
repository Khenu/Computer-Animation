# N3 tricepsLateral.py
# Created by Laushon Neferkara on 3/30/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# 1. Set Based On attribute to pose
# 2. Duplicate cross sections
# 3. Unlock attributes
# 4. Parent cross section targets to pose group
# 5. Create blend shape node
# 6. Connect driver outputs to blend shape node



scriptName = 'N3 tricepsLateral.py'
print '\r' + scriptName + ' running'




def makeMusclePoseSys(muscleName, muscleNode, crossSectionList, controlList):

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

	
	# Lock transforms
	def lockTransforms(node, mode):
		attrList = []
	
		if 'translate' in mode or 'all' in mode:
			attrList.extend(['translateX', 'translateY', 'translateZ'])
		
		if 'rotate' in mode or 'all' in mode:
			attrList.extend(['rotateX', 'rotateY', 'rotateZ'])
		
		if 'scale' in mode or 'all' in mode:
			attrList.extend(['scaleX', 'scaleY', 'scaleZ'])
		
		for attr in attrList:
			mc.setAttr(
				node + '.' + attr, 
				lock=True)



	
	# Existing scene objects
	latData = 'N3_humerus_lat_data'
	twistData = 'N3_humerus_twist_data'
	muscleSdkDriver = 'N3_muscleSdk_driver'
	muscleShapeDriver = 'N3_muscleShape_driver'
	muscleRefGrp = 'muscle_ref_grp'
	musclePoseGrp = 'muscle_pose_grp'
	
	# Attribute lists
	longList = [
		'xn45', 'x0', 'x45', 'x90', 'x135', 'x180']

	latList = [
		'y0', 'y45', 'y90', 'y135', 'y170']

	twistList = [
		'wn90', 'wn45', 'w0', 'w45', 'w90']

	# Pose values
	longitudes = [
		-45, 0, 45, 90, 135, 180]

	latitudes = [
		0, 45, 90, 135, 170]

	twists = [
		-90, -45, 0, 45, 90]

	# Character controls
	longCtrl = 'L_arm_ctrl.rotateY'
	latCtrl = 'L_arm_ctrl.rotateX' # neg values
	twistCtrl = 'L_arm_ctrl.twist'


	# 1. Set Based On attribute to pose
	# mc.setAttr(muscleNode + '.basedOn', 1)

	
	# CREATE POSES 

	# Create groups to hold poses
	for r in range(1, len(controlList) + 1):
		musclePoseGrp = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(r))
		mainPoseGrp = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(r)) + '_pose_grp'
		makeSimpleGrp(mainPoseGrp, musclePoseGrp)
		for long in longList: 
			longPoseGrp = muscleName + '_control%s_' % str(r) + long + '_grp'
			makeSimpleGrp(longPoseGrp, mainPoseGrp)
			for lat in latList:
				latPoseGrp = muscleName + '_control%s_' % str(r) + long + '_' + lat + '_grp'
				makeSimpleGrp(latPoseGrp, longPoseGrp)
				for twist in twistList:
					twistPoseGrp = muscleName + '_control%s_' % str(r) + long + '_' + lat + '_' + twist + '_grp'
					makeSimpleGrp(twistPoseGrp, latPoseGrp)
					#
					mc.setAttr(
						twistPoseGrp + '.visibility', 
						False)

	# Move character to pose position and make poses for twist 0
	for i in range(len(longList)): 
		mc.setAttr(longCtrl, longitudes[i])
		for j in range(len(latList)):
			mc.setAttr(latCtrl, -latitudes[j])
			k = 2	# twist 0
			for r in range(len(controlList)):
				
				twistPoseGrp = (muscleName + '_control%s_' % str(r + 1) + longList[i] + '_' + latList[j] + '_' + 
					twistList[k] + '_grp')

				controlTargetName = (muscleName + '_control' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
# 				
# 				# Create transform group for control curve
# 				twistPoseTransGrp = controlTargetName + '_grp'
# 				mc.group(
# 					empty=True,
# 					name=twistPoseTransGrp,
# 					parent=twistPoseGrp)
# 				
# 				mc.parentConstraint(
# 					controlList[r], 
# 					twistPoseTransGrp,
# 					maintainOffset=False,
# 					n='tempParentConstraint')
# 					
# 				mc.delete('tempParentConstraint')
# 				
# 				lockTransforms(
# 					twistPoseTransGrp,
# 					'all')

				# Duplicate control curves
				mc.duplicate(
					controlList[r], 
					n=controlTargetName)
				
				# Delete the child squash and stretch curves 
				mc.delete(
					mc.listRelatives(
						controlTargetName, 
						type='transform', 
						path=True))
				
				# Unlock transforms for reparenting
				unlockCS(controlTargetName)
			
				mc.parent(
					controlTargetName, 
# 					twistPoseTransGrp)
					twistPoseGrp)

				lockTransforms(
					controlTargetName,
					'rotate, scale')
				
# 
# 				# Duplicate cross sections
# 				targetName = (muscleName + '_crossSection' + str(r + 1) + '_' + 
# 					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
# 			
# 				mc.duplicate(
# 					crossSectionList[r], 
# 					n=targetName)
# 			
# 				unlockCS(targetName)
# 			
# 				mc.parent(
# 					targetName, 
# 					controlTargetName)
# 				
# 				mc.makeIdentity(
# 					targetName, 
# 					apply=True, 
# 					rotate=True)
# 				
# 				lockTransforms(
# 					targetName,
# 					'all')
# 				

					
					
	# Move the arm control back to home position.					
	mc.setAttr(longCtrl, 0)
	mc.setAttr(latCtrl, 0)
	mc.setAttr(twistCtrl, 0)


	# Connect to driver (for twist 0)

	for r in range(len(crossSectionList)):
		pIndex = 0
		for i in range(len(longList)): 
			for j in range(len(latList)):
				k = 2
# 				
# 				# CROSS SECTIONS
# 				targetName = (muscleName + '_crossSection' + str(r + 1) + '_' + 
# 					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
# 			
# 				crossSection = crossSectionList[r]
# 			
# 				blendShapeNode = crossSection + '_blendShape'
# 			
# 				# Create blend shape node with 1st target. 
# 				# Add to blend shape node for additional targets.
# 				if i == 0 and j == 0 and k == 2:
# 					mc.blendShape(
# 						targetName, 
# 						crossSection, 
# 						name = blendShapeNode)
# 					bIndex = 1
# 				else:
# 					mc.blendShape(
# 						blendShapeNode, 
# 						edit=True, 
# 						t=(crossSection, bIndex, targetName, 1.0))
# 					bIndex += 1
# 			
# 				# Connect driver outputs to blend shape node
# 				mc.connectAttr(
# 					muscleShapeDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
# 						twistList[k], 
# 					blendShapeNode + '.' + targetName)
# 				
				
				# Controls
				controlTargetName = (muscleName + '_control' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
				control = controlList[r]
			
				# Create point constraints				
				mc.pointConstraint(
					controlTargetName, 
					control, 
					weight=0.0)

				# Connect driver outputs to point constraint
				mc.connectAttr(
					muscleShapeDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
						twistList[k], 
					control + '_pointConstraint1.' + controlTargetName + 'W' + str(pIndex))
				pIndex += 1
				




# Muscle 5
muscleName5 = 'L_tricepsLongD'
muscleNode5 = 'cMuscleCreatorMus_L_tricepsLongD1'
# crossSectionList5 = [
# 	'iControlMidMus_L_tricepsLongD11_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD21_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD31_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD41_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD51_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD61_crossSectionREST',
# 	'iControlMidMus_L_tricepsLongD71_crossSectionREST']
controlList5 = [
	'iControlMidMus_L_tricepsLongD11', 
	'iControlMidMus_L_tricepsLongD21', 
	'iControlMidMus_L_tricepsLongD31', 
	'iControlMidMus_L_tricepsLongD41', 
	'iControlMidMus_L_tricepsLongD51', 
	'iControlMidMus_L_tricepsLongD61', 
	'iControlMidMus_L_tricepsLongD71']

# Muscle 6
muscleName6 = 'L_tricepsLateral'
muscleNode6 = 'cMuscleCreatorMus_L_tricepsLateralD1'
# crossSectionList6 = [
# 	'iControlMidMus_L_tricepsLateralD11_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD21_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD31_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD41_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD51_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD61_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD71_crossSectionREST',
# 	'iControlMidMus_L_tricepsLateralD81_crossSectionREST']
controlList6 = [
	'iControlMidMus_L_tricepsLateralD11', 
	'iControlMidMus_L_tricepsLateralD21', 
	'iControlMidMus_L_tricepsLateralD31', 
	'iControlMidMus_L_tricepsLateralD41', 
	'iControlMidMus_L_tricepsLateralD51', 
	'iControlMidMus_L_tricepsLateralD61', 
	'iControlMidMus_L_tricepsLateralD71', 
	'iControlMidMus_L_tricepsLateralD81']



makeMusclePoseSys(muscleName5, muscleNode5, crossSectionList5, controlList5)
# makeMusclePoseSys(muscleName6, muscleNode6, crossSectionList6, controlList6)




print '\r\r' + scriptName + ' completed successfully\r\r'
