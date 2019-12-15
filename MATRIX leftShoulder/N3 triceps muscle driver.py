# N3 triceps muscle driver.py
# Created by Laushon Neferkara on 5/1/13.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.



# Import function module
import nm
	

def main():
	# Existing scene objects
	elbowFlexion = 'L_elbow_ctrl.rotateZ'			# 0 to 150
	parentGroup = 'N3_L_SHOULDER'

	# New scene objects
	# Get flexData from N4 system? No. Make a new one to keep the systems seperate.	
	# flexData = 'N3_triceps_data'
	muscleDriver = 'N3_triceps_driver'

	# Attribute lists
	flexList = [
		'a0', 'a45', 'a90', 'a135', 'a150']

	# Pose values
	flexes = [
		0, 45, 90, 135, 150]

	# Create data groups: flexData and proData
	nm.makeDataGrp(muscleDriver, flexList, parentGroup)

	# SDK's for longData, latData, twistData
	nm.makeSawtooth(muscleDriver, elbowFlexion, flexList, flexes)		


if __name__ == '__main__':
	main()


print '\r\rCompleted successfully\r\r'

