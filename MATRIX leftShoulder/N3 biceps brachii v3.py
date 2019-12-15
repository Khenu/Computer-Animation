# N3 biceps brachii v3.py
# Created by Laushon Neferkara on 4/13/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Create poseMatrix to control L_biceps_origin_ctrl

# 
# # Import function module
# import nm

# Create simple group
def makeSimpleGrp(grpName, parent):
	hideList = [
		'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ']

	mc.group(em=True, r=True, n=grpName)

	for hidden in hideList:
		mc.setAttr(
			grpName + '.' + hidden, 
			keyable=False, 
			lock=True, 
			cb=False)

	mc.parent(grpName, parent)


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
		mc.setAttr(node + '.' + attr, lock=True)


# Unlock cross section
def unlockCS(node):
	attrList = [
		'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ']

	for attr in attrList:
		mc.setAttr(node + '.' + attr, lock=False)

	visibility = node + '.visibility'

	mc.setAttr(
		visibility, 
		keyable=True)	

	if mc.connectionInfo(visibility, isDestination=True):
		source = mc.connectionInfo(visibility, sourceFromDestination=True)
		mc.disconnectAttr(
			source, 
			visibility)


def main():
	muscleName = 'L_bicepsBrachii'
	muscleNode = 'cMuscleCreatorMus_L_bicepsBrachii1'
	topPoseGrp = 'muscle_pose_grp'
	muscleDriver = 'N3_muscleShape_driver'
	controlIndexList = [1, 2, 3, 4, 5, 6]

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
	

	# Set Based On attribute to pose
	mc.setAttr(muscleNode + '.basedOn', 1)

	
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


	# Make poses for twist 0
	def createPoses():
		for long in longList: 
			for lat in latList:
				twist = twistList[2]
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


	# Connect to driver twist = 0 set
	def connectDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			for long in longList: 
				for lat in latList:
					twist = twistList[2]
				
					# CONTROLS
					controlTargetName = (muscleName + '_control' + str(cIndex) + '_' + 
						long + '_' + lat + '_' + twist + '_target')
					control = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex))
		
					# Create point constraints				
					mc.pointConstraint(
						controlTargetName, 
						control, 
						weight=0.0)

					# Connect driver outputs to point constraint
					mc.connectAttr(
						muscleDriver + '.' + long + '_' + lat + '_' + twist, 
						control + '_pointConstraint1.' + controlTargetName + 'W' + str(pIndex))
					pIndex += 1

				

				
	createPoseGrps()
	createPoses()
	connectDriver()			


if __name__ == '__main__':
	scriptName = 'N3 biceps brachii v3.py'
	print '\r' + scriptName + ' running'
	main()
	print '\r\r' + scriptName + ' completed Successfully\r\r'
