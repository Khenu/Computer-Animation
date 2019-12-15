# N3 muscle pose system v4.py
# Created by Laushon Neferkara on 3/28/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# 1. Set Based On attribute to pose
# 2. Duplicate cross sections
# 3. Unlock attributes
# 4. Parent cross section targets to pose group
# 5. Create blend shape node
# 6. Connect driver outputs to blend shape node



scriptName = 'N3 muscle pose system v4.py'
print '\r' + scriptName + ' running'




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


	# 1. Set Based On attribute to pose
	mc.setAttr(muscleNode + '.basedOn', 1)

	
	# Create reference poses
	
	# Create reference pose groups
	refPoseGrp = muscleName + '_ref_pose_grp'
	makeSimpleGrp(refPoseGrp, muscleRefGrp)
	for long in longList: 
		longPoseGrp = muscleName + '_' + long + '_ref_grp'
		makeSimpleGrp(longPoseGrp, refPoseGrp)
		for lat in latList:
			latPoseGrp = muscleName + '_' + long + '_' + lat + '_ref_grp'
			makeSimpleGrp(latPoseGrp, longPoseGrp)
			for twist in twistList:
				twistPoseGrp = muscleName + '_' + long + '_' + lat + '_' + twist + '_ref_grp'
				makeSimpleGrp(twistPoseGrp, latPoseGrp)
				#
				mc.setAttr(
					twistPoseGrp + '.visibility', 
					False)
	
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



	################
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


	# 5. Create blend shapes and connect to driver (for twist 0)

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
muscleName1 = 'L_deltoidAnterior'
muscleNode1 = 'cMuscleCreatorMus_deltoid_B1'
crossSectionList1 = [
	'iControlMidMus_deltoid_B11_crossSectionREST',
	'iControlMidMus_deltoid_B21_crossSectionREST',
	'iControlMidMus_deltoid_B31_crossSectionREST',
	'iControlMidMus_deltoid_B41_crossSectionREST',
	'iControlMidMus_deltoid_B51_crossSectionREST']
attachRestList1 = [
	'AttachMidMus_deltoid_B11', 
	'AttachMidMus_deltoid_B21', 
	'AttachMidMus_deltoid_B31', 
	'AttachMidMus_deltoid_B41', 
	'AttachMidMus_deltoid_B51']


# Muscle 2
muscleName2 = 'L_deltoidLateral'
muscleNode2 = 'cMuscleCreatorMus_L_deltoidLateral1'
crossSectionList2 = [
	'iControlMidMus_L_deltoidLateral11_crossSectionREST',
	'iControlMidMus_L_deltoidLateral21_crossSectionREST',
	'iControlMidMus_L_deltoidLateral31_crossSectionREST',
	'iControlMidMus_L_deltoidLateral41_crossSectionREST',
	'iControlMidMus_L_deltoidLateral51_crossSectionREST', 
	'iControlMidMus_L_deltoidLateral61_crossSectionREST', 
	'iControlMidMus_L_deltoidLateral71_crossSectionREST']
attachRestList2 = [
	'AttachMidMus_L_deltoidLateral11', 
	'AttachMidMus_L_deltoidLateral21', 
	'AttachMidMus_L_deltoidLateral31', 
	'AttachMidMus_L_deltoidLateral41', 
	'AttachMidMus_L_deltoidLateral51', 
	'AttachMidMus_L_deltoidLateral61', 
	'AttachMidMus_L_deltoidLateral71']

# Muscle 3
muscleName3 = 'L_deltoidPosterior2A'
muscleNode3 = 'cMuscleCreatorMus_L_deltoidPosterior2A1'
crossSectionList3 = [
	'iControlMidMus_L_deltoidPosterior2A11_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2A21_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2A31_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2A41_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2A51_crossSectionREST']
attachRestList3 = [
	'AttachMidMus_L_deltoidPosterior2A11', 
	'AttachMidMus_L_deltoidPosterior2A21', 
	'AttachMidMus_L_deltoidPosterior2A31', 
	'AttachMidMus_L_deltoidPosterior2A41', 
	'AttachMidMus_L_deltoidPosterior2A51']

