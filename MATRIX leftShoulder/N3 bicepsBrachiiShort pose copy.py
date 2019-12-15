'''Copy'''

def copyPoses(poseList, longitudes):
	for sourcePose in poseList:
		for longitude in longitudes:
			target = sourcePose.replace('x0', longitude)
			mc.setAttr(
				'%s.translateX' % target,
				mc.getAttr('%s.translateX' % sourcePose)
				)
			mc.setAttr(
				'%s.translateY' % target,
				mc.getAttr('%s.translateY' % sourcePose)
				)
			mc.setAttr(
				'%s.translateZ' % target,
				mc.getAttr('%s.translateZ' % sourcePose)
				)


def main():
	sourcePoses1 = (
		'L_bicepsBrachiiShort_control1_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control2_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control3_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control4_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control5_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control6_x0_y0_w90_target', 
		'L_bicepsBrachiiShort_control7_x0_y0_w90_target'
		)

	sourcePoses2 = (
		'L_bicepsBrachiiShort_control1_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control2_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control3_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control4_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control5_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control6_x0_y0_wn90_target', 
		'L_bicepsBrachiiShort_control7_x0_y0_wn90_target'
		)

	longitudes = ('x45', 'x90', 'x135', 'x180', 'xn45')

	copyPoses(sourcePoses1, longitudes)
	copyPoses(sourcePoses2, longitudes)


if __name__ == '__main__':
	main()

