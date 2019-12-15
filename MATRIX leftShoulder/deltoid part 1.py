# deltoid part 1.py
# Created by Laushon Neferkara on 1/30/13.
# Copyright (c) 2012 Skin+Bones Modeling and Rigging Company. All rights reserved.


scriptName = 'deltoid part 1.py'
print '\r' + scriptName + ' running'


import maya.mel as mel


# System name
mus = 'L_deltoid'


# Create clavicle orientation-humerus longitude (aOrient_bLong) joint sets
# Create orientConstraints for clavicle orientation joints (clavicle and scapula).

def makePoseGrp(grpName):
	
	hideList = [
		'translateX', 
		'translateY', 
		'translateZ', 
		'rotateX', 
		'rotateY', 
		'rotateZ', 
		'scaleX', 
		'scaleY', 
		'scaleZ']
	
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


def makePoseLocators(locName, locGrp):	
	for i in range(len(muscleControls)):
		mc.select(muscleControls[i], r=True)
		target = mc.xform(
			q=True, 
			worldSpace=True, 
			translation=True)
		locatorName = locName + str(i)
		mc.spaceLocator(n=locatorName)
		mc.xform(
			worldSpace=True,
			translation=(target[0], target[1], target[2]))
		mc.makeIdentity(apply=True)
		mc.parent(locatorName, locGrp)
	


longitudeList = [
	'x0', 
	'x22h', 
	'x45', 
	'x67h', 
	'x90', 
	'x112h', 
	'x135', 
	'x157h', 
	'x180', 
	'xn157h', 
	'xn22h']

muscleControls = [
	'iControlMidMus_L_deltoid_A11',
	'iControlMidMus_L_deltoid_A21',
	'iControlMidMus_L_deltoid_A31',
	'iControlMidMus_L_deltoid_A41',
	'iControlMidMus_L_deltoid_A51']


longitudeDriver = []
for i in range(len(longitudeList)):
	longitudeDriver.append('N3_humerus_long_data.' + longitudeList[i])


# Create main group
mainGrp = mus + '_pose_grp'
makePoseGrp(mainGrp)


# Create base set
baseGrp = mus + '_base_grp'
makePoseGrp(baseGrp)
mc.parent(baseGrp, mainGrp)
makePoseLocators(
	mus + '_base_control', 
	baseGrp)


# Create pose sets
for j in range(len(longitudeList)):
 
 	poseGrp = mus + '_' + longitudeList[j] + '_grp'
	makePoseGrp(poseGrp)
	mc.parent(poseGrp, mainGrp)
	makePoseLocators(
		mus + '_' + longitudeList[j] + '_control', 
		poseGrp)


# Create constraints to muscle controls
for k in range(len(muscleControls)):
	mc.pointConstraint(
		mus + '_base_control' + str(k),
		muscleControls[k])


# Create level 1 orient constraints
for k in range(len(muscleControls)):
	weightNum = 0

	for m in range(len(longitudeList)):
		mc.pointConstraint(
			mus + '_' + longitudeList[m] + '_control' + str(k),
			mus + '_base_control' + str(k),
			weight=0.0)
		
		mc.connectAttr(
			longitudeDriver[m], 
			mus + '_base_control' + str(k) + '_pointConstraint1.' + 
				mus + '_' + longitudeList[m] + '_control' + str(k) + 'W' + str(weightNum))
		
		weightNum += 1


# Completion message
print '\r' + scriptName + ' complete'


