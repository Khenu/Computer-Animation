# neferMuscleConnections.py
# Created by Laushon Neferkara on 2/25/14.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''
1. Delete existing muscle control and muscle cross section connections.
2. Replace poses.
3. Reestablish connections.


'''
class Driver():
	"""docstring for Driver"""
	def __init__(self, name, data):
		self.name = name
		self.data = data


def main():

	muscleListA = [
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
		]

	n3driver = Driver(
		'N3_muscleDriver1', 
		(('x0', 'x45', 'x90', 'x135', 'x180', 'xn45'), 
		('y0', 'y45', 'y90', 'y135', 'y170'), 
		('w0', 'w45', 'w90', 'wn45', 'wn90'))
		)

	
	for muscle in muscleListA:

		musCtrls = []
		for cIndex in range(muscle[1]):
			musCtrls.append('iControlMidMus_%s%s1' % (muscle[0], str(cIndex + 1)))
		
			# Muscle Controls
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

			# Muscle Cross Sections
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