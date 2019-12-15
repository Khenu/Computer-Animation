# N3 brachialis driver.py
# Created by Laushon Neferkara on 8/14/13.
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


class NDriver2Axes():
	'''Create driver with 2 axes.'''
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
				driverAttrList.append('%s_%s' % (axis1Point, axis2Point))

		self.makeDataGrp(driverAttrList)

	def makeMultiplyNodes(self):
		for axis1Point in self.nData['axis1Pts']:
			for axis2Point in self.nData['axis2Pts']:
				nm.multiply(
					# multiply(nodeName, input1, input2, output)
					'N3_bicepsBrachii_multiply_%s_%s' % (axis1Point, axis2Point), 
					'%s.%s' % (self.nData['axis1Name'], axis1Point), 
					'%s.%s' % (self.nData['axis2Name'], axis2Point), 
					'%s.%s_%s' % (self.nData['driverName'], axis1Point, axis2Point)
					)

def main():
	scriptName = 'N3 brachialis driver.py'
	print '\r' + scriptName + ' running'

	bbDriver = NDriver2Axes({
		'driverName'	: 	'N3_brachialis_driver', 
		'axis1Name'		: 	'N3_humerus_long_data2',						# Existing
		'axis1Pts'		: 	('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Name'		: 	'N3_biceps_lat_data',
		'axis2Pts'		: 	('y0', 'y90', 'y170')
		})

	print '\r\r' + scriptName + ' completed Successfully\r\r'


if __name__ == '__main__':
	main()