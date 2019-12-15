# poseEditCtrl.py
# Created by Laushon Neferkara on 12/12/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

# Create simple group
def makeSimpleGrp(grpName, parent):

	hideList = [
		'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ']

	mc.group(em=True, r=True, n=grpName)

	for hidden in hideList:
		mc.setAttr(grpName + '.' + hidden, keyable=False, lock=True, cb=False)

	mc.parent(grpName, parent)


def createPoseEditGrp(ctrlGrp, poseList):
	makeSimpleGrp(ctrlGrp, 'muscle_pose_grp')
	mc.select(ctrlGrp, r=True)
	for pose in poseList:
		mc.addAttr(shortName=pose, longName=pose, attributeType='bool', keyable=True)


def main():

	ctrlGrp = 'L_shoulder_pose_ctrl'

	poseList = [
		# x0 group
		'x0_y0_w0', 
		'x0_y0_w45', 
		'x0_y0_w90', 
		'x0_y0_wn45', 
		'x0_y0_wn90', 
		
		'x0_y45_w0', 
		'x0_y45_w45', 
		'x0_y45_w90', 
		'x0_y45_wn45', 
		'x0_y45_wn90',

		'x0_y90_w0', 
		'x0_y90_w45', 
		'x0_y90_w90', 
		'x0_y90_wn45',
		'x0_y90_wn90',

		'x0_y135_w0', 
		'x0_y135_w45', 
		'x0_y135_w90', 
		'x0_y135_wn45',
		'x0_y135_wn90',

		'x0_y170_w0', 
		'x0_y170_w45', 
		'x0_y170_w90', 
		'x0_y170_wn45',
		'x0_y170_wn90',

		# x45 group
		'x45_y0_w0', 
		'x45_y0_w45', 
		'x45_y0_w90', 
		'x45_y0_wn45', 
		'x45_y0_wn90', 
		
		'x45_y45_w0', 
		'x45_y45_w45', 
		'x45_y45_w90', 
		'x45_y45_wn45', 
		'x45_y45_wn90',

		'x45_y90_w0', 
		'x45_y90_w45', 
		'x45_y90_w90', 
		'x45_y90_wn45',	
		'x45_y90_wn90',

		'x45_y135_w0', 
		'x45_y135_w45', 
		'x45_y135_w90', 
		'x45_y135_wn45',	
		'x45_y135_wn90',

		'x45_y170_w0', 
		'x45_y170_w45', 
		'x45_y170_w90', 
		'x45_y170_wn45',
		'x45_y170_wn90',

		# x90 group
		'x90_y0_w0', 
		'x90_y0_w45', 
		'x90_y0_w90', 
		'x90_y0_wn45', 
		'x90_y0_wn90', 
		
		'x90_y45_w0', 
		'x90_y45_w45', 
		'x90_y45_w90', 
		'x90_y45_wn45', 
		'x90_y45_wn90',	

		'x90_y90_w0', 	
		'x90_y90_w45', 
		'x90_y90_w90', 
		'x90_y90_wn45',	
		'x90_y90_wn90',	

		'x90_y135_w0', 	
		'x90_y135_w45', 
		'x90_y135_w90', 
		'x90_y135_wn45',	
		'x90_y135_wn90',	

		'x90_y170_w0', 	
		'x90_y170_w45', 
		'x90_y170_w90', 
		'x90_y170_wn45', 
		'x90_y170_wn90', 

		# x135 group
		'x135_y0_w0', 
		'x135_y0_w45', 
		'x135_y0_w90', 
		'x135_y0_wn45', 
		'x135_y0_wn90', 
		
		'x135_y45_w0', 
		'x135_y45_w45', 
		'x135_y45_w90', 
		'x135_y45_wn45', 
		'x135_y45_wn90', 

		'x135_y90_w0', 
		'x135_y90_w45', 
		'x135_y90_w90', 
		'x135_y90_wn45',
		'x135_y90_wn90',

		'x135_y135_w0', 
		'x135_y135_w45', 
		'x135_y135_w90', 
		'x135_y135_wn45',
		'x135_y135_wn90',

		'x135_y170_w0', 
		'x135_y170_w45', 
		'x135_y170_w90', 
		'x135_y170_wn45',
		'x135_y170_wn90',

		# x180 group
		'x180_y0_w0', 
		'x180_y0_w45', 
		'x180_y0_w90', 
		'x180_y0_wn45', 
		'x180_y0_wn90', 
		
		'x180_y45_w0', 
		'x180_y45_w45', 
		'x180_y45_w90', 
		'x180_y45_wn45', 
		'x180_y45_wn90', 

		'x180_y90_w0', 
		'x180_y90_w45', 
		'x180_y90_w90', 
		'x180_y90_wn45',
		'x180_y90_wn90',

		'x180_y135_w0', 
		'x180_y135_w45', 
		'x180_y135_w90', 
		'x180_y135_wn45',
		'x180_y135_wn90',

		'x180_y170_w0', 
		'x180_y170_w45', 
		'x180_y170_w90', 
		'x180_y170_wn45',
		'x180_y170_wn90',

		# xn45 group
		'xn45_y0_w0', 
		'xn45_y0_w45', 
		'xn45_y0_w90', 
		'xn45_y0_wn45', 
		'xn45_y0_wn90', 
		
		'xn45_y45_w0', 
		'xn45_y45_w45', 
		'xn45_y45_w90', 
		'xn45_y45_wn45', 
		'xn45_y45_wn90',

		'xn45_y90_w0', 
		'xn45_y90_w45', 
		'xn45_y90_w90', 
		'xn45_y90_wn45',
		'xn45_y90_wn90',

		'xn45_y135_w0', 
		'xn45_y135_w45', 
		'xn45_y135_w90', 
		'xn45_y135_wn45',
		'xn45_y135_wn90',

		'xn45_y170_w0', 
		'xn45_y170_w45', 
		'xn45_y170_w90', 
		'xn45_y170_wn45',
		'xn45_y170_wn90',
		]

	createPoseEditGrp(ctrlGrp, poseList)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'








