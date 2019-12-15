# N3DeltoidAddCrossSections.py
# Created by Laushon Neferkara on 10/11/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Add cross section blend shapes.
# Muscle Ctrls are already posed.

# Import function module
import nm

import pymel.core as pm

class Driver():
	"""docstring for Driver"""
	def __init__(self, driverData):
		self.name = driverData['driverName']
		self.axis1Pts = driverData['axis1Pts']
		self.axis2Pts = driverData['axis2Pts']
		self.axis3Pts = driverData['axis3Pts']

							

class MuscleCrossSection():
	'''Represents a Maya Muscle cross section of a neferMuscle.'''
	def __init__(self, muscleName, cIndex, nDriver):	
		self.muscleName = muscleName
		self.name = 'iControlMidMus_%s%s1_crossSectionREST' % (self.muscleName, str(cIndex + 1))
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
			pm.blendShape(self.blendShape, edit=True, 
				t=(self.name, bIndex, self.targetList[bIndex], 1.0))

	def connectDriver(self):
		'Connect the Maya Muscle control blend shape node to the driver.'
		for pIndex in range(len(self.targetList)):
			pm.connectAttr(
				'%s.%s' % (self.nDriver, self.driverList[pIndex]),
				'%s.%s' % (self.blendShape, self.targetList[pIndex])
				)
							

class SceneTarget():
	'''Represents a target object in Maya.'''
	def __init__(self, name, baseObj, parentGrpName):	
		self.name = name
		self.baseObj = baseObj
		self.parentGrpName = parentGrpName
		
		# Duplicate muscle control
		pm.duplicate(self.baseObj.name, n=self.name)

		# Delete the child squash and stretch curves. (Cross sections do not have.) 
		children = pm.listRelatives(self.name, type='transform', path=True)
		# listRelatives returns a list
		if children:
			pm.delete(children)

		# Unlock transforms for reparenting
		attrList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ']
		for attr in attrList:
			pm.setAttr('%s.%s' % (self.name, attr), lock=False)

		# Make visible
		visibility = '%s.visibility' % self.name
		pm.setAttr(visibility, keyable=True)	
		if pm.connectionInfo(visibility, isDestination=True):
			source = pm.connectionInfo(visibility, sourceFromDestination=True)
			pm.disconnectAttr(source, visibility)

		# Parent to parent grp
		pm.parent(self.name, parentGrpName)

		# Add muscle cross target to muscle controls's target list
		self.baseObj.addTarget(self.name)


class MuscleCtrlTarget(SceneTarget):
	'''Represents a target for a Maya Muscle control.'''
	def __init__(self, name, musCtrl, parentGrpName):	
		SceneTarget.__init__(self, name, musCtrl, parentGrpName)
		# Lock unused transforms
		pm.setAttr('%s.rotate' % self.name, lock=True)
		pm.setAttr('%s.scale' % self.name, lock=True)
		# Make visible
		pm.setAttr('%s.visibility' % self.name, True)



class MuscleCrossTarget(SceneTarget):
	'''Represents a target for a Maya Muscle cross section.'''
	def __init__(self, name, musCross, parentGrpName):	
		SceneTarget.__init__(self, name, musCross, parentGrpName)
		# Lock all transforms
		pm.setAttr('%s.translate' % self.name, lock=True)
		pm.setAttr('%s.rotate' % self.name, lock=True)
		pm.setAttr('%s.scale' % self.name, lock=True)
		# Make visible
		pm.setAttr('%s.visibility' % self.name, True)


