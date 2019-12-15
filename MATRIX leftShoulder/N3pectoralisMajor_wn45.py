muscleList = [
	# 'L_pectoralisMajor2A', 
	# 'L_pectoralisMajor2B', 
	# 'L_pectoralisMajor2C', 
	'L_pectoralisMajor2D', 
	'L_pectoralisMajor2E', 
	'L_pectoralisMajor2F', 
	'L_pectoralisMajor2G', 
	'L_pectoralisMajor2H', 
	'L_pectoralisMajor2I', 
	'L_pectoralisMajor2J', 
	'L_pectoralisMajor2K' 
]

numCtrls = 6

for musName in muscleList:
	for ctrlNum in range(numCtrls):
		for trans in ['translateX', 'translateY', 'translateZ']:
			transValue1 = mc.getAttr('%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), 
				'x90', 'y90', 'w0', trans))
			transValue2 = mc.getAttr('%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), 
				'x90', 'y90', 'wn90', trans))
			newTransValue = (transValue1 + transValue2)/2
			mc.setAttr('%s_control%s_%s_%s_%s_target.%s' % (musName, str(ctrlNum + 1), 
				'x90', 'y90', 'wn45', trans), newTransValue)

