# readPoseFromFile.py
# Created by Laushon Neferkara on 1/24/14.
# Copyright (c) 2014 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''

'''

# import collections
from collections import namedtuple
import pickle

poseName = 'x90_y135_wn90'
MuscleData = namedtuple('MuscleInfo', ['musclename', 'numClrls'])
PoseData = namedtuple('PoseData', ['musclename', 'ctrlNum', 'transX', 'transY', 'transZ'])

def main():

	# Open file
	fileName = '/Users/laushon/Documents/Animation/gina 3.0/gina_3.0_project/scenes/pose_%s.txt' % poseName
	dataFile = open(fileName)
	poseData = pickle.load(dataFile)

	for posePoint in poseData: 
		destTarget = '%s_control%s_%s_target' % (posePoint.musclename, posePoint.ctrlNum, poseName)
		mc.setAttr('%s.translateX' % destTarget, posePoint.transX)
		mc.setAttr('%s.translateY' % destTarget, posePoint.transY)
		mc.setAttr('%s.translateZ' % destTarget, posePoint.transZ)
			

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'

