# neferMuscle_bicepsBrachii.py
# Created by Laushon Neferkara on 8/8/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.
'''
Assumptions:
	1. muscle_pose_grp group exists in the scene
'''


import pymel.core as pm

class Driver():
	'''docstring for Driver'''
	def __init__(self, name, data):
		self.name = name
		self.data = data

class SimpleGrp():
	'''Create a group in the Maya scene with the translate, rotate and scale attributes 
	locked and hidden'''
	def __init__(self, name, parentName, lockTrans=True):
		self.name = name
		# Test if parent is a object or a string?
		self.parentName = parentName
		hideList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ']
		# Create the group in the scene
		newGrp = pm.group(em=True, r=True, n=self.name, p=self.parentName)
		# Lock and hide the translate, rotate and scale attributes
		if lockTrans:
			for transform in hideList:
				newGrp.attr(transform).set(lock=True, keyable=False, cb=False)
		
	def parentConstraint(self, targetName):
		pm.parentConstraint(targetName, self.name, maintainOffset=False)
	
	def makeInvisible(self):
		pm.setAttr(self.name + '.visibility', False)
		
	def makeVisible(self):
		pm.setAttr(self.name + '.visibility', True)
		

class MuscleControl():
	'''Represents a Maya Muscle control of a neferMuscle.'''
	def __init__(self, muscleName, cIndex, nDriver):	
		self.muscleName = muscleName		
		self.name = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex + 1))
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
		pm.pointConstraint(self.targetList, self.name, weight=0.0)

	def connectDriver(self):
		'Connect the Maya Muscle control point constraint to the driver.'
		for pIndex in range(len(self.targetList)):
			pm.connectAttr(
				'%s.%s' % (self.nDriver, self.driverList[pIndex]),
				'%s_pointConstraint1.%sW%s' % (self.name, self.targetList[pIndex], str(pIndex))
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


class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleName, driverInfo):
		self.muscleName = muscleName
		self.muscleDriver = driverInfo.name
		self.data = driverInfo.data
		self.getMayaMusInfo()
		self.setupMayaMus()
		self.createPoses()
		self.connectDriver()
		
	def getMayaMusInfo(self):
		# Calculate the number of controls on the Maya Muscle
		ctrlList = pm.ls('iControlMidMus_%s*1' % self.muscleName, exactType='transform')
		self.numCtrls = len(ctrlList)

		# Create objects to represent the Maya Muscle controls and place in list
		self.musCtrls = []
		for cIndex in range(self.numCtrls):
			self.musCtrls.append(MuscleControl(self.muscleName, cIndex, self.muscleDriver))

	def setupMayaMus(self):
		# Set Based On attribute of Maya Muscle to pose
	  	pm.setAttr('cMuscleCreatorMus_%s1.basedOn' % self.muscleName, 1)	

	
	def createPoses(self):

		def _createCtrlCrossPoses(parentGrpName, driverPt):
			'Create pose groups for each muscle control.'
			for dIndex in range(self.numCtrls):
				ctrlPoseGrp = SimpleGrp(
					parentGrpName.replace('_grp', '_control%s_grp' % str(dIndex + 1)), 
					parentGrpName, 
					False)
				
				# Constrain ctrlPoseGrp to Maya Muscle control AUTO to get auto movement
				ctrlPoseGrp.parentConstraint(self.musCtrls[dIndex].autoGrpName)
				
				# Create control target
				ctrlTargetName = '%s_control%s_%s_target' % (self.muscleName, str(dIndex + 1), driverPt)
				ctrlTarget = MuscleCtrlTarget(ctrlTargetName, self.musCtrls[dIndex], ctrlPoseGrp.name)
				
				# Add driver to driver list
				self.musCtrls[dIndex].addDriver(driverPt)

		# Create the main pose group for the muscle
		topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		mainPoseGrp = SimpleGrp('%s_pose_grp' % self.muscleName, topPoseGrp)

		# Create the poses within pose groups. Select based on number of axes.
		for pointA in self.data[0]:
			poseGrpA = SimpleGrp(
				mainPoseGrp.name.replace('_pose_grp', '_%s_grp' % pointA), 
				mainPoseGrp.name)
			if len(self.data) == 1:
				poseGrpC.makeInvisible()
				driverPt = pointA
				_createCtrlCrossPoses(poseGrpA.name, driverPt)
			else:
				for pointB in self.data[1]:
					poseGrpB = SimpleGrp(
						poseGrpA.name.replace('_grp', '_%s_grp' % pointB), 
						poseGrpA.name)
					if len(self.data) == 2:
						poseGrpC.makeInvisible()
						driverPt = '%s_%s' % (pointA, pointB)
						_createCtrlCrossPoses(poseGrpB.name, driverPt)
					else:
						for pointC in self.data[2]:
							poseGrpC = SimpleGrp(
								poseGrpB.name.replace('_grp', '_%s_grp' % pointC), 
								poseGrpB.name)
							if len(self.data) == 3:
								poseGrpC.makeInvisible()
								driverPt = '%s_%s_%s' % (pointA, pointB, pointC)
								_createCtrlCrossPoses(poseGrpC.name, driverPt)
							else:
								for pointD in self.data[3]:
									poseGrpD = SimpleGrp(
										poseGrpC.name.replace('_grp', '_%s_grp' % pointD), 
										poseGrpC.name)
									poseGrpC.makeInvisible()
									driverPt = '%s_%s_%s_%s' % (pointA, pointB, pointC, pointD)
									_createCtrlCrossPoses(poseGrpD.name, driverPt)

	def connectDriver(self):
		# Connect poses to muscle control and muscle cross sections
		for index in range(self.numCtrls):
			self.musCtrls[index].connectTargets()
		
		# Connect driver
		for index in range(self.numCtrls):
			self.musCtrls[index].connectDriver()





def main():
	scriptName = 'neferMuscle_bicepsBrachii.py'
	print '\r' + scriptName + ' running'

	nDriver = Driver(
		'N3_bicepsBrachii_driver', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y90', 'y170'), 
		('w0', 'w90', 'wn90'))
		)

	muscle = NeferMuscle('L_bicepsBrachiiShort', nDriver)
	muscle = NeferMuscle('L_bicepsBrachiiLong', nDriver)

	print '\r\r' + scriptName + ' completed Successfully\r\r'

if __name__ == '__main__':
	main()








