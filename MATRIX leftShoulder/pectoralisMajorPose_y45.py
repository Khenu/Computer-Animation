
def averagePose(muscleList):
	axis1Point = 'x90'
	axis2Point = 'y90'
	axis3Point = 'w0'

	for musInfo in muscleList:
		musName = musInfo[0]
		numCtrls = musInfo[1]
		for ctrlNum in range(numCtrls):
			for trans in ['translateX', 'translateY', 'translateZ']:
				transValue1 = mc.getAttr('%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), 
					'x90', 'y90', 'wn90', trans))
				transValue2 = mc.getAttr('%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), 
					'x90', 'y90', 'wn90', trans))
				# mc.setAttr(
				# 	'%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), axis1Point, axis2Point, axis3Point, trans), 
				# 	(transValue1 * 0.5) + (transValue2 * 0.5)
				# 	)
				mc.setAttr(
					'%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), axis1Point, axis2Point, axis3Point, trans), 
					transValue1)


# muscleList1 = [
# 	('L_pectoralisMajor2A', 6), 
# 	('L_pectoralisMajor2B', 6), 
# 	('L_pectoralisMajor2C', 6), 
# 	('L_pectoralisMajor2D', 6), 
# 	('L_pectoralisMajor2E', 6), 
# 	('L_pectoralisMajor2F', 6), 
# 	('L_pectoralisMajor2G', 6), 
# 	('L_pectoralisMajor2H', 6), 
# 	('L_pectoralisMajor2I', 6), 
# 	('L_pectoralisMajor2J', 6), 
# 	('L_pectoralisMajor2K', 6)
# 	]

muscleList2 = [
	# ('L_deltoidAnteriorA', 5), 
	# ('L_deltoidAnteriorB', 5), 
	# ('L_deltoidAnteriorC', 5), 
	# ('L_deltoidLateralA', 5), 
	# ('L_deltoidLateralB', 5), 
	# ('L_deltoidLateralC', 5), 
	# ('L_deltoidPosteriorA', 5), 
	# ('L_deltoidPosteriorB', 5), 
	# ('L_deltoidPosteriorC', 5),
	# ('L_deltoidPosteriorD', 5)
	# ('L_brachialisA', 5), 
	('L_teresMajor', 5), 
	# ('L_teresMinor2', 5), 
	# ('L_infraspinatusA', 5), 
	# ('L_infraspinatusB', 5), 
	# ('L_infraspinatusC', 5)
	# ('L_coracobrachialis2', 5)

# 	('L_bicepsBrachiiA', 6), 
# 	('L_tricepsLateral', 5), 
# 	('L_tricepsLong', 5), 
# 	('L_coracobrachialis', 5)
	]

averagePose(muscleList2)


################################################################


musList = [
	# 'L_deltoidAnteriorA'
	# 'L_deltoidAnteriorB', 
	# 'L_deltoidAnteriorC'
	# 'L_deltoidLateralA', 
	# 'L_deltoidLateralB', 
	# 'L_deltoidLateralC', 
	# 'L_deltoidPosteriorA', 
	# 'L_deltoidPosteriorB', 
	# 'L_deltoidPosteriorC', 
	# 'L_deltoidPosteriorD'
	'L_pectoralisMajor2A', 
	'L_pectoralisMajor2B', 
	'L_pectoralisMajor2C', 
	'L_pectoralisMajor2D', 
	'L_pectoralisMajor2E', 
	'L_pectoralisMajor2F', 
	'L_pectoralisMajor2G', 
	'L_pectoralisMajor2H', 
	'L_pectoralisMajor2I', 
	'L_pectoralisMajor2J', 
	'L_pectoralisMajor2K'
	# 'L_brachialisA'
	# 'L_bicepsBrachiiA'
	# 'L_tricepsLateral', 
	# 'L_tricepsLong'
	]

numCtrls = 6

for musName in musList:
	for cNum in range(1, numCtrls + 1):
		crossSection = '%s_crossSection%s_x90_y170_wn45_target' % (musName, cNum)
		template = crossSection + '_template'
		mc.duplicate(crossSection, n=template)
		cross1 = '%s_crossSection%s_x90_y170_w0_target' % (musName, cNum)
		cross2 = '%s_crossSection%s_x90_y170_wn90_target' % (musName, cNum)
		mc.blendShape(cross1, cross2, template, w=[(0, 0.5), (1, 0.5)]) 
		# cross1 = '%s_crossSection%s_x0_y0_wn90_target' % (musName, cNum)
		# mc.blendShape(cross1, template, w=[(0, 1.0)]) 
		













