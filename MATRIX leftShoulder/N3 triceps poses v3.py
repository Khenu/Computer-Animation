# N3 triceps poses v3.py
# Created by Laushon Neferkara on 5/1/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.


def main(muscleName, controlIndexList):
	# Attribute lists
	flexList = [
		'a0', 'a45', 'a90', 'a135', 'a150']

	# Pose values
	flexes = [
		0, 45, 90, 135, 150]


	topPoseGrp = 'muscle_pose_grp'
	muscleDriver = 'N3_triceps_driver'
	


	# Set Based On attribute to pose
	mc.setAttr('cMuscleCreatorMus_%s1.basedOn' % muscleName, 1)	

	# Create groups to hold poses
	def createPoseGrps():
		mainPoseGrp = muscleName + '_pose_grp'
		nm.makeSimpleGrp(mainPoseGrp, topPoseGrp)
	
		for flex in flexList: 
			flexPoseGrp = muscleName + '_' + flex + '_grp'
			nm.makeSimpleGrp(flexPoseGrp, mainPoseGrp)
			mc.setAttr(flexPoseGrp + '.visibility', False)

			for cIndex in controlIndexList:
				controlPoseGrp = (muscleName + '_' + flex + '_control%s' % str(cIndex) + '_grp')
				mc.group(em=True, r=True, n=controlPoseGrp)
				mc.parent(controlPoseGrp, flexPoseGrp)

				# Constrain controlPoseGrp to controlPoseGrpTarget to get auto movement
				controlPoseGrpTarget = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex))

				mc.parentConstraint(
					controlPoseGrpTarget, 
					controlPoseGrp, 
					maintainOffset=False)

	
	# Make poses
	def createPoses():
		for flex in flexList: 
			for cIndex in controlIndexList:
				controlPoseGrp = (muscleName + '_' + flex + '_control%s' % str(cIndex) + '_grp')
				controlTargetName = (muscleName + '_control%s' % str(cIndex) + '_' + 
					flex + '_target')

				# Duplicate muscle control
				mc.duplicate(
					'iControlMidMus_%s%s1' % (muscleName, str(cIndex)),
					n=controlTargetName)
			
				# Delete the child squash and stretch curves 
				mc.delete(
					mc.listRelatives(
						controlTargetName, 
						type='transform', 
						path=True))
			
				# Unlock transforms for reparenting
				nm.unlockCS(controlTargetName)
		
				mc.parent(controlTargetName, controlPoseGrp)
			
				# Lock unused transforms
				nm.lockTransforms(controlTargetName, 'rotate, scale')

				# Duplicate cross sections
				targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
					flex + '_target')
		
				mc.duplicate(
					'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex)),  
					n=targetName)
		
				# The original cross section has locked transforms. Unlike befor parenting.
				nm.unlockCS(targetName)
			
				# Parent target to 
				mc.parent(targetName, controlTargetName)
			
				# Freeze transforms
				mc.makeIdentity(targetName, apply=True, rotate=True)
			
				# Lock unused transforms
				nm.lockTransforms(targetName, 'all')


	# Connect to driver wFlexes = 0 set
	def connectDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			for i in range(len(flexList)): 
			
				# CONTROLS
				controlTargetName = (muscleName + '_control' + str(cIndex) + '_' + 
					flexList[i] + '_target')
				control = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex))
		
				# Create point constraints				
				mc.pointConstraint(
					controlTargetName, 
					control, 
					weight=0.0)

				# Connect driver outputs to point constraint
				mc.connectAttr(
					muscleDriver + '.' + flexList[i], 
					control + '_pointConstraint1.' + controlTargetName + 'W' + str(pIndex))
				pIndex += 1

				# CROSS SECTIONS
				targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
					flexList[i] + '_target')
		
				# crossSection = crossSectionList[r]
				crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex))
				blendShapeNode = crossSection + '_blendShape'
		
				# Create blend shape node with 1st target. 
				# Add to blend shape node for additional targets.
				if i == 0:
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
					muscleDriver + '.' + flexList[i], 
					blendShapeNode + '.' + targetName)
				
	createPoseGrps()
	createPoses()
	connectDriver()			




if __name__ == "__main__":
	
	muscleName1 = 'L_tricepsBrachiiMedial'
	controlIndexList1 = [1, 2, 3, 4, 5, 6]

	main(muscleName1, controlIndexList1)


print '\r\rCompleted successfully\r\r'











