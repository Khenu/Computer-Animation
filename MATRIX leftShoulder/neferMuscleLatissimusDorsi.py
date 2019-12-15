# neferMuscleLatissimusDorsi.py
# Created by Laushon Neferkara on 10/18/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''
Added crossSectionRange

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
		

class MuscleControl():
	'''Represents a Maya Muscle control of a neferMuscle.'''
	def __init__(self, muscleName, cIndex, nDriver):	
		self.muscleName = muscleName		
		self.name = 'iControlMidMus_%s%s1' % (muscleName, str(cIndex + 1))
		self.autoGrpName = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(cIndex + 1))
		self.nDriver = nDriver
		self.targetList = []
		self.driverList = []
		# Disable jiggle
		mc.setAttr('%s.jiggle' % self.name, 0)

	def addTarget(self, target):
		self.targetList.append(target)
	
	def addDriver(self, driver):
		self.driverList.append(driver)

	def connectTargets(self):
		'Create point constraint to all of the targets'
		mc.pointConstraint(self.targetList, self.name, weight=0.0)

	def connectDriver(self):
		'Connect the Maya Muscle control point constraint to the driver.'
		for pIndex in range(len(self.targetList)):
			mc.connectAttr(
				'%s.%s' % (self.nDriver, self.driverList[pIndex]),
				'%s_pointConstraint1.%sW%s' % (self.name, self.targetList[pIndex], str(pIndex))
				)
							

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
		mc.blendShape(self.targetList[0], self.name, name = self.blendShape)
		# Add the remaining targets to the blend shape node
		for bIndex in range(1, len(self.targetList)):
			mc.blendShape(self.blendShape, edit=True, 
				t=(self.name, bIndex, self.targetList[bIndex], 1.0))

	def connectDriver(self):
		'Connect the Maya Muscle control blend shape node to the driver.'
		for pIndex in range(len(self.targetList)):
			mc.connectAttr(
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
		mc.duplicate(self.baseObj.name, n=self.name)

		# Delete the child squash and stretch curves. (Cross sections do not have.) 
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


class MuscleCtrlTarget(SceneTarget):
	'''Represents a target for a Maya Muscle control.'''
	def __init__(self, name, musCtrl, parentGrpName):	
		SceneTarget.__init__(self, name, musCtrl, parentGrpName)
		# Lock unused transforms
		mc.setAttr('%s.rotate' % self.name, lock=True)
		mc.setAttr('%s.scale' % self.name, lock=True)
		# Make visible
		mc.setAttr('%s.visibility' % self.name, True)



class MuscleCrossTarget(SceneTarget):
	'''Represents a target for a Maya Muscle cross section.'''
	def __init__(self, name, musCross, parentGrpName):	
		SceneTarget.__init__(self, name, musCross, parentGrpName)
		# Lock all transforms
		mc.setAttr('%s.translate' % self.name, lock=True)
		mc.setAttr('%s.rotate' % self.name, lock=True)
		mc.setAttr('%s.scale' % self.name, lock=True)
		# Make visible
		mc.setAttr('%s.visibility' % self.name, True)


class NeferMuscle():
	'''Represents a neferMuscle: a Maya Muscle that is controlled by a multi-variable
	 pose controller.'''
	def __init__(self, muscleData):
		self.muscleName = muscleData['muscleName']
		self.numCtrls =  muscleData['numCtrls']
		self.muscleDriver =  muscleData['driverData'].name
		self.data =  muscleData['driverData'].data
		self.crossSectionRange =  muscleData['crossSectionRange']
		self.createMusCtrlObjs()
		self.setupMayaMus()
		self.createPoses()
		self.connectDriver()
		
	def createMusCtrlObjs(self):
		# Create objects to represent the Maya Muscle controls and cross sections and place in list
		self.musCtrls = []
		self.musCross = []
		for cIndex in range(self.numCtrls):
			self.musCtrls.append(MuscleControl(self.muscleName, cIndex, self.muscleDriver))
			self.musCross.append(MuscleCrossSection(self.muscleName, cIndex, self.muscleDriver))

	def setupMayaMus(self):
		# Set Based On attribute of Maya Muscle to pose
	  	mc.setAttr('cMuscleCreatorMus_%s1.basedOn' % self.muscleName, 1)	

	def createPoses(self):

		def _createCtrlCrossPoses(parentGrpName, driverPt):
			'Create pose groups for each muscle control/cross section pair.'
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
				
				# Create cross section target
				if self.crossSectionRange[0] <= dIndex + 1 <= self.crossSectionRange[1]:
					crossTargetName = '%s_crossSection%s_%s_target' % (self.muscleName, str(dIndex + 1), 
						driverPt)
					crossTarget = MuscleCrossTarget(crossTargetName, self.musCross[dIndex], ctrlTarget.name)

				# Add driver to driver list
				self.musCtrls[dIndex].addDriver(driverPt)
				if self.crossSectionRange[0] <= dIndex + 1 <= self.crossSectionRange[1]:
					self.musCross[dIndex].addDriver(driverPt)

		# Create the main pose group for the muscle
		topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		mainPoseGrp = SimpleGrp('%s_pose_grp' % self.muscleName, topPoseGrp)

		# Create the poses within pose groups. Select based on number of axes.
		for pointA in self.data[0]:
			poseGrpA = SimpleGrp(
				mainPoseGrp.name.replace('_pose_grp', '_%s_grp' % pointA), 
				mainPoseGrp.name)
			if len(self.data) == 1:
				poseGrpA.makeInvisible()
				driverPt = pointA
				_createCtrlCrossPoses(poseGrpA.name, driverPt)
			else:
				for pointB in self.data[1]:
					poseGrpB = SimpleGrp(
						poseGrpA.name.replace('_grp', '_%s_grp' % pointB), 
						poseGrpA.name)
					if len(self.data) == 2:
						poseGrpB.makeInvisible()
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
									poseGrpD.makeInvisible()
									driverPt = '%s_%s_%s_%s' % (pointA, pointB, pointC, pointD)
									_createCtrlCrossPoses(poseGrpD.name, driverPt)

	def connectDriver(self):
		# Connect poses to muscle control and muscle cross sections. Create point constraint and 
		# blend shape node
		for index in range(self.numCtrls):
			self.musCtrls[index].connectTargets()
			if self.crossSectionRange[0] <= index + 1 <= self.crossSectionRange[1]:
				self.musCross[index].connectTargets()

		# Connect driver attributes to point constraint and blend shape node
		for index in range(self.numCtrls):
			self.musCtrls[index].connectDriver()
			if self.crossSectionRange[0] <= index + 1 <= self.crossSectionRange[1]:
				self.musCross[index].connectDriver()





def main():

	n3driver = Driver(
		'N3_muscleDriver1', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y45', 'y90', 'y135', 'y170'), 
		('w0', 'w45', 'w90', 'wn45', 'wn90'))
		)

	muscleData1 = {
		'muscleName': 'L_latissimusDorsi2A', 
		'numCtrls': 6, 
		'driverData': n3driver,
		'crossSectionRange': (1, 6)
		}
	muscleData2 = {
		'muscleName': 'L_latissimusDorsi2B', 
		'numCtrls': 6, 
		'driverData': n3driver,
		'crossSectionRange': (1, 6)
		}
	muscleData3 = {
		'muscleName': 'L_latissimusDorsi2C', 
		'numCtrls': 7, 
		'driverData': n3driver,
		'crossSectionRange': (3, 7)
		}
	muscleData4 = {
		'muscleName': 'L_latissimusDorsi2D', 
		'numCtrls': 7, 
		'driverData': n3driver,
		'crossSectionRange': (3, 7)
		}
	muscleData5 = {
		'muscleName': 'L_latissimusDorsi2E', 
		'numCtrls': 8, 
		'driverData': n3driver,
		'crossSectionRange': (4, 8)
		}
	muscleData6 = {
		'muscleName': 'L_latissimusDorsi2F', 
		'numCtrls': 9, 
		'driverData': n3driver,
		'crossSectionRange': (5, 9)
		}
	muscleData7 = {
		'muscleName': 'L_latissimusDorsi2G', 
		'numCtrls': 9, 
		'driverData': n3driver,
		'crossSectionRange': (5, 9)
		}
	muscleData8 = {
		'muscleName': 'L_latissimusDorsi2H', 
		'numCtrls': 7, 
		'driverData': n3driver,
		'crossSectionRange': (1, 7)
		}

	muscle = NeferMuscle(muscleData4)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'

