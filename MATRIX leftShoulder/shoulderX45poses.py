# shoulderX45poses.py
# Created by Laushon Neferkara on 4/14/14.
# Copyright (c) 2014 Skin+Bones Modeling and Rigging Company. All rights reserved.
'''
'''


import pymel.core as pm

class Driver():
	"""docstring for Driver"""
	def __init__(self, name, data):
		self.name = name
		self.data = data

						
class MuscleCrossSection():
	'''Represents a Maya Muscle cross section of a neferMuscle.'''
	def __init__(self, muscleName, cIndex, nDriver):	
		self.muscleName = muscleName
		self.name = 'iControlMidMus_%s%s1_crossSectionREST' % (self.muscleName, str(cIndex))
		self.nDriver = nDriver
		self.targetList = []
		self.driverList = []			
		self.blendShape = '%s_blendShape' % self.name

	def addTarget(self, target):
		self.targetList.append(target)
	
	def addDriver(self, driver):
		self.driverList.append(driver)

	def connectTargets(self):
		'Create blend shape node to all of the targets'
		# Create blend shape node with 1st target
		pm.blendShape(self.targetList[0], self.name, name = self.blendShape)
		# Add the remaining targets to the blend shape node
		for bIndex in range(1, len(self.targetList)):
			pm.blendShape(self.blendShape, edit=True, t=(self.name, bIndex, self.targetList[bIndex], 1.0))

	def connectDriver(self):
		'Connect the Maya Muscle control blend shape node to the driver.'
		for pIndex in range(len(self.targetList)):
			pm.connectAttr('%s.%s' % (self.nDriver, self.driverList[pIndex]), '%s.%s' % (self.blendShape, self.targetList[pIndex]))
							

class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleName, newFirst, newLast, driverInfo):
		self.muscleName = muscleName
		self.newFirst = newFirst
		self.newLast = newLast
		self.muscleDriver = driverInfo.name
		self.data = driverInfo.data
		
	def deleteBlendShape(self):
		for cIndex in range(self.newFirst, self.newLast + 1):
			mc.delete('iControlMidMus_%s%s1_crossSectionREST_blendShape' % (self.muscleName, cIndex))

	def poseCopy(self, sourcePoseA, sourcePoseB, destPose):
		for cIndex in range(self.newFirst, self.newLast + 1):
			sourceA = '%s_crossSection%s_%s_target' % (self.muscleName, cIndex, sourcePoseA)
			sourceB = '%s_crossSection%s_%s_target' % (self.muscleName, cIndex, sourcePoseB)
			destination = '%s_crossSection%s_%s_target' % (self.muscleName, cIndex, destPose)
			destParent = '%s_control%s_%s_target' % (self.muscleName, cIndex, destPose)
			# mc.delete(destination)
			mc.blendShape(sourceA, sourceB, destination, w=[(0, 1.0), (1, 1.0)])
			mc.duplicate(destination, n=destination + '_new')
			mc.delete(destination)
			mc.rename(destination + '_new', destination)
			# mc.parent(destination, destParent)


	def createCSDeformation(self):
		# Create objects to represent the Maya Muscle cross sections and place in list
		self.musCross = []
		for cIndex in range(self.newFirst, self.newLast + 1):
			self.musCross.append(MuscleCrossSection(self.muscleName, cIndex, self.muscleDriver))

		# 
		for pointA in self.data[0]:
			for pointB in self.data[1]:
				for pointC in self.data[2]:
					driverPt = '%s_%s_%s' % (pointA, pointB, pointC)
					
					# control target
					ctrlTargetName = '%s_control_%s_target' % (self.muscleName, driverPt)

					mcIndex = 0
					for dIndex in range(self.newFirst, self.newLast + 1):
						# Create cross section target
						crossTarget = '%s_crossSection%s_%s_target' % (self.muscleName, str(dIndex), driverPt)
						# Add muscle cross target to muscle controls's target list
						self.musCross[mcIndex].addTarget(crossTarget)

						# Add driver to driver list
						self.musCross[mcIndex].addDriver(driverPt)
						mcIndex += 1

		# Connect pose targets to muscle cross sections with blend shape node
		for index in range(len(self.musCross)):
			self.musCross[index].connectTargets()
		# Connect blend shape node weights to driver
		for index in range(len(self.musCross)):
			self.musCross[index].connectDriver()