class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleName, numCtrls, n3driver):
		self.muscleName = muscleName
		# self.muscleDriver = n3driver.name
		self.n3driver = n3driver
		self.numCtrls = numCtrls
		# self.data = driverInfo.data
		self.getMayaMusInfo()
		self.setupMayaMus()
		self.createPoses()
		self.connectDriver()
		
	def getMayaMusInfo(self):
		# # Calculate the number of controls on the Maya Muscle
		# ctrlList = pm.ls('iControlMidMus_%s*1' % self.muscleName, exactType='transform')
		# self.numCtrls = len(ctrlList)

		# Create objects to represent the Maya Muscle controls and cross sections and place in list
		self.musCtrls = []
		self.musCross = []
		for cIndex in range(self.numCtrls):
			# self.musCtrls.append(MuscleControl(self.muscleName, cIndex, self.muscleDriver))
			self.musCross.append(MuscleCrossSection(self.muscleName, cIndex, self.n3driver.name))

	def setupMayaMus(self):
		# Set Based On attribute of Maya Muscle to pose
	  	pm.setAttr('cMuscleCreatorMus_%s1.basedOn' % self.muscleName, 1)	

	def createPoses(self):

		# # Create the main pose group for the muscle
		# topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		# mainPoseGrp = SimpleGrp('%s_pose_grp' % self.muscleName, topPoseGrp)

		# Create the cross section poses 
		for dIndex in range(self.numCtrls):
			for axis1Point in self.n3driver.axis1Pts: 
				for axis2Point in self.n3driver.axis2Pts:
					for axis3Point in self.n3driver.axis3Pts:
						# Create cross section target
						crossTargetName = '%s_crossSection%s_%s_%s_%s_target' % (self.muscleName, str(dIndex + 1), axis1Point, axis2Point, axis3Point)
						ctrlTargetName = '%s_control%s_%s_%s_%s_target' % (self.muscleName, str(dIndex + 1), axis1Point, axis2Point, axis3Point)
						# Save ctrlTarget pose info. Set to 0
						transX = '%s.translateX' % ctrlTargetName
						transY = '%s.translateY' % ctrlTargetName
						transZ = '%s.translateZ' % ctrlTargetName
						ctrlTargetTransX = mc.getAttr(transX)
						ctrlTargetTransY = mc.getAttr(transY)
						ctrlTargetTransZ = mc.getAttr(transZ)
						mc.setAttr(transX, 0)
						mc.setAttr(transY, 0)
						mc.setAttr(transZ, 0)
						#
						rotX = '%s.rotateX' % ctrlTargetName
						rotY = '%s.rotateY' % ctrlTargetName
						rotZ = '%s.rotateZ' % ctrlTargetName
						ctrlTargetRotX = mc.getAttr(rotX)
						ctrlTargetRotY = mc.getAttr(rotY)
						ctrlTargetRotZ = mc.getAttr(rotZ)
						mc.setAttr(rotX, 0)
						mc.setAttr(rotY, 0)
						mc.setAttr(rotZ, 0)

						crossTarget = MuscleCrossTarget(crossTargetName, self.musCross[dIndex], ctrlTargetName)

						# Reset ctrlTarget pose.
						mc.setAttr(transX, ctrlTargetTransX)
						mc.setAttr(transY, ctrlTargetTransY)
						mc.setAttr(transZ, ctrlTargetTransZ)
						mc.setAttr(rotX, ctrlTargetRotX)
						mc.setAttr(rotY, ctrlTargetRotY)
						mc.setAttr(rotZ, ctrlTargetRotZ)


						# Add driver to driver list
						# self.musCtrls[dIndex].addDriver(driverPt)
						self.musCross[dIndex].addDriver('%s_%s_%s' % (axis1Point, axis2Point, axis3Point))

	def connectDriver(self):
		# Connect poses to muscle control and muscle cross sections
		for index in range(self.numCtrls):
			# self.musCtrls[index].connectTargets()
			self.musCross[index].connectTargets()
		
		# Connect driver
		for index in range(self.numCtrls):
			# self.musCtrls[index].connectDriver()
			self.musCross[index].connectDriver()





def main():

	driverData = {
		'driverName'	: 	'N3_muscleDriver1', 
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Pts'		: 	('y0', 'y45', 'y90', 'y135', 'y170'),
		'axis3Pts'		: 	('w0', 'w45', 'w90', 'wn45', 'wn90')
		}
	
	n3driver = Driver(driverData)

	# Can not run all of these at once in Maya
	# 
	# muscle = NeferMuscle('L_deltoidPosteriorA', 5, n3driver)
	# muscle = NeferMuscle('L_deltoidPosteriorB', 5, n3driver)
	# muscle = NeferMuscle('L_deltoidPosteriorC', 5, n3driver)
	muscle = NeferMuscle('L_deltoidPosteriorD', 5, n3driver)

if __name__ == '__main__':
	main()







#################################################################################



def drivePoses(muscleData, driverData):
	
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
	
	connectDriver()




def main():
	
	muscleData1 = {
		'name'			:	'L_latissimusDorsiA',
		'numCtrls'		:	6
		}

	muscleData2 = {
		'name'			:	'L_latissimusDorsiB',
		'numCtrls'		:	6
		}
	
	muscleData3 = {
		'name'			:	'L_latissimusDorsiC',
		'numCtrls'		:	7
		}

	muscleData4 = {
		'name'			:	'L_latissimusDorsiD',
		'numCtrls'		:	7
		}

	muscleData5 = {
		'name'			:	'L_latissimusDorsiE',
		'numCtrls'		:	8
		}

	muscleData6 = {
		'name'			:	'L_latissimusDorsiF',
		'numCtrls'		:	9
		}

	muscleData7 = {
		'name'			:	'L_latissimusDorsiH',
		'numCtrls'		:	9
		}

	muscleData8 = {
		'name'			:	'L_latissimusDorsiG',
		'numCtrls'		:	7
		}


	driverData = {
		'driverName'	: 	'N3_muscleDriver3', 
		'axis1Name'		: 	'N3_humerus_long_data2', 
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Name'		: 	'N3_biceps_lat_data', 
		'axis2Pts'		: 	('y0', 'y90', 'y170')
		}
	
	# drivePoses(muscleData1, driverData)
	drivePoses(muscleData2, driverData)
	drivePoses(muscleData3, driverData)
	drivePoses(muscleData4, driverData)
	drivePoses(muscleData5, driverData)
	drivePoses(muscleData6, driverData)
	drivePoses(muscleData7, driverData)
	drivePoses(muscleData8, driverData)

	print '\r\rScript completed successfully\r\r'



if __name__ == "__main__":
	main()
	










