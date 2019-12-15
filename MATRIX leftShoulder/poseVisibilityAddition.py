# poseVisibilityAddition.py
# Created by Laushon Neferkara on 5/15/14.
# Copyright (c) 2014 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''


'''


def main():

	poseList = [
		'x45_y45_w90', 
		'x45_y45_wn90'
		]

	driverName = 'N3_muscleDriver1'
	poseCtrl = 'L_shoulder_pose_ctrl'

	for pose in poseList:
		mc.connectAttr('%s.%s' % (driverName, pose), '%s.%s' % (poseCtrl, pose))


if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'