def poseCopy(sourcePoseA, sourcePoseB, destPose):
	
	n3driver = Driver(
		'N3_muscleDriver1', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y45', 'y90', 'y135', 'y170'), 
		('w0', 'w45', 'w90', 'wn45', 'wn90'))
		)

	# List for controls
	muscleList = [
		['L_deltoidAnteriorA', 5], 
		['L_deltoidAnteriorB', 5], 
		['L_deltoidAnteriorC', 5], 
		['L_deltoidLateralA', 5], 
		['L_deltoidLateralB', 5], 
		['L_deltoidLateralC', 5], 
		['L_deltoidPosteriorA', 5], 
		['L_deltoidPosteriorB', 5], 
		['L_deltoidPosteriorC', 5], 
		['L_deltoidPosteriorD', 5],  
		['L_pectoralisA', 6],
		['L_pectoralisB', 6],
		['L_pectoralisC', 6],
		['L_pectoralisD', 6],
		['L_pectoralisE', 6],
		['L_pectoralisF', 6],
		['L_pectoralisG', 6],
		['L_pectoralisH', 6],
		['L_pectoralisJ', 6],
		['L_pectoralisK', 7],
		['L_pectoralisL', 7],
		['L_pectoralisM', 7], 
		['L_latissimusDorsi2A', 6],
		['L_latissimusDorsi2B', 6],
		['L_latissimusDorsi2C', 7],
		['L_latissimusDorsi2D', 7],
		['L_latissimusDorsi2E', 8],
		['L_latissimusDorsi2F', 9],
		['L_latissimusDorsi2G', 9],
		['L_latissimusDorsi2H', 7], 
		['L_teresMajor', 5], 
		['L_teresMinor2', 5], 
		['L_infraspinatusA', 5], 
		['L_infraspinatusB', 5], 
		['L_infraspinatusC', 5], 
		['L_coracobrachialisB', 5], 
		['L_brachialisA', 5], 
		['L_bicepsBrachiiShort2', 6], 
		['L_bicepsBrachiiLong2', 6], 
		['L_tricepsLateral', 5], 
		['L_tricepsLong', 5],
		['L_trapeziusO', 4], 
		['L_trapeziusP', 4], 
		['L_trapeziusQ', 4], 
		['L_trapeziusR', 4], 
		['L_trapeziusS', 4]
		]

	# List for cross sections
	muscleListB = [
		['L_deltoidAnteriorA', 5], 
		['L_deltoidAnteriorB', 5], 
		['L_deltoidAnteriorC', 5], 
		['L_deltoidLateralA', 5], 
		['L_deltoidLateralB', 5], 
		['L_deltoidLateralC', 5], 
		['L_deltoidPosteriorA', 5], 
		['L_deltoidPosteriorB', 5], 
		['L_deltoidPosteriorC', 5], 
		['L_deltoidPosteriorD', 5],  
		['L_pectoralisA', 6],
		['L_pectoralisB', 6],
		['L_pectoralisC', 6],
		['L_pectoralisD', 6],
		['L_pectoralisE', 6],
		['L_pectoralisF', 6],
		['L_pectoralisG', 6],
		['L_pectoralisH', 6],
		['L_pectoralisJ', 6],
		['L_pectoralisK', 7],
		['L_pectoralisL', 7],
		['L_pectoralisM', 7], 
		['L_latissimusDorsi2A', 6],
		['L_latissimusDorsi2B', 6],
		['L_latissimusDorsi2C', 7],
		['L_latissimusDorsi2D', 7],
		['L_latissimusDorsi2E', 8],
		['L_latissimusDorsi2F', 9],
		['L_latissimusDorsi2G', 9],
		['L_latissimusDorsi2H', 7], 
		['L_teresMajor', 5], 
		['L_teresMinor2', 5], 
		# ['L_infraspinatusA', 5], 
		# ['L_infraspinatusB', 5], 
		# ['L_infraspinatusC', 5], 
		['L_coracobrachialisB', 5], 
		['L_brachialisA', 5], 
		['L_bicepsBrachiiShort2', 6], 
		['L_bicepsBrachiiLong2', 6], 
		['L_tricepsLateral', 5], 
		['L_tricepsLong', 5],
		['L_trapeziusO', 4], 
		['L_trapeziusP', 4], 
		['L_trapeziusQ', 4], 
		['L_trapeziusR', 4], 
		['L_trapeziusS', 4]
		]


	# # Controls
	# for muscleData in muscleList: 
	# 	for cNum in range(1, muscleData[1] + 1):
	# 		sourceTarget = '%s_control%s_%s_target' % (muscleData[0], cNum, sourcePose)
	# 		destTarget = '%s_control%s_%s_target' % (muscleData[0], cNum, destPose)
	# 		mc.setAttr('%s.translateX' % destTarget, mc.getAttr('%s.translateX' % sourceTarget))
	# 		mc.setAttr('%s.translateY' % destTarget, mc.getAttr('%s.translateY' % sourceTarget))
	# 		mc.setAttr('%s.translateZ' % destTarget, mc.getAttr('%s.translateZ' % sourceTarget))

	# # Cross sections
	# for muscleData in muscleListB: 
	# 	muscle = NeferMuscle(muscleData[0], 1, muscleData[1], n3driver)
	# 	muscle.deleteBlendShape()
	# 	muscle.poseCopy(sourcePose, destPose)
	# 	muscle.createCSDeformation()

	# Controls
	for muscleData in muscleList: 
		for cNum in range(1, muscleData[1] + 1):
			sourceTargetA = '%s_control%s_%s_target' % (muscleData[0], cNum, sourcePoseA)
			sourceTargetB = '%s_control%s_%s_target' % (muscleData[0], cNum, sourcePoseB)
			destTarget = '%s_control%s_%s_target' % (muscleData[0], cNum, destPose)

			mc.setAttr('%s.translateX' % destTarget, 
				(mc.getAttr('%s.translateX' % sourceTargetA) + mc.getAttr('%s.translateX' % sourceTargetB))/2
				)
			
			mc.setAttr('%s.translateY' % destTarget, 
				(mc.getAttr('%s.translateY' % sourceTargetA) + mc.getAttr('%s.translateY' % sourceTargetB))/2
				)
			
			mc.setAttr('%s.translateZ' % destTarget, 
				(mc.getAttr('%s.translateZ' % sourceTargetA) + mc.getAttr('%s.translateZ' % sourceTargetB))/2
				)

	# Cross sections
	for muscleData in muscleListB: 
		muscle = NeferMuscle(muscleData[0], 1, muscleData[1], n3driver)
		muscle.deleteBlendShape()
		muscle.poseCopy(sourcePoseA, sourcePoseB, destPose)
		muscle.createCSDeformation()


def main():

	latList = 	['y45', 'y90', 'y135', 'y170']

	twistList = ['w0', 'w45', 'w90', 'wn45', 'wn90']

	for latPt in latList:
		for twistPt in twistList:
			poseCopy('x0_%s_%s' % (latPt, twistPt), 'x90_%s_%s' % (latPt, twistPt), 'x45_%s_%s' % (latPt, twistPt))



if __name__ == '__main__':
	main()

print '\r\rScript completed successfully. Wait for Channel Box to become active.\r\r'




