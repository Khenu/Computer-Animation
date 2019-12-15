# neferMuscleShoulderReducedY0.py
# Created by Laushon Neferkara on 11/25/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''


'''


class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleName, numCtrls, driverName, poseList, crossSections=True):
		self.muscleName = muscleName
		self.numCtrls = numCtrls
		self.driverName = driverName
		self.crossSections = crossSections
		self.poseList = poseList
		self.createConstraints()
		self.connectDriver()


	def createConstraints(self):
		# Create 
		# for dIndex in range(self.numCtrls):
		# 	ctrlTargetList = []
		# 	for driverPt in self.poseList:
		# 		ctrlTargetName = '%s_control%s_%s_target' % (self.muscleName, str(dIndex + 1), driverPt)
		# 		ctrlTargetList.append(ctrlTargetName)
		# 	ctrlCurve = 'iControlMidMus_%s%s1' % (self.muscleName, str(dIndex + 1))
		# 	mc.pointConstraint(ctrlTargetList, ctrlCurve, weight=0.0)

		if self.crossSections:
			for dIndex in range(self.numCtrls):
				crossTargetList = []
				for driverPt in self.poseList:
					crossTargetName = '%s_crossSection%s_%s_target' % (self.muscleName, str(dIndex + 1), driverPt)
					crossTargetList.append(crossTargetName)
				crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (self.muscleName, str(dIndex + 1))
				bShapeNode = '%s_blendShape' % crossSection
				mc.blendShape(crossTargetList[0], crossSection, name=bShapeNode)
				# Add the remaining targets to the blend shape node
				for bIndex in range(1, len(crossTargetList)):
					mc.blendShape(bShapeNode, edit=True, t=(crossSection, bIndex, crossTargetList[bIndex], 1.0))


	def connectDriver(self):
		# 'Connect the Maya Muscle control point constraint to the driver.'
		# for dIndex in range(self.numCtrls):
		# 	ctrlCurve = 'iControlMidMus_%s%s1' % (self.muscleName, str(dIndex + 1))
		# 	ctrlTargetList = []
		# 	for driverPt in self.poseList:
		# 		ctrlTargetName = '%s_control%s_%s_target' % (self.muscleName, str(dIndex + 1), driverPt)
		# 		ctrlTargetList.append(ctrlTargetName)

		# 	for pIndex in range(len(ctrlTargetList)):
		# 		mc.connectAttr(
		# 			'%s.%s' % (self.driverName, self.poseList[pIndex]),
		# 			'%s_pointConstraint1.%sW%s' % (ctrlCurve, ctrlTargetList[pIndex], str(pIndex))
		# 			)
		
		if self.crossSections:
			for dIndex in range(self.numCtrls):
				crossTargetList = []
				for driverPt in self.poseList:
					crossTargetName = '%s_crossSection%s_%s_target' % (self.muscleName, str(dIndex + 1), driverPt)
					crossTargetList.append(crossTargetName)

				crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (self.muscleName, str(dIndex + 1))
				bShapeNode = '%s_blendShape' % crossSection
				for pIndex in range(len(crossTargetList)):
					mc.connectAttr(
						'%s.%s' % (self.driverName, self.poseList[pIndex]),
						'%s.%s' % (bShapeNode, crossTargetList[pIndex])
						)






def main():

	poseList = [
		# x0 group
		# 'x0_y0_w0', 
		'x0_y0_w45', 
		'x0_y0_w90', 						# out of range at y0 but need to blend with y45
		'x0_y0_wn45', 
		'x0_y0_wn90', 						# out of range at y0 but need to blend with y45
		
		'x0_y45_w0', 
		'x0_y45_w45', 
		'x0_y45_w90', 
		'x0_y45_wn45', 
		# 'x0_y45_wn90',	out of range

		'x0_y90_w0', 
		'x0_y90_w45', 
		'x0_y90_w90', 
		# 'x0_y90_wn45',	out of range
		# 'x0_y90_wn90',	out of range

		'x0_y135_w0', 
		'x0_y135_w45', 
		'x0_y135_w90', 
		# 'x0_y135_wn45',	out of range
		# 'x0_y135_wn90',	out of range

		'x0_y170_w0', 
		'x0_y170_w45', 
		'x0_y170_w90', 
		# 'x0_y170_wn45',	out of range
		# 'x0_y170_wn90',	out of range

		# x45 group
		# 'x45_y0_w0', 
		'x45_y0_w45', 
		'x45_y0_w90', 
		'x45_y0_wn45', 
		'x45_y0_wn90', 
		
		'x45_y45_w0', 
		'x45_y45_w45', 
		# 'x45_y45_w90', 	out of range?
		'x45_y45_wn45', 
		# 'x45_y45_wn90',	out of range?

		'x45_y90_w0', 
		'x45_y90_w45', 
		# 'x45_y90_w90', 	out of range
		'x45_y90_wn45',	
		# 'x45_y90_wn90',	out of range

		'x45_y135_w0', 
		'x45_y135_w45', 
		# 'x45_y135_w90', 	out of range
		'x45_y135_wn45',	
		# 'x45_y135_wn90',	out of range

		'x45_y170_w0', 
		'x45_y170_w45', 
		# 'x45_y170_w90', 	out of range
		'x45_y170_wn45',
		# 'x45_y170_wn90',	out of range

		# x90 group
		# 'x90_y0_w0', 
		'x90_y0_w45', 
		'x90_y0_w90', 
		'x90_y0_wn45', 
		'x90_y0_wn90', 
		
		'x90_y45_w0', 
		'x90_y45_w45', 
		'x90_y45_w90', 					# ** Added back **
		'x90_y45_wn45', 
		'x90_y45_wn90',	

		'x90_y90_w0', 	
		'x90_y90_w45', 					# ** Added back **
		# 'x90_y90_w90', 	out of range
		'x90_y90_wn45',	
		'x90_y90_wn90',	

		'x90_y135_w0', 	
		# 'x90_y135_w45', 	out of range
		# 'x90_y135_w90', 	out of range
		'x90_y135_wn45',	
		'x90_y135_wn90',	

		'x90_y170_w0', 	
		# 'x90_y170_w45', 	out of range
		# 'x90_y170_w90', 	out of range
		'x90_y170_wn45', 
		'x90_y170_wn90', 

		# x135 group
		# 'x135_y0_w0', 
		'x135_y0_w45', 
		'x135_y0_w90', 
		'x135_y0_wn45', 
		'x135_y0_wn90', 
		
		'x135_y45_w0', 
		'x135_y45_w45', 
		'x135_y45_w90', 
		'x135_y45_wn45', 
		'x135_y45_wn90', 

		'x135_y90_w0', 
		'x135_y90_w45', 
		'x135_y90_w90', 
		# 'x135_y90_wn45',	out of range
		# 'x135_y90_wn90',	out of range

		# 'x135_y135_w0', 	out of range
		# 'x135_y135_w45', 	out of range
		# 'x135_y135_w90', 	out of range
		# 'x135_y135_wn45',	out of range
		# 'x135_y135_wn90',	out of range

		# 'x135_y170_w0', 	out of range
		# 'x135_y170_w45', 	out of range
		# 'x135_y170_w90', 	out of range
		# 'x135_y170_wn45',	out of range
		# 'x135_y170_wn90',	out of range

		# x180 group
		# 'x180_y0_w0', 
		'x180_y0_w45', 
		'x180_y0_w90', 
		'x180_y0_wn45', 
		'x180_y0_wn90', 
		
		'x180_y45_w0', 
		'x180_y45_w45', 
		'x180_y45_w90', 
		'x180_y45_wn45', 
		# 'x180_y45_wn90',	out of range ???

		# 'x180_y90_w0', 	out of range
		# 'x180_y90_w45', 	out of range
		# 'x180_y90_w90', 	out of range
		# 'x180_y90_wn45',	out of range
		# 'x180_y90_wn90',	out of range

		# 'x180_y135_w0', 	out of range
		# 'x180_y135_w45', 	out of range
		# 'x180_y135_w90', 	out of range
		# 'x180_y135_wn45',	out of range
		# 'x180_y135_wn90',	out of range

		# 'x180_y170_w0', 	out of range
		# 'x180_y170_w45', 	out of range
		# 'x180_y170_w90', 	out of range
		# 'x180_y170_wn45',	out of range
		# 'x180_y170_wn90',	out of range

		# xn45 group
		# 'xn45_y0_w0', 
		'xn45_y0_w45', 
		'xn45_y0_w90', 
		'xn45_y0_wn45', 
		# 'xn45_y0_wn90', 	out of range
		
		'xn45_y45_w0', 
		'xn45_y45_w45', 
		'xn45_y45_w90', 
		'xn45_y45_wn45', 
		# 'xn45_y45_wn90',	out of range

		'xn45_y90_w0', 
		'xn45_y90_w45', 
		'xn45_y90_w90', 
		# 'xn45_y90_wn45',	out of range
		# 'xn45_y90_wn90',	out of range

		'xn45_y135_w0', 
		'xn45_y135_w45', 
		'xn45_y135_w90', 
		# 'xn45_y135_wn45',	out of range
		# 'xn45_y135_wn90',	out of range

		'xn45_y170_w0', 
		'xn45_y170_w45', 
		'xn45_y170_w90', 
		# 'xn45_y170_wn45',	out of range
		# 'xn45_y170_wn90',	out of range

		]

	
	driverName = 'N3_muscleDriver1'

	NeferMuscle('L_deltoidAnteriorA', 5, driverName, poseList) 
	NeferMuscle('L_deltoidAnteriorB', 5, driverName, poseList) 
	NeferMuscle('L_deltoidAnteriorC', 5, driverName, poseList) 
	NeferMuscle('L_deltoidLateralA', 5, driverName, poseList) 
	NeferMuscle('L_deltoidLateralB', 5, driverName, poseList) 
	NeferMuscle('L_deltoidLateralC', 5, driverName, poseList) 
	NeferMuscle('L_deltoidPosteriorA', 5, driverName, poseList) 
	NeferMuscle('L_deltoidPosteriorB', 5, driverName, poseList) 
	NeferMuscle('L_deltoidPosteriorC', 5, driverName, poseList) 
	NeferMuscle('L_deltoidPosteriorD', 5, driverName, poseList) 

	NeferMuscle('L_pectoralisMajor2A', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2B', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2C', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2D', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2E', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2F', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2G', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2H', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2I', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2J', 6, driverName, poseList) 
	NeferMuscle('L_pectoralisMajor2K', 6, driverName, poseList) 

	NeferMuscle('L_latissimusDorsi2A', 6, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2B', 6, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2C', 7, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2D', 7, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2E', 8, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2F', 9, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2G', 9, driverName, poseList)
	NeferMuscle('L_latissimusDorsi2H', 7, driverName, poseList) 
	NeferMuscle('L_teresMajor', 5, driverName, poseList) 
	NeferMuscle('L_teresMinor2', 5, driverName, poseList) 
	# NeferMuscle('L_infraspinatusA', 5, driverName, poseList, crossSections=False) 
	# NeferMuscle('L_infraspinatusB', 5, driverName, poseList, crossSections=False) 
	# NeferMuscle('L_infraspinatusC', 5, driverName, poseList, crossSections=False) 
	# NeferMuscle('L_coracobrachialis2', 5, driverName, poseList, crossSections=False) 
	NeferMuscle('L_bicepsBrachiiShort', 7, driverName, poseList) 
	NeferMuscle('L_bicepsBrachiiLong', 7, driverName, poseList)
	NeferMuscle('L_brachialisA', 5, driverName, poseList) 
	NeferMuscle('L_tricepsLateral', 5, driverName, poseList) 
	NeferMuscle('L_tricepsLong', 5, driverName, poseList)


if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'











