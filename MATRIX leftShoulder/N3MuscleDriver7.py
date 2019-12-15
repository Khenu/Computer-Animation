# N3MuscleDriver6.py
# Created by Laushon Neferkara on 10/10/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.


# Import function module
import nm


class AxisData():
	'''Represents a axis data group in the the scene'''
	def __init__(self, grpName, dataPts, driver):
		self.grpName = grpName
		self.dataPts = dataPts
		self.driver = driver
		self.makeDataGrp()
		self.makeSawtooth()

	def makeDataGrp(self):
		'''Create a group with the supplied attributes (and the standard attributes locked and 
		hidden).'''

		hideList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ', 'visibility']

		parentGrp = 'N3_L_SHOULDER'
		
		mc.group(em=True, r=True, n=self.grpName)
		
		for hidden in hideList:
			mc.setAttr(self.grpName + '.' + hidden, keyable=False, lock=True, cb=False)
		
		for newAttr in self.dataPts:
			mc.addAttr(longName=newAttr[0], keyable=True, attributeType='float')
		
		mc.parent(self.grpName, parentGrp)

	def makeSawtooth(self):
		# drivenGrp, driver, pointNames, self.dataPts
		mc.setDrivenKeyframe(
			self.grpName + '.' + self.dataPts[0][0], 
			cd=self.driver, 
			dv=self.dataPts[0][1], 
			v=1, 
			itt='linear', ott='linear')

		mc.setDrivenKeyframe(
			self.grpName + '.' + self.dataPts[0][0], 
			cd=self.driver, 
			dv=self.dataPts[1][1], 
			v=0, 
			itt='linear', ott='linear')

		for i in range(1, len(self.dataPts) - 1):
			
			mc.setDrivenKeyframe(
				self.grpName + '.' + self.dataPts[i][0], 
				cd=self.driver, 
				dv=self.dataPts[i - 1][1], 
				v=0, 
				itt='linear', ott='linear')

			mc.setDrivenKeyframe(
				self.grpName + '.' + self.dataPts[i][0], 
				cd=self.driver, 
				dv=self.dataPts[i][1], 
				v=1, 
				itt='linear', ott='linear')

			mc.setDrivenKeyframe(
				self.grpName + '.' + self.dataPts[i][0], 
				cd=self.driver, 
				dv=self.dataPts[i + 1][1], 
				v=0, 
				itt='linear', ott='linear')

		mc.setDrivenKeyframe(
			self.grpName + '.' + self.dataPts[-1][0], 
			cd=self.driver, 
			dv=self.dataPts[-2][1], 
			v=0, 
			itt='linear', ott='linear')

		mc.setDrivenKeyframe(
			self.grpName + '.' + self.dataPts[-1][0], 
			cd=self.driver, 
			dv=self.dataPts[-1][1], 
			v=1, 
			itt='linear', 
			ott='linear')


class NDriver3Axes():
	'''Create driver with 3 axes.'''
	def __init__(self, nData):
		self.nData = nData
		self.makeDriver()
		self.makeMultiplyNodes()
	
	def makeDataGrp(self, driverAttrList):
		'''Create a group with the supplied attributes (and the standard attributes locked and 
		hidden).'''

		hideList = [
			'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 
			'scaleX', 'scaleY', 'scaleZ', 'visibility']

		parentGrp = 'N3_L_SHOULDER'
		
		mc.group(em=True, r=True, n=self.nData['driverName'])
		
		for hidden in hideList:
			mc.setAttr(self.nData['driverName'] + '.' + hidden, keyable=False, lock=True, cb=False)
		
		for newAttr in driverAttrList:
			mc.addAttr(longName=newAttr, keyable=True, attributeType='float')
		
		mc.parent(self.nData['driverName'], parentGrp)
	
	def makeDriver(self):
		# Construct muscleDriver attribute list
		driverAttrList = []
		for axis1Point in self.nData['axis1Pts']:
			for axis2Point in self.nData['axis2Pts']:
				for axis3Point in self.nData['axis3Pts']:
					driverAttrList.append('%s_%s_%s' % (axis1Point, axis2Point, axis3Point))

		self.makeDataGrp(driverAttrList)

	def makeMultiplyNodes(self):
		for axis1Point in self.nData['axis1Pts']:
			for axis2Point in self.nData['axis2Pts']:
				for axis3Point in self.nData['axis3Pts']:
					nm.multiply3(
						# multiply3(nodeName, input1, input2, input3, output)
						'%s_multiply_%s_%s_%s' % (self.nData['driverName'], axis1Point, axis2Point, axis3Point), 
						'%s.%s' % (self.nData['axis1Name'], axis1Point), 
						'%s.%s' % (self.nData['axis2Name'], axis2Point), 
						'%s.%s' % (self.nData['axis3Name'], axis3Point),  
						'%s.%s_%s_%s' % (self.nData['driverName'], axis1Point, axis2Point, axis3Point))

def main():

	twistData = 'N3_twist_data3'
	twistList = (('wn40', -40), ('wn50', -50), ('wn60', -60), ('wn70', -70), ('wn80', -80), ('wn90', -90))
	humerusCurrentTwist = 'L_arm_ctrl.twist'
	twists = [-40, -50, -60, -70, -80, -90]


	# nm.makeDataGrp(twistData, twistList, parentGroup)
	# nm.makeSawtooth(twistData, humerusCurrentTwist, twistList, twists)

	# newData = AxisData(twistData, twistList, humerusCurrentTwist)

	bbDriver = NDriver3Axes({
		'driverName'	: 	'N3_muscleDriver6', 
		'axis1Name'		: 	'N3_humerus_long_data2',						# Existing
		'axis1Pts'		: 	('x90', ), 
		'axis2Name'		: 	'N3_humerus_lat_data2',							# Existing
		'axis2Pts'		: 	('y170', ), 
		'axis3Name'		: 	'N3_twist_data3', 
		'axis3Pts'		: 	('wn40', 'wn50', 'wn60', 'wn70', 'wn80', 'wn90')
		})

	print '\r\rScript completed successfully\r\r'


if __name__ == '__main__':
	main()



