# N3ArmCtrlDisplay.py
# Created by Laushon Neferkara on 12/2113.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

armCtrl = 'L_arm_ctrl'
longData = 'N3_humerus_long_data2'
latData = 'N3_humerus_lat_data2'
twistData = 'N3_humerus_twist_data2'


# Attribute lists
longList = [
	'xn45', 'x0', 'x45', 'x90', 'x135', 'x180']

latList = [
	'y0', 'y45', 'y90', 'y135', 'y170']

twistList = [
	'wn90', 'wn45', 'w0', 'w45', 'w90']


mc.select(armCtrl, replace=True)

longitudeLabel = 'Longitude'
mc.addAttr(longName=longitudeLabel, attributeType='enum', enumName='Group:---:*')
mc.setAttr('%s.%s' % (armCtrl, longitudeLabel), channelBox=True, keyable=False)
for newAttr in longList:
	mc.addAttr(longName=newAttr, attributeType='float')
	mc.setAttr('%s.%s' % (armCtrl, newAttr), channelBox=True, keyable=False)

latitudeLabel = 'Latitude'
mc.addAttr(longName=latitudeLabel, attributeType='enum', enumName='Group:---:*')
mc.setAttr('%s.%s' % (armCtrl, latitudeLabel), channelBox=True, keyable=False)
for newAttr in latList:
	mc.addAttr(longName=newAttr, attributeType='float')
	mc.setAttr('%s.%s' % (armCtrl, newAttr), channelBox=True, keyable=False)

twistLabel = 'Twist'
mc.addAttr(longName=twistLabel, attributeType='enum', enumName='Group:---:*')
mc.setAttr('%s.%s' % (armCtrl, twistLabel), channelBox=True, keyable=False)
for newAttr in twistList:
	mc.addAttr(longName=newAttr, attributeType='float')
	mc.setAttr('%s.%s' % (armCtrl, newAttr), channelBox=True, keyable=False)

for attr in longList:
	mc.connectAttr('%s.%s' % (longData, attr), '%s.%s' % (armCtrl, attr), lock=True)
for attr in latList:
	mc.connectAttr('%s.%s' % (latData, attr), '%s.%s' % (armCtrl, attr), lock=True)
for attr in twistList:
	mc.connectAttr('%s.%s' % (twistData, attr), '%s.%s' % (armCtrl, attr), lock=True)



print '\r\rScript completed Successfully\r\r'
