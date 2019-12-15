# N3 biceps brachii flex.py
# Created by Laushon Neferkara on 4/13/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

 
# Import function module
import nm

def main():
	muscleName = 'L_bicepsBrachii'
	muscleNode = 'cMuscleCreatorMus_L_bicepsBrachii1'
	topPoseGrp = 'muscle_pose_grp'
	muscleDriver = 'N3_upperArm_driver'
	controlIndexList = [1, 2, 3, 4, 5, 6]

	# Attribute lists
	flexList = [
		'a0', 'a45', 'a90', 'a135', 'a150']
	proList = [
		'b0', 'b140']

	# Pose values
	flexes = [
		0, 45, 90, 135, 150]

	pros = [
		0, 140]


	# Set Based On attribute to pose
	mc.setAttr(muscleNode + '.basedOn', 1)


	# Create groups to hold poses
	def createPoseGrps():
		mainPoseGrp = muscleName + '_flex_pose_grp'
		nm.makeSimpleGrp(mainPoseGrp, topPoseGrp)

		for flex in flexList: 
			flexPoseGrp = muscleName + '_' + flex + '_grp'
			nm.makeSimpleGrp(flexPoseGrp, mainPoseGrp)

			for pro in proList:
				proPoseGrp = muscleName + '_' + flex + '_' + pro + '_grp'
				nm.makeSimpleGrp(proPoseGrp, flexPoseGrp)

				mc.setAttr(proPoseGrp + '.visibility', False)

				for cIndex in controlIndexList:
					crossSectionPoseGrp = (muscleName + '_' + flex + '_' + pro +
						'_crossSection%s' % str(cIndex) + '_grp')
					mc.group(em=True, r=True, n=crossSectionPoseGrp)
					mc.parent(crossSectionPoseGrp, proPoseGrp)

					# Constrain crossSectionPoseGrp to crossSectionPoseGrpTarget to get auto movement
					crossSectionPoseGrpTarget = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex))

					mc.parentConstraint(
						crossSectionPoseGrpTarget, 
						crossSectionPoseGrp, 
						maintainOffset=False)

	# Make poses
	def createPoses():
		for flex in flexList: 
			for pro in proList:
				for cIndex in controlIndexList:
					crossSectionPoseGrp = (muscleName + '_' + flex + '_' + pro +
						'_crossSection%s' % str(cIndex) + '_grp')

					# Duplicate cross sections
					targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
						flex + '_' + pro + '_target')
		
					mc.duplicate(
						'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex)),  
						n=targetName)
		
					# The original cross section has locked transforms. Unlike befor parenting.
					nm.unlockCS(targetName)
			
					# Freeze transforms
					mc.makeIdentity(targetName, apply=True, rotate=True)
			
					# Lock unused transforms
					nm.lockTransforms(targetName, 'all')


	# Connect to driver
	def connectDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			for flex in flexList: 
				for pro in proList:
					# CROSS SECTIONS
					targetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
						flex + '_' + pro + '_target')
		
					# crossSection = crossSectionList[r]
					crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex))
					blendShapeNode = crossSection + '_blendShape'
		
					# Create blend shape node with 1st target. 
					# Add to blend shape node for additional targets.
					if flex == flexList[0] and pro == proList[0]:
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
						muscleDriver + '.' + flex + '_' + pro, 
						blendShapeNode + '.' + targetName)
				

				
	createPoseGrps()
	createPoses()
	connectDriver()			


if __name__ == '__main__':
	scriptName = 'N3 biceps brachii.py'
	print '\r' + scriptName + ' running'
	main()
	print '\r\r' + scriptName + ' completed Successfully\r\r'
