# savePoseToFile.py
# Created by Laushon Neferkara on 1/24/14.
# Copyright (c) 2014 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''

'''

# import collections
from collections import namedtuple
import pickle

MuscleData = namedtuple('MuscleInfo', ['musclename', 'numClrls'])
PoseData = namedtuple('PoseData', ['musclename', 'ctrlNum', 'transX', 'transY', 'transZ'])

def main():
	poseName = 'x90_y135_wn45'
	muscleList = [
		# MuscleData('L_deltoidAnteriorA', 5), 
		# MuscleData('L_deltoidAnteriorB', 5), 
		# MuscleData('L_deltoœidAnteriorC', 5), 
		# MuscleData('L_deltoidLateralA', 5), 
		# MuscleData('L_deltoidLateralB', 5), 
		# MuscleData('L_deltoidLateralC', 5), 
		MuscleData('L_deltoidPosteriorA', 5), 
		MuscleData('L_deltoidPosteriorB', 5), 
		MuscleData('L_deltoidPosteriorC', 5), 
		MuscleData('L_deltoidPosteriorD', 5),  
		MuscleData('L_pectoralisMajor2A', 6), 
		MuscleData('L_pectoralisMajor2B', 6), 
		MuscleData('L_pectoralisMajor2C', 6), 
		MuscleData('L_pectoralisMajor2D', 6), 
		MuscleData('L_pectoralisMajor2E', 6), 
		MuscleData('L_pectoralisMajor2F', 6), 
		MuscleData('L_pectoralisMajor2G', 6), 
		MuscleData('L_pectoralisMajor2H', 6), 
		MuscleData('L_pectoralisMajor2I', 6), 
		MuscleData('L_pectoralisMajor2J', 6), 
		MuscleData('L_pectoralisMajor2K', 6)
		# MuscleData('L_latissimusDorsi2A', 6),
		# MuscleData('L_latissimusDorsi2B', 6),
		# MuscleData('L_latissimusDorsi2C', 7),
		# MuscleData('L_latissimusDorsi2D', 7),
		# MuscleData('L_latissimusDorsi2E', 8),
		# MuscleData('L_latissimusDorsi2F', 9),
		# MuscleData('L_latissimusDorsi2G', 9),
		# MuscleData('L_latissimusDorsi2H', 7),
		# MuscleData('L_teresMajor', 5), 
		# MuscleData('L_teresMinor2', 5), 
		# MuscleData('L_infraspinatusA', 5), 
		# MuscleData('L_infraspinatusB', 5), 
		# MuscleData('L_infraspinatusC', 5), 
		# MuscleData('L_coracobrachialis2', 5), 
		# MuscleData('L_brachialisA', 5), 
		# MuscleData('L_bicepsBrachiiShort2', 6), 
		# MuscleData('L_bicepsBrachiiLong2', 6)
		# MuscleData('L_tricepsLateral', 5), 
		# MuscleData('L_tricepsLong', 5)
		]

	# Open file
	fileName = '/Users/laushon/Documents/Animation/gina 3.0/gina_3.0_project/scenes/pose_%s.txt' % poseName
	dataFile = open(fileName, 'w')
	# pickle.dump(poseName, dataFile)
	posePointList = []
	for muscle in muscleList: 
		for cNum in range(1, muscle.numClrls + 1):
			sourceTarget = '%s_control%s_%s_target' % (muscle.musclename, cNum, poseName)
			posePoint = PoseData(
				muscle.musclename, 
				cNum,
				mc.getAttr('%s.translateX' % sourceTarget), 
				mc.getAttr('%s.translateY' % sourceTarget), 
				mc.getAttr('%s.translateZ' % sourceTarget)
				)
			posePointList.append(posePoint)
	pickle.dump(posePointList, dataFile)

	# for muscle in muscleList: 
	# 	for cNum in range(1, muscle.numClrls + 1):
	# 		sourceTarget = '%s_control%s_%s_target' % (muscle.musclename, cNum, poseName)
	# 		posePoint = PoseData(
	# 			muscle.musclename, 
	# 			cNum,
	# 			mc.getAttr('%s.translateX' % sourceTarget), 
	# 			mc.getAttr('%s.translateY' % sourceTarget), 
	# 			mc.getAttr('%s.translateZ' % sourceTarget)
	# 			)
	# 		pickle.dump(posePoint, dataFile)

	dataFile.close()
			

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'










