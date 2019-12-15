class Driver():
	"""docstring for Driver"""
	def __init__(self, name, data):
		self.name = name
		self.data = data


def main():

	muscleListA = [
		['L_deltoidAnterior', 5],
		['L_deltoidLateral', 7],
		['L_deltoidPosterior2A', 5], 
		['L_deltoidPosterior2B', 5], 
		['L_pectoralisMajorUpper', 5], 
		['L_pectoralisMajorMid', 5], 
		['L_pectoralisMajorLower', 5], 
		['L_pectoralisMajorLowerB', 5], 
		['L_teresMajor', 5], 
		['L_latissimusDorsiA', 6], 
		['L_latissimusDorsiB', 6], 
		['L_latissimusDorsiC', 7], 
		['L_latissimusDorsiD', 7], 
		['L_latissimusDorsiE', 8], 
		['L_latissimusDorsiF', 9], 
		['L_latissimusDorsiG', 7], 
		['L_latissimusDorsiH', 9]]

	n3driver = Driver(
		'N3_muscle_driver', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y45', 'y90', 'y135', 'y170'))
		)

	
	for muscle in muscleListA:

		musCtrls = []
		for cIndex in range(muscle[1]):
			musCtrls.append('iControlMidMus_%s%s1' % (muscle[0], str(cIndex + 1)))
		
			targetList = []
			driverList = []
			for longitude in n3driver.data[0]:
				for latitude in n3driver.data[1]:
					driverPt = '%s_%s' % (longitude, latitude)
					targetList.append('%s_control%s_%s_w0_target' % (muscle[0], str(cIndex + 1), driverPt))
					driverList.append('%s_%s' % (longitude, latitude))

			mc.pointConstraint(targetList, 'iControlMidMus_%s%s1' % (muscle[0], str(cIndex + 1)), weight=0.0)

			for pIndex in range(len(targetList)):
				mc.connectAttr(
					'%s.%s' % (n3driver.name, driverList[pIndex]),
					'iControlMidMus_%s%s1_pointConstraint1.%sW%s' % (muscle[0], str(cIndex + 1), targetList[pIndex], str(pIndex))
					)

if __name__ == '__main__':
	main()