# N3TeresMajorPosesChange.py
# Created by Laushon Neferkara on 9/10/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Reduce the number of poses. Drive with N3_muscleDriver3.

# Import function module
import nm

def drivePoses(muscleData, driverData):
	
	def delExTargetConnections():
		for cIndex in range(1, muscleData['numCtrls'] + 1):
			mc.delete('iControlMidMus_%s%s1_pointConstraint1' % (muscleData['name'], str(cIndex)))
			# mc.delete('iControlMidMus_%s%s1_crossSectionREST_blendShape' % (muscleData['name'], str(cIndex)))

	def deleteUnusedPoses():
		mc.select('%s_*_y45_grp' % muscleData['name'], r=True)
		mc.select('%s_*_y135_grp' % muscleData['name'], add=True)
		mc.delete()

	def connectDriver():
		# for cIndex in controlIndexList:
		for cIndex in range(1, muscleData['numCtrls'] + 1):
			pIndex = 0
			i = 0
			for axis1Point in driverData['axis1Pts']: 
				for axis2Point in driverData['axis2Pts']:

					# CONTROLS
					controlTargetName = '%s_control%s_%s_%s_w0_target' % (muscleData['name'], str(cIndex), axis1Point, axis2Point)
					control = 'iControlMidMus_%s%s1' % (muscleData['name'], str(cIndex))
					# Create point constraints				
					mc.pointConstraint(controlTargetName, control, weight=0.0)
					# Connect driver outputs to point constraint
					mc.connectAttr(
						'%s.%s_%s' % (driverData['driverName'], axis1Point, axis2Point), 
						'%s_pointConstraint1.%sW%s' % (control, controlTargetName, str(pIndex)))
					pIndex += 1

					# # CROSS SECTIONS
					# targetName = '%s_crossSection%s_%s_%s_%s_target' % (muscleData['name'], str(cIndex), axis1Point, axis2Point, axis3Point)
					# crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscleData['name'], str(cIndex))
					# blendShapeNode = '%s_blendShape' % crossSection
			
					# # Create blend shape node with 1st target. 
					# # Add to blend shape node for additional targets.

					# if i == 0:
					# 	mc.blendShape(
					# 		targetName, 
					# 		crossSection, 
					# 		name = blendShapeNode)
					# 	bIndex = 1
					# 	i = 1
					# else:
					# 	mc.blendShape(
					# 		blendShapeNode, 
					# 		edit=True, 
					# 		t=(crossSection, bIndex, targetName, 1.0))
					# 	bIndex += 1
			
					# # Connect driver outputs to blend shape node
					# mc.connectAttr(
					# 	'%s.%s_%s_%s' % (driverData['driverName'], axis1Point, axis2Point, axis3Point), 
					# 	'%s.%s' % (blendShapeNode, targetName))
	
	delExTargetConnections()
	deleteUnusedPoses()	
	connectDriver()




def main():
	
	muscleData1 = {
		'name'			:	'L_teresMajor',
		'numCtrls'		:	5
		}

	muscleData2 = {
		'name'			:	'',
		'numCtrls'		:	8
		}

	driverData = {
		'driverName'	: 	'N3_muscleDriver3', 
		'axis1Name'		: 	'N3_humerus_long_data2', 
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Name'		: 	'N3_biceps_lat_data', 
		'axis2Pts'		: 	('y0', 'y90', 'y170')
		}
	
	drivePoses(muscleData1, driverData)

	print '\r\rScript completed successfully\r\r'



if __name__ == "__main__":
	main()
	










