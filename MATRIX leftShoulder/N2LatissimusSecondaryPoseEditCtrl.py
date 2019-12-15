'''
N2LatissimusPoseEditCtrl.py
Created by Laushon Neferkara on 11/20/14.
Copyright (c) 2014 Skin+Bones Modeling and Rigging Company. All rights reserved.

Create L_latissimusDorsi_secondary_pose_ctrl
'''

# Create simple group
def makeSimpleGrp(grpName, parent):
	hideList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
	mc.group(em=True, r=True, n=grpName)
	for hidden in hideList:
		mc.setAttr(grpName + '.' + hidden, keyable=False, lock=True, cb=False)
	mc.parent(grpName, parent)


class PoseEditGrp():
	'''Create a data group to control the visibility of the pose targets.'''
	def __init__(self, name, mDriver):
		self.name = name
		self.mDriver = mDriver
		# Create group
		makeSimpleGrp(self.name, 'muscle_pose_grp')
		mc.select(self.name, r=True)
		# Add attributes and connect them to driver
		for pointA in self.mDriver['axis1Points']:
			for pointB in self.mDriver['axis2Points']:
				for pointC in self.mDriver['axis3Points']:
					pose = '%s_%s_%s' % (pointA, pointB, pointC)
					mc.addAttr(shortName=pose, longName=pose, attributeType='bool', keyable=True)
					mc.connectAttr('%s.%s' % (self.mDriver['name'], pose), '%s.%s' % (self.name, pose))


def main():

	mDriver = {
		'name' : 'N2_muscleDriver1', 
		'axis1Points' : ('xn135', 'xn90', 'xn45', 'x0', 'x45', 'x90', 'x135', 'x180'), 
		'axis2Points' : ('y0', 'y45'), 
		'axis3Points' : ('wn20', 'w0', 'w20')
		}

	dataGrp = PoseEditGrp('L_latissimusDorsi_secondary_pose_ctrl', mDriver)

	print '\r\rScript completed successfully\r\r'

if __name__ == '__main__':
	main()

