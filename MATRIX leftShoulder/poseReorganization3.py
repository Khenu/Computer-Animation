# poseReorganization3.py
# Created by Laushon Neferkara on 2/5/14.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''
Group all of the poses per control and constrained just that group.


'''

import pymel.core as pm 	# Used in SimpleGrp()


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
	def __init__(self, muscleGroupName, muscleDataList, mDriver):
		self.muscleGroupName = muscleGroupName
		self.muscleDataList = muscleDataList
		self.mDriver = mDriver
		self.deleteParentConstraints()
		self.reorg()

	

	def deleteParentConstraints(self):
		for muscleData in self.muscleDataList:
			for pointA in self.mDriver['axis1Points']:
				for pointB in self.mDriver['axis2Points']:
					for pointC in self.mDriver['axis3Points']:
						for ctrlNum in range(1, muscleData[1] + 1):
							grpConstraint = '%s_%s_%s_%s_control%s_grp_parentConstraint1' % (muscleData[0], pointA, pointB, pointC, ctrlNum)
							mc.delete(grpConstraint)
	



	def reorg(self):
		# Create new group hierarchy
		topPoseGrp = 'muscle_pose_grp'		# Already exists in the scene
		
		for muscleData in self.muscleDataList:
			muscleName = muscleData[0]
			numCtrls = muscleData[1]

			# Create new group for poses
			musclePoseGrp = '%s_pose_grp' % muscleName
			SimpleGrp(musclePoseGrp, topPoseGrp)
			# 
			for ctrlNum in range(1, numCtrls + 1):
				# Create a new group for all of the poses for each control. Parent constrain the group to the AUTO group.
				ctrlPoseGrp = '%s_control%s_pose_grp' % (muscleName, str(ctrlNum))
				SimpleGrp(ctrlPoseGrp, musclePoseGrp, lockTrans=False)
				autoGrpName = 'grpiControlMidMus_%s%sAUTO1' % (muscleName, str(ctrlNum))
				mc.parentConstraint(autoGrpName, ctrlPoseGrp, maintainOffset=False)
				# 
				for pointA in self.mDriver['axis1Points']:
					poseGrpA = '%s_control%s_%s_pose_grp' % (muscleName, str(ctrlNum), pointA)
					SimpleGrp(poseGrpA, ctrlPoseGrp)
					for pointB in self.mDriver['axis2Points']:
						poseGrpB = '%s_control%s_%s_%s_pose_grp' % (muscleName, str(ctrlNum), pointA, pointB)
						SimpleGrp(poseGrpB, poseGrpA)
						for pointC in self.mDriver['axis3Points']:
							poseGrpC = '%s_control%s_%s_%s_%s_pose_grp' % (muscleName, str(ctrlNum), pointA, pointB, pointC)
							SimpleGrp(poseGrpC, poseGrpB)
							mc.setAttr(poseGrpC + '.visibility', False)
							mc.parent('%s_control%s_%s_%s_%s_target' % (muscleName, ctrlNum, pointA, pointB, pointC), poseGrpC)


def main():
	
	mDriver = {
		'driverName' : 'N3_muscleDriver1', 
		'axis1Points' : ('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Points' : ('y0', 'y45', 'y90', 'y135', 'y170'), 
		'axis3Points' : ('w0', 'w45', 'w90', 'wn45', 'wn90')
		}


	# muscleGroupName = 'L_pectoralis'
	# muscleData = [
	# ['L_pectoralisA', 6],
	# ['L_pectoralisB', 6],
	# ['L_pectoralisC', 6],
	# ['L_pectoralisD', 6],
	# ['L_pectoralisE', 6],
	# ['L_pectoralisF', 6],
	# ['L_pectoralisG', 6],
	# ['L_pectoralisH', 6],
	# ['L_pectoralisJ', 6],
	# ['L_pectoralisK', 7],
	# ['L_pectoralisL', 7],
	# ['L_pectoralisM', 7]
	# ]

	# muscleGroupName = 'L_coracobrachialis'
	# muscleData = [
	# ['L_coracobrachialisB', 5]
	# ]

	# muscleGroupName = 'L_trapeziusLower'
	# muscleData = [
	# 	['L_trapeziusO', 4], 
	# 	['L_trapeziusP', 4], 
	# 	['L_trapeziusQ', 4], 
	# 	['L_trapeziusR', 4], 
	# 	['L_trapeziusS', 4], 
	# 	]

	muscleGroupName = 'L_bicepsBrachiiShort'
	muscleData = [
		['L_bicepsBrachiiShort', 5]
		]

	newStructure = ReorgPoses(muscleGroupName, muscleData, mDriver)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'








