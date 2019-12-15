# shoulderY0BlendShapeCopy.py
# Created by Laushon Neferkara on 11/25/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''

'''



def deleteNefer(muscleName, numCtrls):
	for cIndex in range(numCtrls):
		# pointConNode = 'iControlMidMus_%s%s1_pointConstraint1' % (muscleName, str(cIndex + 1))
		# if mc.objExists(pointConNode):
		# 	mc.delete(pointConNode)
		bShapeNode = 'iControlMidMus_%s%s1_crossSectionREST_blendShape' % (muscleName, str(cIndex + 1))
		if mc.objExists(bShapeNode):
			mc.delete(bShapeNode)




muscleList = [
	['L_deltoidAnteriorA', 5], 
	['L_deltoidAnteriorB', 5], 
	['L_deltoidAnteriorC', 5], 
	['L_deltoidLateralA', 5], 
	['L_deltoidLateralB', 5], 
	['L_deltoidLateralC', 5], 
	['L_deltoidPosteriorA', 5], 
	['L_deltoidPosteriorB', 5], 
	['L_deltoidPosteriorC', 5], 
	['L_deltoidPosteriorD', 5], 
	['L_pectoralisMajor2A', 6], 
	['L_pectoralisMajor2B', 6], 
	['L_pectoralisMajor2C', 6], 
	['L_pectoralisMajor2D', 6], 
	['L_pectoralisMajor2E', 6], 
	['L_pectoralisMajor2F', 6], 
	['L_pectoralisMajor2G', 6], 
	['L_pectoralisMajor2H', 6], 
	['L_pectoralisMajor2I', 6], 
	['L_pectoralisMajor2J', 6], 
	['L_pectoralisMajor2K', 6], 
	['L_latissimusDorsi2A', 6],
	['L_latissimusDorsi2B', 6],
	['L_latissimusDorsi2C', 7],
	['L_latissimusDorsi2D', 7],
	['L_latissimusDorsi2E', 8],
	['L_latissimusDorsi2F', 9],
	['L_latissimusDorsi2G', 9],
	['L_latissimusDorsi2H', 7], 
	['L_teresMajor', 5], 
	['L_teresMinor2', 5], 
	# ['L_infraspinatusA', 5], No crossSections
	# ['L_infraspinatusB', 5], No crossSections
	# ['L_infraspinatusC', 5], No crossSections
	# ['L_coracobrachialis2', 5], No crossSections
	['L_brachialisA', 5], 
	['L_bicepsBrachiiShort', 7], 
	['L_bicepsBrachiiLong', 7], 
	['L_tricepsLateral', 5], 
	['L_tricepsLong', 5]
	]

longList = ['x45', 'x90', 'x135', 'x180', 'xn45']
twistList = ['w45', 'w90', 'wn45', 'wn90']


for musInfo in muscleList:
	deleteNefer(musInfo[0], musInfo[1])

for muscleData in muscleList:
	for cNum in range(1, muscleData[1] + 1):
		for longPt in longList:
			for twistPt in twistList:
				source = '%s_crossSection%s_x0_y0_%s_target' % (muscleData[0], cNum, twistPt)
				target = '%s_crossSection%s_%s_y0_%s_target' % (muscleData[0], cNum, longPt, twistPt)
				parentCtrl = '%s_control%s_%s_y0_%s_target' % (muscleData[0], cNum, longPt, twistPt)
				mc.delete(target)
				mc.duplicate(source, name=target)
				mc.parent(source, parentCtrl)



print '\r\rScript completed successfully\r\r'

