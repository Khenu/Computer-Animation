# 
# 
# 
# 
class RemoveAttrs():
	
	def __init__(self, muscleName, numCtrls, mDriver):
		self.muscleName = muscleName
		self.numCtrls = numCtrls
		self.mDriver = mDriver
		self.attrList = ['JIGGLE', 'jiggle', 'jiggleX', 'jiggleY', 'jiggleZ', 'jiggleImpact', 'jiggleImpactStart', 'jiggleImpactStop', 'cycle', 'rest']
		self.remove()

	def remove(self):
		for dIndex in range(self.numCtrls): 
			for pointA in self.mDriver['axis1Points']:
				for pointB in self.mDriver['axis2Points']:
					for pointC in self.mDriver['axis3Points']:
						control = '%s_control%s_%s_%s_%s_target' % (self.muscleName, str(dIndex + 1), pointA, pointB, pointC)
						mc.setAttr('%s.JIGGLE' % control, lock=False)
						for attr in self.attrList:
							mc.deleteAttr('%s.%s' % (control, attr))			


def main():

	mDriver = {
		'driverName' : 'N3_muscleDriver1', 
		'axis1Points' : ('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		'axis2Points' : ('y0', 'y45', 'y90', 'y135', 'y170'), 
		'axis3Points' : ('w0', 'w45', 'w90', 'wn45', 'wn90')
		}

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
		['L_pectoralisM', 7], 
		['L_teresMajor', 5], 
		['L_teresMinor2', 5], 
		['L_infraspinatusA', 5], 
		['L_infraspinatusB', 5], 
		['L_infraspinatusC', 5], 
		['L_coracobrachialis', 4], 
		['L_latissimusDorsi2A', 6], 
		['L_latissimusDorsi2B', 6], 
		['L_latissimusDorsi2C', 7], 
		['L_latissimusDorsi2D', 7], 
		['L_latissimusDorsi2E', 8], 
		['L_latissimusDorsi2F', 9], 
		['L_latissimusDorsi2G', 9], 
		['L_latissimusDorsi2H', 7],  
		['L_brachialisA', 5],  
		['L_tricepsBrachiiMedial', 5],  
		['L_tricepsLateral', 5],  
		# ['L_tricepsLong', 5], 
		['L_bicepsBrachiiShort', 5], 
		['L_bicepsBrachiiLong2', 6], 
		['L_coracobrachialisB', 5], 
		['L_trapeziusO', 4], 
		['L_trapeziusP', 4], 
		['L_trapeziusQ', 4], 
		['L_trapeziusR', 4], 
		['L_trapeziusS', 4]
		]

	for muscle in muscleList:
		muscleName = muscle[0]
		numCtrls = muscle[1]
		Cleared = RemoveAttrs(muscleName, numCtrls, mDriver)


if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'





