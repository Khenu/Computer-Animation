# N3 upper arm muscle driver v2.py
# Created by Laushon Neferkara on 4/13/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.



# Import function module
import nm
	

def main():
	# Existing scene objects
	elbowFlexion = 'L_elbow_ctrl.rotateZ'			# 0 to 150
	forearmPronation = 'L_hand_ctrl.pronation'		# 0 to 140
	parentGroup = 'N3_L_SHOULDER'

	# New scene objects
	# Get flexData from N4 system? No. Make a new one to keep the systems seperate.	
	flexData = 'N3_upperArm_flex_data'
	proData = 'N3_upperArm_pronation_data'
	muscleDriver = 'N3_upperArm_driver'

	# Attribute lists
	flexList = [
		'a0', 'a45', 'a90', 'a135', 'a150']
	proList = [
		'b0', 'b140']

	# Pose values
	flexes = [
		0, 45, 90, 135, 150]

	pros = [
		0, 140]

	# Create data groups: flexData and proData
	nm.makeDataGrp(flexData, flexList, parentGroup)
	nm.makeDataGrp(proData, proList, parentGroup)

	# SDK's for longData, latData, twistData
	nm.makeSawtooth(flexData, elbowFlexion, flexList, flexes)		
	nm.makeSawtooth(proData, forearmPronation, proList, pros)		

	# Create multiply nodes to calculate driver values
	nm.makeDriver2(
		muscleDriver, 
		flexData, 
		proData, 
		flexList, 
		proList, 
		parentGroup)


if __name__ == '__main__':
	scriptName = 'N3 upper arm muscle driver.py'
	print '\r' + scriptName + ' running'
	main()
	print '\r\r' + scriptName + ' completed Successfully\r\r'

