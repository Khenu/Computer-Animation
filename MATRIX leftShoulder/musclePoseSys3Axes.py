# musclePoseSys3Axes.py
# Created by Laushon Neferkara on 5/3/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Import function module
from nm import *
	

def create(
	muscleName, 
	controlIndexList, 
	muscleDriver, 
	longList, 
	latList, 
	twistList,
	longitudes, 
	latitudes, 
	twists, 
	topPoseGrp):
	
	
	# Set Based On attribute to pose
	mc.setAttr('cMuscleCreatorMus_%s1.basedOn' % muscleName, 1)	

	# Create groups to hold poses
	def createPoseGrps():
		mainPoseGrp = muscleName + '_pose_grp'
		makeSimpleGrp(mainPoseGrp, topPoseGrp)
	
		for long in longList: 
			longPoseGrp = muscleName + '_' + long + '_grp'
			makeSimpleGrp(longPoseGrp, mainPoseGrp)

			for lat in latList:
				latPoseGrp = muscleName + '_' + long + '_' + lat + '_grp'
				makeSimpleGrp(latPoseGrp, longPoseGrp)

				for twist in twistList:
					twistPoseGrp = muscleName + '_' + long + '_' + lat + '_' + twist + '_grp'
					makeSimpleGrp(twistPoseGrp, latPoseGrp)
					mc.setAttr(twistPoseGrp + '.visibility', False)

					for cIndex in controlIndexList:
						controlPoseGrp = (muscleName + '_' + long + '_' + lat + '_' + twist +
							'_control%s' % str(cIndex) + '_grp')
						mc.group(em=True, r=True, n=controlPoseGrp)
						mc.parent(controlPoseGrp, twistPoseGrp)

						# Constrain controlPoseGrp to controlPoseGrpTarget to get auto movement
						controlPoseGrpTarget = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex))

						mc.parentConstraint(
							controlPoseGrpTarget, 
							controlPoseGrp, 
							maintainOffset=False)

	
	# Make poses
	def createPoses():
		for long in longList: 
			for lat in latList:
				for twist in twistList:
					for cIndex in controlIndexList:
						controlPoseGrp = (muscleName + '_' + long + '_' + lat + '_' + twist +
							'_control%s' % str(cIndex) + '_grp')
						controlTargetName = (muscleName + '_control%s' % str(cIndex) + '_' + 
							long + '_' + lat + '_' + twist + '_target')

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
						unlockCS(controlTargetName)
			
						mc.parent(controlTargetName, controlPoseGrp)
				
						# Lock unused transforms
						lockTransforms(controlTargetName, 'rotate, scale')

						# Duplicate cross sections
						targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
							long + '_' + lat + '_' + twist + '_target')
			
						mc.duplicate(
							'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex)),  
							n=targetName)
			
						# The original cross section has locked transforms. Unlike befor parenting.
						unlockCS(targetName)
				
						# Parent target to 
						mc.parent(targetName, controlTargetName)
				
						# Freeze transforms
						mc.makeIdentity(targetName, apply=True, rotate=True)
				
						# Lock unused transforms
						lockTransforms(targetName, 'all')


	# Connect to driver
	def connectDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			for i in range(len(longList)): 
				for j in range(len(latList)):
					for m in range(len(twistList)):				

						# CONTROLS
						controlTargetName = (muscleName + '_control' + str(cIndex) + '_' + 
							longList[i] + '_' + latList[j] + '_' + twistList[m] + '_target')
						control = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex))
			
						# Create point constraints				
						mc.pointConstraint(
							controlTargetName, 
							control, 
							weight=0.0)

						# Connect driver outputs to point constraint
						mc.connectAttr(
							muscleDriver + '.' + longList[i] + '_' + latList[j] + '_' + twistList[m], 
							control + '_pointConstraint1.' + controlTargetName + 'W' + str(pIndex))
						pIndex += 1

						# CROSS SECTIONS
						targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
							longList[i] + '_' + latList[j] + '_' + twistList[m] + '_target')
			
						# crossSection = crossSectionList[r]
						crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex))
						blendShapeNode = crossSection + '_blendShape'
			
						# Create blend shape node with 1st target. 
						# Add to blend shape node for additional targets.
						if i == 0 and j == 0 and m == 0:
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
							muscleDriver + '.' + longList[i] + '_' + latList[j] + '_' + twistList[m], 
							blendShapeNode + '.' + targetName)
				
	createPoseGrps()
	createPoses()
	connectDriver()			