# Muscle 4
muscleName4 = 'L_deltoidPosterior2B'
muscleNode4 = 'cMuscleCreatorMus_L_deltoidPosterior2B1'
crossSectionList4 = [
	'iControlMidMus_L_deltoidPosterior2B11_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2B21_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2B31_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2B41_crossSectionREST',
	'iControlMidMus_L_deltoidPosterior2B51_crossSectionREST']
attachRestList4 = [
	'AttachMidMus_L_deltoidPosterior2B11', 
	'AttachMidMus_L_deltoidPosterior2B21', 
	'AttachMidMus_L_deltoidPosterior2B31', 
	'AttachMidMus_L_deltoidPosterior2B41', 
	'AttachMidMus_L_deltoidPosterior2B51']


# Muscle 5
muscleName5 = 'L_tricepsLong'
muscleNode5 = 'cMuscleCreatorMus_L_tricepsLongB1'
crossSectionList5 = [
	'iControlMidMus_L_tricepsLongB11_crossSectionREST',
	'iControlMidMus_L_tricepsLongB21_crossSectionREST',
	'iControlMidMus_L_tricepsLongB31_crossSectionREST',
	'iControlMidMus_L_tricepsLongB41_crossSectionREST',
	'iControlMidMus_L_tricepsLongB51_crossSectionREST',
	'iControlMidMus_L_tricepsLongB61_crossSectionREST',
	'iControlMidMus_L_tricepsLongB71_crossSectionREST']
attachRestList5 = [
	'AttachMidMus_L_tricepsLongB11', 
	'AttachMidMus_L_tricepsLongB21', 
	'AttachMidMus_L_tricepsLongB31', 
	'AttachMidMus_L_tricepsLongB41', 
	'AttachMidMus_L_tricepsLongB51', 
	'AttachMidMus_L_tricepsLongB61', 
	'AttachMidMus_L_tricepsLongB71']

# Muscle 6
muscleName6 = 'L_tricepsLateral'
muscleNode6 = 'cMuscleCreatorMus_L_tricepsLateralC1'
crossSectionList6 = [
	'iControlMidMus_L_tricepsLateralC11_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC21_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC31_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC41_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC51_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC61_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC71_crossSectionREST',
	'iControlMidMus_L_tricepsLateralC81_crossSectionREST']
attachRestList6 = [
	'AttachMidMus_L_tricepsLateralC11', 
	'AttachMidMus_L_tricepsLateralC21', 
	'AttachMidMus_L_tricepsLateralC31', 
	'AttachMidMus_L_tricepsLateralC41', 
	'AttachMidMus_L_tricepsLateralC51', 
	'AttachMidMus_L_tricepsLateralC61', 
	'AttachMidMus_L_tricepsLateralC71', 
	'AttachMidMus_L_tricepsLateralC81']





# Muscle 7
muscleName7 = 'L_teresMajor'
muscleNode7 = 'cMuscleCreatorMus_L_teresMajor1'
crossSectionList7 = [
	'iControlMidMus_L_teresMajor11_crossSectionREST',
	'iControlMidMus_L_teresMajor21_crossSectionREST',
	'iControlMidMus_L_teresMajor31_crossSectionREST',
	'iControlMidMus_L_teresMajor41_crossSectionREST',
	'iControlMidMus_L_teresMajor51_crossSectionREST']








# makeMusclePoseSys(muscleName1, muscleNode1, crossSectionList1, attachRestList1)
# makeMusclePoseSys(muscleName2, muscleNode2, crossSectionList2, attachRestList2)
# makeMusclePoseSys(muscleName3, muscleNode3, crossSectionList3, attachRestList3)
# makeMusclePoseSys(muscleName4, muscleNode4, crossSectionList4, attachRestList4)
makeMusclePoseSys(muscleName5, muscleNode5, crossSectionList5, attachRestList5)
# makeMusclePoseSys(muscleName6, muscleNode6, crossSectionList6, attachRestList6)
# makeMusclePoseSys(muscleName7, muscleNode7, crossSectionList7)




print '\r\r' + scriptName + ' completed successfully\r\r'
