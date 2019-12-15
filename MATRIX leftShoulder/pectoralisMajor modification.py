# 1. Delete the attach point point constraint. 
# 2. Create control targets. 
# 3. Translate the control targets to the old attach targets. 
# 4. Parent the existing cross section targets to the new control targets. 
# 5. Delete the old attach targets. 
# 6. Create new control point constraint. 


# Import function module
import nm
	

def main(muscleName, controlIndexList):
	# Character controls
	longCtrl = 'L_arm_ctrl.rotateY'
	latCtrl = 'L_arm_ctrl.rotateX' # neg values

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

	topPoseGrp = 'muscle_pose_grp'
	muscleDriver = 'N3_muscleShape_driver'
	

	# 1. Delete the attach point point constraint. 
	def deleteAttachConstraints():
		for i in controlIndexList:
			mc.delete('AttachMidMus_%s%s1_pointConstraint1' % (muscleName, str(i)))

	# Create groups to hold poses
	def createPoseGrps():
		mainPoseGrp = muscleName + '_pose_grp'
		nm.makeSimpleGrp(mainPoseGrp, topPoseGrp)
	
		for long in longList: 
			longPoseGrp = muscleName + '_' + long + '_grp'
			nm.makeSimpleGrp(longPoseGrp, mainPoseGrp)

			for lat in latList:
				latPoseGrp = muscleName + '_' + long + '_' + lat + '_grp'
				nm.makeSimpleGrp(latPoseGrp, longPoseGrp)

				for twist in twistList:
					twistPoseGrp = muscleName + '_' + long + '_' + lat + '_' + twist + '_grp'
					nm.makeSimpleGrp(twistPoseGrp, latPoseGrp)
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

	
	# 2. Create control targets. 
	def createPoses():
		for i in range(len(longList)): 
			mc.setAttr(longCtrl, longitudes[i])
			for j in range(len(latList)):
				mc.setAttr(latCtrl, -latitudes[j])
				twist = 'w0'
				for cIndex in controlIndexList:
					controlPoseGrp = (muscleName + '_' + longList[i] + '_' + latList[j] + '_' + twist +
						'_control%s' % str(cIndex) + '_grp')
					controlTargetName = (muscleName + '_control%s' % str(cIndex) + '_' + 
						longList[i] + '_' + latList[j] + '_' + twist + '_target')

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

					# 3. Translate the control targets to the old attach targets. 
					attachTargetName = (muscleName + '_attachRest' + str(cIndex) + '_' + 
							longList[i] + '_' + latList[j] + '_' + twist + '_target')
					mc.pointConstraint(
						attachTargetName, 
						controlTargetName, 
						maintainOffset=False,
						name='tempPointConstraint')
					mc.delete('tempPointConstraint')
					
					# 4. Parent the existing cross section targets to the new control targets.
					csTargetName = (muscleName + '_crossSection' + str(cIndex) + '_' + 
						longList[i] + '_' + latList[j] + '_' + twist + '_target')
		
					# The cross sections have locked transforms. Unlike befor parenting.
					nm.unlockCS(csTargetName)
					
					# Parent target to 
					mc.parent(csTargetName, controlTargetName)
			
					# Freeze transforms
					mc.makeIdentity(csTargetName, apply=True, rotate=True)
			
					# Lock unused transforms
					nm.lockTransforms(csTargetName, 'all')

					# 5. Delete the old attach targets. 
					mc.delete(attachTargetName)
		# Move the arm control back to home position.					
		mc.setAttr(longCtrl, 0)
		mc.setAttr(latCtrl, 0)


	# 6. Create new control point constraint.
	def connectToDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			for i in range(len(longList)): 
				for j in range(len(latList)):
					k = 2
				
					# CONTROLS
					controlTargetName = (muscleName + '_control' + str(cIndex) + '_' + 
						longList[i] + '_' + latList[j] + '_' + twistList[k] + '_target')

					control = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex))
			
					# Create point constraints				
					mc.pointConstraint(
						controlTargetName, 
						control, 
						weight=0.0)

					# Connect driver outputs to point constraint
					mc.connectAttr(
						muscleDriver + '.' + longList[i] + '_' + latList[j] + '_' + 
							twistList[k], 
						control + '_pointConstraint1.' + controlTargetName + 'W' + str(pIndex))
					pIndex += 1

			
	createPoseGrps()
	deleteAttachConstraints()
	createPoses()
	connectToDriver()


if __name__ == "__main__":
	
	# Muscle 1
	muscleName1 = 'L_pectoralisMajorUpper'
	controlIndexList1 = [1, 2, 3, 4, 5]

	# Muscle 2
	muscleName2 = 'L_pectoralisMajorMid'
	controlIndexList2 = [1, 2, 3, 4, 5]
	
	# Muscle 3
	muscleName3 = 'L_pectoralisMajorLower'
	controlIndexList3 = [1, 2, 3, 4, 5]

	# Muscle 4
	muscleName4 = 'L_pectoralisMajorLowerB'
	controlIndexList4 = [1, 2, 3, 4, 5]
	
	# Run one muscle at a time. Edit parameter below.
	main(muscleName4, controlIndexList1)


