# neferMuscleDeltoidNew2_extra.py
# Created by Laushon Neferkara on 10/8/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''
Creates _extra_grp's

'''


import pymel.core as pm

class Driver():
	"""docstring for Driver"""
	def __init__(self, name, data):
		self.name = name
		self.data = data


class SimpleGrp():
	'''Create a group in the Maya scene with the translate, rotate and scale attributes 
	locked and hidden'''
	def __init__(self, name, parent, lockTrans=True):
		self.name = name
		# Test if parent is a object or a string?
		self.parent = parent
		hideList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ']
		# Create the group in the scene
		newGrp = pm.group(em=True, r=True, n=self.name, p=self.parent)
		# Lock and hide the translate, rotate and scale attributes
		if lockTrans:
			for transform in hideList:
				newGrp.attr(transform).set(lock=True, keyable=False, cb=False)
		
	def parentConstraint(self, targetName):
		mc.parentConstraint(targetName, self.name, maintainOffset=False)
	
	def makeInvisible(self):
		mc.setAttr(self.name + '.visibility', False)
		
	def makeVisible(self):
		mc.setAttr(self.name + '.visibility', True)
		

class ExtraCtrl():
	'''Represents a'''
	def __init__(self, muscleName, cIndex, nDriver):	
		self.muscleName = muscleName		
		# self.name = 'iControlMidMus_%s%s1' % (self.muscleName, str(cIndex + 1))
		self.name = 'iControlMidMus_%s%s1_extra_grp' % (self.muscleName, str(cIndex + 1))
		self.autoGrpName = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex + 1))
		self.nDriver = nDriver
		self.targetList = []
		self.driverList = []

	def addTarget(self, target):
		self.targetList.append(target)
	
	def addDriver(self, driver):
		self.driverList.append(driver)

	def connectTargets(self):
		'Create point constraint to all of the targets'
		mc.orientConstraint(self.targetList, self.name, skip=["x", "z"], weight=0.0)

	def connectDriver(self):
		'Connect the Maya Muscle control point constraint to the driver.'
		for pIndex in range(len(self.targetList)):
			mc.connectAttr(
				'%s.%s' % (self.nDriver, self.driverList[pIndex]),
				'%s_orientConstraint1.%sW%s' % (self.name, self.targetList[pIndex], str(pIndex))
				)
							

class MuscleExtraTarget():
	'''Represents a target for a Maya Muscle control.'''
	def __init__(self, name, baseObj, parentGrpName):	
		self.name = name
		self.baseObj = baseObj
		self.parentGrpName = parentGrpName
		
		# Duplicate 
		mc.duplicate(self.baseObj.name, n=self.name)

		# Delete the children 
		children = mc.listRelatives(self.name, type='transform', path=True)
		# listRelatives returns a list
		if children:
			mc.delete(children)

		# Unlock transforms for reparenting
		attrList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ']
		for attr in attrList:
			mc.setAttr('%s.%s' % (self.name, attr), lock=False)

		# Make visible
		visibility = '%s.visibility' % self.name
		mc.setAttr(visibility, keyable=True)	
		if mc.connectionInfo(visibility, isDestination=True):
			source = mc.connectionInfo(visibility, sourceFromDestination=True)
			mc.disconnectAttr(source, visibility)

		# Parent to parent grp
		mc.parent(self.name, parentGrpName)

		# Add muscle cross target to muscle controls's target list
		self.baseObj.addTarget(self.name)
		# Lock unused transforms
		mc.setAttr('%s.scale' % self.name, lock=True)
		# Make visible
		mc.setAttr('%s.visibility' % self.name, True)





class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleName, driverInfo):
		self.muscleName = muscleName
		self.muscleDriver = driverInfo.name
		self.data = driverInfo.data
		self.getMayaMusInfo()
		self.createCtrlRotateGrps()
		# self.createRotateGrpPoses()
		# self.connectExtra()
		
	def getMayaMusInfo(self):
		# Calculate the number of controls on the Maya Muscle
		ctrlList = mc.ls('iControlMidMus_%s*1' % self.muscleName, exactType='transform')
		self.numCtrls = len(ctrlList)

		# Create objects to represent the rotate grps and place in list
		self.extraList = []
		for cIndex in range(self.numCtrls):
			self.extraList.append(ExtraCtrl(self.muscleName, cIndex, self.muscleDriver))


	def createCtrlRotateGrps(self):
		for rIndex in range(self.numCtrls):
			ctrlName = 'iControlMidMus_%s%s1' % (self.muscleName, str(rIndex + 1))
			mc.group(ctrlName, n='%s_extra_grp' % ctrlName)



	def createRotateGrpPoses(self):

		def _createCtrlCrossPoses(parentGrpName, driverPt):
			'Create pose groups for each muscle control/cross section pair.'
			for dIndex in range(self.numCtrls):
				ctrlPoseGrp = SimpleGrp(
					parentGrpName.replace('_extra_grp', '_control%s_extra_grp' % str(dIndex + 1)), 
					parentGrpName, 
					False)
				
				# Constrain ctrlPoseGrp to Maya Muscle control AUTO to get auto movement
				ctrlPoseGrp.parentConstraint(self.extraList[dIndex].autoGrpName)
				
				# Create control target
				ctrlTargetName = '%s_control%s_%s_extra_target' % (self.muscleName, str(dIndex + 1), driverPt)
				ctrlTarget = MuscleExtraTarget(ctrlTargetName, self.extraList[dIndex], ctrlPoseGrp.name)

				# Add driver to driver list
				self.extraList[dIndex].addDriver(driverPt)

		# Create the main pose group for the muscle
		topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		mainPoseGrp = SimpleGrp('%s_pose_extra_grp' % self.muscleName, topPoseGrp)

		# Create the poses within pose groups. Select based on number of axes.
		for pointA in self.data[0]:
			poseGrpA = SimpleGrp(
				mainPoseGrp.name.replace('_pose_extra_grp', '_%s_extra_grp' % pointA), 
				mainPoseGrp.name)
			if len(self.data) == 1:
				poseGrpC.makeInvisible()
				driverPt = pointA
				_createCtrlCrossPoses(poseGrpA.name, driverPt)
			else:
				for pointB in self.data[1]:
					poseGrpB = SimpleGrp(
						poseGrpA.name.replace('_extra_grp', '_%s_extra_grp' % pointB), 
						poseGrpA.name)
					if len(self.data) == 2:
						poseGrpC.makeInvisible()
						driverPt = '%s_%s' % (pointA, pointB)
						_createCtrlCrossPoses(poseGrpB.name, driverPt)
					else:
						for pointC in self.data[2]:
							poseGrpC = SimpleGrp(
								poseGrpB.name.replace('_extra_grp', '_%s_extra_grp' % pointC), 
								poseGrpB.name)
							if len(self.data) == 3:
								poseGrpC.makeInvisible()
								driverPt = '%s_%s_%s' % (pointA, pointB, pointC)
								_createCtrlCrossPoses(poseGrpC.name, driverPt)
							else:
								for pointD in self.data[3]:
									poseGrpD = SimpleGrp(
										poseGrpC.name.replace('_extra_grp', '_%s_extra_grp' % pointD), 
										poseGrpC.name)
									poseGrpC.makeInvisible()
									driverPt = '%s_%s_%s_%s' % (pointA, pointB, pointC, pointD)
									_createCtrlCrossPoses(poseGrpD.name, driverPt)



	def connectExtra(self):
		# Connect poses to 
		for index in range(self.numCtrls):
			self.extraList[index].connectTargets()
		
		# Connect driver
		for index in range(self.numCtrls):
			self.extraList[index].connectDriver()





def main():
	# n3driver = Driver(
	# 	'N3_muscleDriver1', 
	# 	(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
	# 	('y0', 'y45', 'y90', 'y135', 'y170'), 
	# 	('w0', 'w45', 'w90', 'wn45', 'wn90'))
	# 	)
	n3driver = Driver(
		'N3_muscleDriver6', 
		(('x90', ), 
		('y170', ), 
		('wn40', 'wn50', 'wn60', 'wn70', 'wn80', 'wn90'))
		)
	# muscle = NeferMuscle('L_deltoidAnteriorA', n3driver)
	# muscle = NeferMuscle('L_deltoidAnteriorB', n3driver)
	# muscle = NeferMuscle('L_deltoidAnteriorC', n3driver)
	# muscle = NeferMuscle('L_deltoidLateralA', n3driver)
	# muscle = NeferMuscle('L_deltoidLateralB', n3driver)
	# muscle = NeferMuscle('L_deltoidLateralC', n3driver)
	# muscle = NeferMuscle('L_deltoidPosteriorA', n3driver)
	# muscle = NeferMuscle('L_deltoidPosteriorB', n3driver)
	muscle = NeferMuscle('L_deltoidPosteriorC', n3driver)
	muscle = NeferMuscle('L_deltoidPosteriorD', n3driver)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'

