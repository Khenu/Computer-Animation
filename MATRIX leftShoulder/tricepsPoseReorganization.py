# tricepsPoseReorganization.py
# Created by Laushon Neferkara on 10/16/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.


import pymel.core as pm


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
		

class ReorgPoses():
	def __init__(self, muscleMainName, muscleList, mDriver):
		self.muscleMainName = muscleMainName
		self.muscleList = muscleList
		self.mDriver = mDriver
		self.reorg()

	def reorg(self):
		# Create new group hierarchy
		topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		if mc.objExists('%s_pose_grp' % self.muscleMainName):
			mc.rename('%s_pose_grp' % self.muscleMainName, '%s_pose_grp_OLD' % self.muscleMainName)
		mainPoseGrp = SimpleGrp('%s_pose_grp' % self.muscleMainName, topPoseGrp)
		
		for pointA in self.mDriver['axis1Points']:
			poseGrpA = SimpleGrp(
				mainPoseGrp.name.replace('_pose_grp', '_%s_grp' % pointA), mainPoseGrp.name)
			for pointB in self.mDriver['axis2Points']:
				poseGrpB = SimpleGrp(
					poseGrpA.name.replace('_grp', '_%s_grp' % pointB), poseGrpA.name)
				for pointC in self.mDriver['axis3Points']:
					poseGrpC = SimpleGrp(
						poseGrpB.name.replace('_grp', '_%s_grp' % pointC), poseGrpB.name)
					for indivMus in self.muscleList:
						indivMusGrp = '%s_%s_%s_%s_grp' % (indivMus, pointA, pointB, pointC)
						# mc.setAttr('%s.visibility' % indivMusGrp, True)
						mc.parent(indivMusGrp, poseGrpC.name)


def main():

	muscleMainName = 'L_tricepsBrachii'
	
	muscleList = [
		'L_tricepsLong', 
		'L_tricepsLateral'
		]
	
	mDriver = {
		'driverName' : 'N3_muscleDriver1', 
		'axis1Points' : ('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Points' : ('y0', 'y45', 'y90', 'y135', 'y170'), 
		'axis3Points' : ('w0', 'w45', 'w90', 'wn45', 'wn90')
		}


	newStructure = ReorgPoses(muscleMainName, muscleList, mDriver)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'