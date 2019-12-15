def delExTargetConnections(muscleData):
	for cIndex in range(1, muscleData['numCtrls'] + 1):
		mc.delete('iControlMidMus_%s%s1_pointConstraint1' % (muscleData['name'], str(cIndex)))
		# mc.delete('iControlMidMus_%s%s1_crossSectionREST_blendShape' % (muscleData['name'], str(cIndex)))

def deleteUnusedPoses(muscleData):
	mc.delete('%s_pose_grp' % muscleData['name'])
	

def main():
	
	muscleData1 = {
		'name'			:	'L_teresMinor',
		'numCtrls'		:	5
		}

	muscleData2 = {
		'name'			:	'L_coracobrachialis',
		'numCtrls'		:	5
		}

	# delExTargetConnections(muscleData1)
	# deleteUnusedPoses(muscleData1)

	delExTargetConnections(muscleData2)
	deleteUnusedPoses(muscleData2)


	print '\r\rScript completed successfully\r\r'

if __name__ == "__main__":
	main()
	

##############################################################



def delExTargetConnections(muscleData):
	for cIndex in range(1, muscleData['numCtrls'] + 1):
		mc.delete('iControlMidMus_%s%s1_pointConstraint1' % (muscleData['name'], str(cIndex)))
		mc.delete('iControlMidMus_%s%s1_crossSectionREST_blendShape' % (muscleData['name'], str(cIndex)))

def deleteUnusedPoses(muscleData):
	mc.delete('%s_pose_grp' % muscleData['name'])
	

def main():
	
	muscleData1 = {
		'name'			:	'L_pectoralisMajorE',
		'numCtrls'		:	5
		}

	delExTargetConnections(muscleData1)
	deleteUnusedPoses(muscleData1)

	print '\r\rScript completed successfully\r\r'

if __name__ == "__main__":
	main()
	
