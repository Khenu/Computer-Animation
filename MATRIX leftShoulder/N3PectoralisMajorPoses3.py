# N3PectoralisMajorPoses3.py
# Created by Laushon Neferkara on 9/3/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.



def makeMusclePoseSys(muscleName, muscleNode, crossSectionList, attachRestList):

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


	# Set Based On attribute to pose
	mc.setAttr(muscleNode + '.basedOn', 1)
	
	
	# Move character to pose positions and duplicate cross sections
	for i in range(len(longList)): 
		mc.setAttr(longCtrl, longitudes[i])
		for j in range(len(latList)):
			mc.setAttr(latCtrl, -latitudes[j])
			for k in range(len(twistList)):
				# Duplicate cross sections
				for r in range(len(crossSectionList)):
					
					twistPoseGrp = (muscleName + '_' + longList[i] + '_' + latList[j] + '_' + 
						twistList[k] + '_ref_grp')
			
					# Duplicate attach rest curves
					attachRefName = (muscleName + '_attachRest' + str(r + 1) + '_' + 
						longList[i] + '_' + latList[j] + '_' + twistList[k] + '_ref')
				
					mc.duplicate(
						attachRestList[r], 
						n=attachRefName)
				
					# Delete the child squash and stretch curves 
					mc.delete(
						mc.listRelatives(
							attachRefName, 
							type='transform', 
							path=True))
			
					unlockCS(attachRefName)
			
					mc.parent(
						attachRefName, 
						twistPoseGrp)


					# Duplicate cross sections
					refName = (muscleName + '_crossSection' + str(r + 1) + '_' + 
						longList[i] + '_' + latList[j] + '_' + twistList[k] + '_ref')
			
					mc.duplicate(
						crossSectionList[r], 
						n=refName)
			
					unlockCS(refName)
			
					mc.parent(
						refName, 
						attachRefName)				
					
	# Move the arm control back to home position.					
	mc.setAttr(longCtrl, 0)
	mc.setAttr(latCtrl, 0)
	mc.setAttr(twistCtrl, 0)



	# CREATE POSES 

	# Create groups to hold poses
	mainPoseGrp = muscleName + '_pose_grp'
	makeSimpleGrp(mainPoseGrp, musclePoseGrp)
	for long in longList: 
		longPoseGrp = muscleName + '_' + long + '_grp'
		makeSimpleGrp(longPoseGrp, mainPoseGrp)
		for lat in latList:
			latPoseGrp = muscleName + '_' + long + '_' + lat + '_grp'
			makeSimpleGrp(latPoseGrp, longPoseGrp)
			for twist in twistList:
				twistPoseGrp = muscleName + '_' + long + '_' + lat + '_' + twist + '_grp'
				makeSimpleGrp(twistPoseGrp, latPoseGrp)
				mc.setAttr(
					twistPoseGrp + '.visibility', 
					False)

	# Move character to pose position and make poses for twist 0
	for i in range(len(longList)): 
		mc.setAttr(longCtrl, longitudes[i])
		for j in range(len(latList)):
			mc.setAttr(latCtrl, -latitudes[j])
			k = 2	# twist 0
			for r in range(len(crossSectionList)):
				
				twistPoseGrp = (muscleName + '_' + longList[i] + '_' + latList[j] + '_' + 
					twistList[k] + '_grp')

				attachTargetName = (muscleName + '_attachRest' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
				
				# Create transform group for attach rest curve
				twistPoseTransGrp = attachTargetName + '_grp'
				mc.group(
					empty=True,
					name=twistPoseTransGrp,
					parent=twistPoseGrp)
				
				mc.parentConstraint(
					attachRestList[r], 
					twistPoseTransGrp,
					maintainOffset=False,
					n='tempParentConstraint')
					
				mc.delete('tempParentConstraint')
				
				lockTransforms(
					twistPoseTransGrp,
					'all')

				# Duplicate attach rest curves
				mc.duplicate(
					attachRestList[r], 
					n=attachTargetName)
				
				# Delete the child squash and stretch curves 
				mc.delete(
					mc.listRelatives(
						attachTargetName, 
						type='transform', 
						path=True))
				
				# Unlock transforms for reparenting
				unlockCS(attachTargetName)
			
				mc.parent(
					attachTargetName, 
					twistPoseTransGrp)
				
				lockTransforms(
					attachTargetName,
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
					attachTargetName)
				
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


	# Create blend shapes and connect to driver (for twist 0)

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
				
				
				# ATTACH REST POINTS
				attachTargetName = (muscleName + '_attachRest' + str(r + 1) + '_' + 
					longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')
			
				attachRest = attachRestList[r]
			
				# pointConstraintName = attachRest + '_pointConstraint1'
			
				# Create point constraints
				
				mc.pointConstraint(
					attachTargetName, 
					attachRest, 
					weight=0.0)
				# Connect driver outputs to point constraint
				mc.connectAttr(
					muscleShapeDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
						twistList[k], 
					attachRest + '_pointConstraint1.' + attachTargetName + 'W' + str(pIndex))
				pIndex += 1
				




# Muscle 1
muscleName1 = 'L_pectoralisMajorUpper'
muscleNode1 = 'cMuscleCreatorMus_L_pectoralisMajorUpper1'
crossSectionList1 = [
	'iControlMidMus_L_pectoralisMajorUpper11_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorUpper21_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorUpper31_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorUpper41_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorUpper51_crossSectionREST']
attachRestList1 = [
	'AttachMidMus_L_pectoralisMajorUpper11', 
	'AttachMidMus_L_pectoralisMajorUpper21', 
	'AttachMidMus_L_pectoralisMajorUpper31', 
	'AttachMidMus_L_pectoralisMajorUpper41', 
	'AttachMidMus_L_pectoralisMajorUpper51']

# Muscle 2
muscleName2 = 'L_pectoralisMajorMid'
muscleNode2 = 'cMuscleCreatorMus_L_pectoralisMajorMid1'
crossSectionList2 = [
	'iControlMidMus_L_pectoralisMajorMid11_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorMid21_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorMid31_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorMid41_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorMid51_crossSectionREST']
attachRestList2 = [
	'AttachMidMus_L_pectoralisMajorMid11', 
	'AttachMidMus_L_pectoralisMajorMid21', 
	'AttachMidMus_L_pectoralisMajorMid31', 
	'AttachMidMus_L_pectoralisMajorMid41', 
	'AttachMidMus_L_pectoralisMajorMid51']

# Muscle 3
muscleName3 = 'L_pectoralisMajorLower'
muscleNode3 = 'cMuscleCreatorMus_L_pectoralisMajorLower1'
crossSectionList3 = [
	'iControlMidMus_L_pectoralisMajorLower11_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLower21_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLower31_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLower41_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLower51_crossSectionREST']
attachRestList3 = [
	'AttachMidMus_L_pectoralisMajorLower11', 
	'AttachMidMus_L_pectoralisMajorLower21', 
	'AttachMidMus_L_pectoralisMajorLower31', 
	'AttachMidMus_L_pectoralisMajorLower41', 
	'AttachMidMus_L_pectoralisMajorLower51']

# Muscle 4
muscleName4 = 'L_pectoralisMajorLowerB'
muscleNode4 = 'cMuscleCreatorMus_L_pectoralisMajorLowerB1'
crossSectionList4 = [
	'iControlMidMus_L_pectoralisMajorLowerB11_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLowerB21_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLowerB31_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLowerB41_crossSectionREST',
	'iControlMidMus_L_pectoralisMajorLowerB51_crossSectionREST']
attachRestList4 = [
	'AttachMidMus_L_pectoralisMajorLowerB11', 
	'AttachMidMus_L_pectoralisMajorLowerB21', 
	'AttachMidMus_L_pectoralisMajorLowerB31', 
	'AttachMidMus_L_pectoralisMajorLowerB41', 
	'AttachMidMus_L_pectoralisMajorLowerB51']





makeMusclePoseSys(muscleName1, muscleNode1, crossSectionList1, attachRestList1)
# makeMusclePoseSys(muscleName2, muscleNode2, crossSectionList2, attachRestList2)
# makeMusclePoseSys(muscleName3, muscleNode3, crossSectionList3, attachRestList3)
# makeMusclePoseSys(muscleName4, muscleNode4, crossSectionList4, attachRestList4)




print '\r\rScript completed successfully\r\r'
