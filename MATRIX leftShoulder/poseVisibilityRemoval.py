# poseVisibilityRemoval.py
# Created by Laushon Neferkara on 11/27/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.


def connectVis(poseList, muscleDataList):
	for muscleData in muscleDataList:
		for pose in poseList:
			for ctrlNum in range(2, muscleData[1] + 1):
				mc.disconnectAttr(
					'%s_control1_%s_pose_grp.visibility' % (muscleData[0], pose), 
					'%s_control%s_%s_pose_grp.visibility' % (muscleData[0], str(ctrlNum), pose)
					)

def main():
	
	poseList = [
		# x0 group
		'x0_y0_w0', 
		'x0_y0_w45', 
		'x0_y0_w90', 
		'x0_y0_wn45', 
		'x0_y0_wn90', 
		
		'x0_y45_w0', 
		'x0_y45_w45', 
		'x0_y45_w90', 
		'x0_y45_wn45', 
		# 'x0_y45_wn90',	out of range

		'x0_y90_w0', 
		'x0_y90_w45', 
		'x0_y90_w90', 
		# 'x0_y90_wn45',	out of range
		# 'x0_y90_wn90',	out of range

		'x0_y135_w0', 
		'x0_y135_w45', 
		'x0_y135_w90', 
		# 'x0_y135_wn45',	out of range
		# 'x0_y135_wn90',	out of range

		'x0_y170_w0', 
		'x0_y170_w45', 
		'x0_y170_w90', 
		# 'x0_y170_wn45',	out of range
		# 'x0_y170_wn90',	out of range

		# x45 group
		'x45_y0_w0', 
		'x45_y0_w45', 
		'x45_y0_w90', 
		'x45_y0_wn45', 
		'x45_y0_wn90', 
		
		'x45_y45_w0', 
		'x45_y45_w45', 
		# 'x45_y45_w90', 	out of range?
		'x45_y45_wn45', 
		# 'x45_y45_wn90',	out of range?

		'x45_y90_w0', 
		'x45_y90_w45', 
		# 'x45_y90_w90', 	out of range
		'x45_y90_wn45',	
		# 'x45_y90_wn90',	out of range

		'x45_y135_w0', 
		'x45_y135_w45', 
		# 'x45_y135_w90', 	out of range
		'x45_y135_wn45',	
		# 'x45_y135_wn90',	out of range

		'x45_y170_w0', 
		'x45_y170_w45', 
		# 'x45_y170_w90', 	out of range
		'x45_y170_wn45',
		# 'x45_y170_wn90',	out of range

		# x90 group
		'x90_y0_w0', 
		'x90_y0_w45', 
		'x90_y0_w90', 
		'x90_y0_wn45', 
		'x90_y0_wn90', 
		
		'x90_y45_w0', 
		'x90_y45_w45', 
		# 'x90_y45_w90', 	out of range
		'x90_y45_wn45', 
		'x90_y45_wn90',	

		'x90_y90_w0', 	
		# 'x90_y90_w45', 	out of range
		# 'x90_y90_w90', 	out of range
		'x90_y90_wn45',	
		'x90_y90_wn90',	

		'x90_y135_w0', 	
		# 'x90_y135_w45', 	out of range
		# 'x90_y135_w90', 	out of range
		'x90_y135_wn45',	
		'x90_y135_wn90',	

		'x90_y170_w0', 	
		# 'x90_y170_w45', 	out of range
		# 'x90_y170_w90', 	out of range
		'x90_y170_wn45', 
		'x90_y170_wn90', 

		# x135 group
		'x135_y0_w0', 
		'x135_y0_w45', 
		'x135_y0_w90', 
		'x135_y0_wn45', 
		'x135_y0_wn90', 
		
		'x135_y45_w0', 
		'x135_y45_w45', 
		'x135_y45_w90', 
		'x135_y45_wn45', 
		'x135_y45_wn90', 

		'x135_y90_w0', 
		'x135_y90_w45', 
		'x135_y90_w90', 
		# 'x135_y90_wn45',	out of range
		# 'x135_y90_wn90',	out of range

		# 'x135_y135_w0', 	out of range
		# 'x135_y135_w45', 	out of range
		# 'x135_y135_w90', 	out of range
		# 'x135_y135_wn45',	out of range
		# 'x135_y135_wn90',	out of range

		# 'x135_y170_w0', 	out of range
		# 'x135_y170_w45', 	out of range
		# 'x135_y170_w90', 	out of range
		# 'x135_y170_wn45',	out of range
		# 'x135_y170_wn90',	out of range

		# x180 group
		'x180_y0_w0', 
		'x180_y0_w45', 
		'x180_y0_w90', 
		'x180_y0_wn45', 
		'x180_y0_wn90', 
		
		'x180_y45_w0', 
		'x180_y45_w45', 
		'x180_y45_w90', 
		'x180_y45_wn45', 
		# 'x180_y45_wn90',	out of range ???

		# 'x180_y90_w0', 	out of range
		# 'x180_y90_w45', 	out of range
		# 'x180_y90_w90', 	out of range
		# 'x180_y90_wn45',	out of range
		# 'x180_y90_wn90',	out of range

		# 'x180_y135_w0', 	out of range
		# 'x180_y135_w45', 	out of range
		# 'x180_y135_w90', 	out of range
		# 'x180_y135_wn45',	out of range
		# 'x180_y135_wn90',	out of range

		# 'x180_y170_w0', 	out of range
		# 'x180_y170_w45', 	out of range
		# 'x180_y170_w90', 	out of range
		# 'x180_y170_wn45',	out of range
		# 'x180_y170_wn90',	out of range

		# xn45 group
		'xn45_y0_w0', 
		'xn45_y0_w45', 
		'xn45_y0_w90', 
		'xn45_y0_wn45', 
		# 'xn45_y0_wn90', 	out of range
		
		'xn45_y45_w0', 
		'xn45_y45_w45', 
		'xn45_y45_w90', 
		'xn45_y45_wn45', 
		# 'xn45_y45_wn90',	out of range

		'xn45_y90_w0', 
		'xn45_y90_w45', 
		'xn45_y90_w90', 
		# 'xn45_y90_wn45',	out of range
		# 'xn45_y90_wn90',	out of range

		'xn45_y135_w0', 
		'xn45_y135_w45', 
		'xn45_y135_w90', 
		# 'xn45_y135_wn45',	out of range
		# 'xn45_y135_wn90',	out of range

		'xn45_y170_w0', 
		'xn45_y170_w45', 
		'xn45_y170_w90', 
		# 'xn45_y170_wn45',	out of range
		# 'xn45_y170_wn90',	out of range

		]
	
	muscleDataList = [
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
		['L_teresMajor', 5], 
		['L_teresMinor2', 5], 
		['L_infraspinatusA', 5], 
		['L_infraspinatusB', 5], 
		['L_infraspinatusC', 5], 
		['L_coracobrachialis2', 5], 
		['L_latissimusDorsi2A', 6], 
		['L_latissimusDorsi2B', 6], 
		['L_latissimusDorsi2C', 7], 
		['L_latissimusDorsi2D', 7], 
		['L_latissimusDorsi2E', 8], 
		['L_latissimusDorsi2F', 9], 
		['L_latissimusDorsi2G', 9], 
		['L_latissimusDorsi2H', 7],  
		['L_brachialisA', 5],  
		['L_bicepsBrachiiA', 6],  
		['L_tricepsLateral', 5],  
		['L_tricepsLong', 5]
		]


	connectVis(poseList, muscleDataList)

if __name__ == '__main__':
	main()

print '\r\rScript completed successfully\r\r'








