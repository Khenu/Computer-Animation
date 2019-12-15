# N3 muscle system driver v6.py
# Created by Laushon Neferkara on 7/3/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.


scriptName = 'N3 muscle system driver v6.py'
print '\r' + scriptName + ' running'

# Import function module
import nm
	


# Existing scene objects
humerusCurrentlong = 'L_humerus_nspace_jnt.longitude'
humerusCurrentLat = 'L_humerus_nspace_jnt.latitude'
humerusCurrentTwist = 'L_arm_ctrl.twist'
parentGroup = 'N3_L_SHOULDER'
longData = 'N3_humerus_long_data2'
latData = 'N3_humerus_lat_data2'
twistData = 'N3_humerus_twist_data2'

# New scene objects
muscleDriver = 'N3_muscle_driver'

# Attribute lists
longList = [
	'xn45', 'x0', 'x45', 'x90', 'x135', 'x180']

latList = [
	'y0', 'y45', 'y90', 'y135', 'y170']

twistList = [
	'wn90', 'wn45', 'w0', 'w45', 'w90']

# Pose values
longitudes = [
	-45, 0, 45, 90, 135, 180]

latitudes = [
	0, 45, 90, 135, 170]

twists = [
	-90, -45, 0, 45, 90]



# Create a group with the supplied attributes (and the standard attributes locked and 
# hidden).
def makeDataGrp(grpName, attrList, parentGrp):
	
	hideList = [
		'translateX', 'translateY', 'translateZ', 
		'rotateX', 'rotateY', 'rotateZ', 
		'scaleX', 'scaleY', 'scaleZ', 
		'visibility']
	
	mc.group(
		em=True, 
		r=True, 
		n=grpName)
	
	for hidden in hideList:
		mc.setAttr(
			grpName + '.' + hidden, 
			keyable=False, 
			lock=True, 
			cb=False)
	
	for newAttr in attrList:
		mc.addAttr(
			longName=newAttr, 
			keyable=True, 
			attributeType='float')
	
	mc.parent(
		grpName, 
		parentGrp)



def makeSawtooth(drivenGrp, driver, pointNames, pointValues):
	
	mc.setDrivenKeyframe(
		drivenGrp + '.' + pointNames[0], 
		cd=driver, 
		dv=pointValues[0], 
		v=1, 
		itt='linear', 
		ott='linear')

	mc.setDrivenKeyframe(
		drivenGrp + '.' + pointNames[0], 
		cd=driver, 
		dv=pointValues[1], 
		v=0, 
		itt='linear', 
		ott='linear')

	for i in range(1, len(pointNames) - 1):
		
		mc.setDrivenKeyframe(
			drivenGrp + '.' + pointNames[i], 
			cd=driver, 
			dv=pointValues[i - 1], 
			v=0, 
			itt='linear', 
			ott='linear')

		mc.setDrivenKeyframe(
			drivenGrp + '.' + pointNames[i], 
			cd=driver, 
			dv=pointValues[i], 
			v=1, 
			itt='linear', 
			ott='linear')

		mc.setDrivenKeyframe(
			drivenGrp + '.' + pointNames[i], 
			cd=driver, 
			dv=pointValues[i + 1], 
			v=0, 
			itt='linear', 
			ott='linear')

	mc.setDrivenKeyframe(
		drivenGrp + '.' + pointNames[-1], 
		cd=driver, 
		dv=pointValues[-2], 
		v=0, 
		itt='linear', 
		ott='linear')

	mc.setDrivenKeyframe(
		drivenGrp + '.' + pointNames[-1], 
		cd=driver, 
		dv=pointValues[-1], 
		v=1, 
		itt='linear', 
		ott='linear')




# Construct muscleDriver attribute list
muscleDriverList = []
for i in range(len(longList)): 
	for j in range(len(latList)):
		muscleDriverList.append(longList[i] + '_' + latList[j])

makeDataGrp(
	muscleDriver, 
	muscleDriverList, 
	parentGroup)


# Construct muscleShapeDriver attribute list
# muscleShapeDriverList = []
# for i in range(len(longList)): 
# 	for j in range(len(latList)):
# 		for k in range(len(twistList)):
# 			muscleShapeDriverList.append(longList[i] + '_' + latList[j] + '_' + 
# 				twistList[k])

# makeDataGrp(
# 	muscleShapeDriver, 
# 	muscleShapeDriverList, 
# 	parentGroup)


# muscleDriver
for i in range(len(longList)): 
	for j in range(len(latList)):
		nm.multiply(
			'N3_muscleDriver_multiply_' + longList[i] + '_' + latList[j], 
			longData + '.' + longList[i], 
			latData + '.' + latList[j], 
			muscleDriver + '.' + longList[i] + '_' + latList[j])


# muscleShapeDriver
# for i in range(len(longList)): 
# 	for j in range(len(latList)):
# 		for k in range(len(twistList)):
# 			nm.multiply(
# 				'N3_muscleShapeDriver_multiply_' + longList[i] + '_' + latList[j] + 
# 					'_' + twistList[k], 
# 				muscleSdkDriver + '.' + longList[i] + '_' + twistList[k], 
# 				latData + '.' + latList[j], 
# 				muscleShapeDriver + '.' + longList[i] + '_' + latList[j] +
# 					'_' + twistList[k])




# multiply(nodeName, input1, input2, output):




print '\r\r' + scriptName + ' completed Successfully\r\r'

