# N3PectoralisMajorPoses4.py
# Created by Laushon Neferkara on 9/3/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Add twist poses
# Reduced axis 2 to 0, 90, 170

# Import function module
import nm

def makePoses(muscleName, controlIndexList, driverData, driverData2):

	topPoseGrp = 'muscle_pose_grp'
	
	# Set Based On attribute to pose
	mc.setAttr('cMuscleCreatorMus_%s1.basedOn' % muscleName, 1)	

	def createPoseGrps():
		'''Create additional twist groups'''
		for axis1Point in driverData['axis1Pts']: 
			for axis2Point in driverData['axis2Pts']:
				for axis3Point in driverData['axis3Pts']:
					poseGrp = '%s_%s_%s_%s_grp' % (muscleName, axis1Point, axis2Point, axis3Point)
					parentGrp = '%s_%s_%s_grp' % (muscleName, axis1Point, axis2Point)
					nm.makeSimpleGrp(poseGrp, parentGrp)
					mc.setAttr(poseGrp + '.visibility', False)
					for cIndex in controlIndexList:
						controlPoseGrp = poseGrp.replace('_grp', '_control%s_grp' % str(cIndex))
						mc.group(em=True, r=True, n=controlPoseGrp)
						mc.parent(controlPoseGrp, poseGrp)
						# Constrain controlPoseGrp to controlPoseGrpTarget to get auto movement
						controlPoseGrpTarget = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex))
						mc.parentConstraint(controlPoseGrpTarget, controlPoseGrp, maintainOffset=False)

	
	def createPoses():
		'''Create additional poses'''
		for axis1Point in driverData['axis1Pts']: 
			for axis2Point in driverData['axis2Pts']:
				for axis3Point in driverData['axis3Pts']:
					for cIndex in controlIndexList:
						controlPoseGrp = '%s_%s_%s_%s_control%s_grp' % (muscleName, axis1Point, axis2Point, axis3Point, str(cIndex))
						controlTargetName = '%s_control%s_%s_%s_%s_target' % (muscleName, str(cIndex), axis1Point, axis2Point, axis3Point)
						
						# Duplicate _w0 target
						# mc.duplicate('iControlMidMus_%s%s1' % (muscleName, str(cIndex)), n=controlTargetName)
						mc.duplicate('%s_control%s_%s_%s_w0_target' % (muscleName, str(cIndex), axis1Point, axis2Point),
							 n=controlTargetName)
						# Unlock transforms for reparenting
						nm.unlockCS(controlTargetName)
						# parent
						mc.parent(controlTargetName, controlPoseGrp)
						# Lock unused transforms
						nm.lockTransforms(controlTargetName, 'rotate, scale')

						# Rename cross section target
						mc.rename('%s|%s_crossSection%s_%s_%s_w0_target' % (controlTargetName, muscleName, str(cIndex), axis1Point, axis2Point),
							'%s_crossSection%s_%s_%s_%s_target' % (muscleName, str(cIndex), axis1Point, axis2Point, axis3Point))


	
	def delExTargetConnections():
		for cIndex in controlIndexList:
			mc.delete('iControlMidMus_%s%s1_pointConstraint1' % (muscleName, str(cIndex)))
			mc.delete('iControlMidMus_%s%s1_crossSectionREST_blendShape' % (muscleName, str(cIndex)))


	# Connect to driver wFlexes = 0 set
	def connectDriver():
		for cIndex in controlIndexList:
			pIndex = 0
			i = 0
			# for i in range(len(flexList)): 
			for axis1Point in driverData2['axis1Pts']: 
				for axis2Point in driverData2['axis2Pts']:
					for axis3Point in driverData2['axis3Pts']:

						# CONTROLS
						controlTargetName = '%s_control%s_%s_%s_%s_target' % (muscleName, str(cIndex), axis1Point, axis2Point, axis3Point)
						control = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex))
						# Create point constraints				
						mc.pointConstraint(controlTargetName, control, weight=0.0)
						# Connect driver outputs to point constraint
						mc.connectAttr(
							'%s.%s_%s_%s' % (driverData2['driverName'], axis1Point, axis2Point, axis3Point), 
							'%s_pointConstraint1.%sW%s' % (control, controlTargetName, str(pIndex)))
						pIndex += 1

						# CROSS SECTIONS
						targetName = '%s_crossSection%s_%s_%s_%s_target' % (muscleName, str(cIndex), axis1Point, axis2Point, axis3Point)
						crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscleName, str(cIndex))
						blendShapeNode = '%s_blendShape' % crossSection
				
						# Create blend shape node with 1st target. 
						# Add to blend shape node for additional targets.

						if i == 0:
							mc.blendShape(
								targetName, 
								crossSection, 
								name = blendShapeNode)
							bIndex = 1
							i = 1
						else:
							mc.blendShape(
								blendShapeNode, 
								edit=True, 
								t=(crossSection, bIndex, targetName, 1.0))
							bIndex += 1
				
						# Connect driver outputs to blend shape node
						mc.connectAttr(
							'%s.%s_%s_%s' % (driverData2['driverName'], axis1Point, axis2Point, axis3Point), 
							'%s.%s' % (blendShapeNode, targetName))
				
	createPoseGrps()
	createPoses()
	delExTargetConnections()
	connectDriver()			



def main():
	
	muscleName1 = 'L_pectoralisMajorUpper'
	controlIndexList1 = [1, 2, 3, 4, 5]

	muscleName2 = 'L_pectoralisMajorMid'
	controlIndexList2 = [1, 2, 3, 4, 5]

	muscleName3 = 'L_pectoralisMajorLower'
	controlIndexList3 = [1, 2, 3, 4, 5]

	muscleName4 = 'L_pectoralisMajorLowerB'
	controlIndexList4 = [1, 2, 3, 4, 5]
	
	muscleName5 = 'L_deltoidAnterior'
	controlIndexList5 = [1, 2, 3, 4, 5]

	muscleName6 = 'L_deltoidLateral'
	controlIndexList6 = [1, 2, 3, 4, 5, 6, 7]

	muscleName7 = 'L_deltoidPosterior2A'
	controlIndexList7 = [1, 2, 3, 4, 5]

	muscleName8 = 'L_deltoidPosterior2B'
	controlIndexList8 = [1, 2, 3, 4, 5]

	driverData = {
		'driverName'	: 	'N3_muscleDriver2', 
		'axis1Name'		: 	'N3_humerus_long_data2', 
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Name'		: 	'N3_biceps_lat_data', 
		'axis2Pts'		: 	('y0', 'y90', 'y170'), 
		'axis3Name'		: 	'N3_biceps_twist_data',	
		'axis3Pts'		: 	('w90', 'wn90')					# Without w0
		}
	
	driverData2 = {
		'driverName'	: 	'N3_muscleDriver2', 
		'axis1Name'		: 	'N3_humerus_long_data2', 
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Name'		: 	'N3_biceps_lat_data', 
		'axis2Pts'		: 	('y0', 'y90', 'y170'), 
		'axis3Name'		: 	'N3_biceps_twist_data',	
		'axis3Pts'		: 	('w0', 'w90', 'wn90')	
		}

	makePoses(muscleName8, controlIndexList8, driverData, driverData2)

	print '\r\rScript completed successfully\r\r'



if __name__ == "__main__":
	main()
	










