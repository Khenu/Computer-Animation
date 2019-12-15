# N3 trapeziusMidB.py
# Created by Laushon Neferkara on 4/5/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

scriptName = 'N3 trapeziusMidB.py'
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
	mc.setAttr(muscleNode + '.basedOn', 1)

	
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
				

				# Duplicate cross sections
				targetName = (muscleName + '_crossSection' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
				mc.duplicate(
					crossSectionList[r], 
					n=targetName)
			
				unlockCS(targetName)
			
				mc.parent(
					targetName, 
					controlTargetName)
				
				mc.makeIdentity(
					targetName, 
					apply=True, 
					rotate=True)
				
				lockTransforms(
					targetName,
					'all')
									
					
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
				
				# CROSS SECTIONS
				targetName = (muscleName + '_crossSection' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
				crossSection = crossSectionList[r]
			
				blendShapeNode = crossSection + '_blendShape'
			
				# Create blend shape node with 1st target. 
				# Add to blend shape node for additional targets.
				if i == 0 and j == 0 and k == 2:
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
			
				# Connect driver outputs to blend shape node
				mc.connectAttr(
					muscleShapeDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
						twistList[k], 
					blendShapeNode + '.' + targetName)
				
				
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
				


# Muscle 1
muscleName1 = 'L_trapeziusMidB'
muscleNode1 = 'cMuscleCreatorMus_L_trapeziusMidB1'
crossSectionList1 = [
	'iControlMidMus_L_trapeziusMidB11_crossSectionREST',
	'iControlMidMus_L_trapeziusMidB21_crossSectionREST',
	'iControlMidMus_L_trapeziusMidB31_crossSectionREST',
	'iControlMidMus_L_trapeziusMidB41_crossSectionREST',
	'iControlMidMus_L_trapeziusMidB51_crossSectionREST']
controlList1 = [
	'iControlMidMus_L_trapeziusMidB11', 
	'iControlMidMus_L_trapeziusMidB21', 
	'iControlMidMus_L_trapeziusMidB31', 
	'iControlMidMus_L_trapeziusMidB41', 
	'iControlMidMus_L_trapeziusMidB51']


makeMusclePoseSys(muscleName1, muscleNode1, crossSectionList1, controlList1)

print '\r\r' + scriptName + ' completed successfully\r\r'
