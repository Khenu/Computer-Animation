class Driver():
	"""docstring for Driver"""
	def __init__(self, name, data):
		self.name = name
		self.data = data


def main():

	muscleListB = [
	['L_deltoidAnterior', 5],
	['L_deltoidLateral', 7],
	['L_deltoidPosterior2A', 5], 
	['L_deltoidPosterior2B', 5], 
	['L_pectoralisMajorUpper', 5], 
	['L_pectoralisMajorMid', 5], 
	['L_pectoralisMajorLower', 5], 
	['L_pectoralisMajorLowerB', 5]] 


	n3driver = Driver(
		'N3_muscle_driver', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y45', 'y90', 'y135', 'y170'))
		)

	
	for muscle in muscleListB:

		for cIndex in range(muscle[1]):
		
			targetList = []
			driverList = []
			for longitude in n3driver.data[0]:
				for latitude in n3driver.data[1]:
					driverPt = '%s_%s' % (longitude, latitude)
					targetList.append('%s_crossSection%s_%s_w0_target' % (muscle[0], str(cIndex + 1), driverPt))
					driverList.append('%s_%s' % (longitude, latitude))

			crossSection = 'iControlMidMus_%s%s1_crossSectionREST' % (muscle[0], str(cIndex + 1))
			bshapeNode = '%s_blendShape' % crossSection
			mc.blendShape(targetList[0], crossSection, name = bshapeNode)
			# Add the remaining targets to the blend shape node
			for bIndex in range(1, len(targetList)):
				mc.blendShape(bshapeNode, edit=True, t=(crossSection, bIndex, targetList[bIndex], 1.0))

			for pIndex in range(len(targetList)):
				mc.connectAttr(
					'%s.%s' % (n3driver.name, driverList[pIndex]),
					'%s.%s' % (bshapeNode, targetList[pIndex])
					)

if __name__ == '__main__':
	main()


