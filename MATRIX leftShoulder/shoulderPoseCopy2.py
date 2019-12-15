################################



sourcePoseA = 'x90_y0_w0'
sourcePoseB = 'x90_y0_wn90'
destPose = 'x90_y0_wn45'
pctA = .50
pctB = .50

muscleList = [
	# ['L_deltoidAnteriorA', 5], 
	# ['L_deltoidAnteriorB', 5], 
	# ['L_deltoidAnteriorC', 5], 
	# ['L_deltoidLateralA', 5], 
	# ['L_deltoidLateralB', 5], 
	# ['L_deltoidLateralC', 5], 
	# ['L_deltoidPosteriorA', 5], 
	# ['L_deltoidPosteriorB', 5], 
	# ['L_deltoidPosteriorC', 5], 
	# ['L_deltoidPosteriorD', 5], 
	['L_pectoralisA', 6],
	['L_pectoralisB', 6],
	['L_pectoralisC', 6],
	['L_pectoralisD', 6],
	['L_pectoralisE', 6],
	['L_pectoralisF', 6],
	['L_pectoralisG', 6],
	['L_pectoralisH', 6],
	['L_pectoralisJ', 6],
	['L_pectoralisK', 7],
	['L_pectoralisL', 7],
	['L_pectoralisM', 7]
	# ['L_pectoralisMajor2K', 6], 
	# ['L_latissimusDorsi2A', 6],
	# ['L_latissimusDorsi2B', 6],
	# ['L_latissimusDorsi2C', 7],
	# ['L_latissimusDorsi2D', 7],
	# ['L_latissimusDorsi2E', 8],
	# ['L_latissimusDorsi2F', 9],
	# ['L_latissimusDorsi2G', 9],
	# ['L_latissimusDorsi2H', 7],
	# ['L_teresMajor', 5], 
	# ['L_teresMinor2', 5], 
	# ['L_infraspinatusA', 5], 
	# ['L_infraspinatusB', 5], 
	# ['L_infraspinatusC', 5], 
	# ['L_coracobrachialis2', 5], 
	# ['L_brachialisA', 5], 
	# ['L_bicepsBrachiiShort2', 6], 
	# ['L_bicepsBrachiiLong2', 6]
	# ['L_tricepsLateral', 5], 
	# ['L_tricepsLong', 5]
	]




for muscleData in muscleList: 
	for cNum in range(1, muscleData[1] + 1):
		sourceTargetA = '%s_control%s_%s_target' % (muscleData[0], cNum, sourcePoseA)
		sourceTargetB = '%s_control%s_%s_target' % (muscleData[0], cNum, sourcePoseB)
		destTarget = '%s_control%s_%s_target' % (muscleData[0], cNum, destPose)
		# 
		mc.setAttr('%s.translateX' % destTarget, pctA * mc.getAttr('%s.translateX' % sourceTargetA) + pctB * mc.getAttr('%s.translateX' % sourceTargetB))
		mc.setAttr('%s.translateY' % destTarget, pctA * mc.getAttr('%s.translateY' % sourceTargetA) + pctB * mc.getAttr('%s.translateY' % sourceTargetB))
		mc.setAttr('%s.translateZ' % destTarget, pctA * mc.getAttr('%s.translateZ' % sourceTargetA) + pctB * mc.getAttr('%s.translateZ' % sourceTargetB))

