# shoulderFreezeMuscle.py

# Edit pose variable

# Exists in scene
frozenCtrlTemp = 'frozen__ctrl'
frozenLayer = 'frozen_muscles_layer'

# Pose that is being frozen
pose = 'x90_y0_w0'


muscleList = [
	'L_deltoidAnteriorA', 
	'L_deltoidAnteriorB', 
	'L_deltoidAnteriorC', 
	'L_deltoidLateralA', 
	'L_deltoidLateralB', 
	'L_deltoidLateralC', 
	'L_deltoidPosteriorA', 
	'L_deltoidPosteriorB', 
	'L_deltoidPosteriorC', 
	'L_deltoidPosteriorD', 
	'L_pectoralisA', 
	'L_pectoralisB', 
	'L_pectoralisC', 
	'L_pectoralisD', 
	'L_pectoralisE', 
	'L_pectoralisF', 
	'L_pectoralisG', 
	'L_pectoralisH', 
	'L_pectoralisJ', 
	'L_pectoralisK', 
	'L_pectoralisL', 
	'L_pectoralisM', 
	'L_latissimusDorsi2A', 
	'L_latissimusDorsi2B', 
	'L_latissimusDorsi2C', 
	'L_latissimusDorsi2D', 
	'L_latissimusDorsi2E', 
	'L_latissimusDorsi2F', 
	'L_latissimusDorsi2G', 
	'L_latissimusDorsi2H', 
	'L_teresMajor', 
	'L_teresMinor', 
	'L_infraspinatusA', 
	'L_infraspinatusB', 
	'L_infraspinatusC', 
	'L_coracobrachialis', 
	'L_bicepsBrachiiShort',
	'L_bicepsBrachiiLong',
	'L_brachialisA', 
	'L_tricepsBrachiiMedial', 
	'L_tricepsLateral', 
	'L_tricepsLong', 
	'L_breastA'
	]


frozenCtrl = frozenCtrlTemp.replace('__', '_%s_' % pose)

mc.duplicate(frozenCtrlTemp, n=frozenCtrl)
mc.setAttr('%s.visibility' % frozenCtrl, 1)

for muscle in muscleList:
	musNode = 'cMuscleSurfaceMus_%s1' % muscle
	frozenName = 'frozen_%s_%s' % (pose, muscle)

	mc.duplicate(musNode, renameChildren=True, name=frozenName)
	children = mc.listRelatives(frozenName, type='cMuscleObject', path=True)
	# listRelatives returns a list
	if children:
		mc.delete(children)
	children = mc.listRelatives(frozenName, type='nurbsSurface', path=True)
	# listRelatives returns a list
	if children:
		mc.rename(children, '%sShape' % frozenName)
	for attr in ['translateX', 'translateY', 'translateZ']:
		mc.setAttr('%s.%s' % (frozenName, attr), lock=False, channelBox=True)
	mc.setAttr('%s.inheritsTransform' % frozenName, 1)
	mc.setAttr('%s.visibility' % frozenName, 1)
	mc.setAttr('%sShape.overrideEnabled' % frozenName, 0)
	mc.parent(frozenName, frozenCtrl)
	mc.editDisplayLayerMembers(frozenLayer, frozenName, noRecurse=True)
	# sets -e -forceElement N7b_lambert_modelingSG3;
	mc.hyperShade(frozenName, assign='lambert_modeling')


# mc.parent(frozenGrp, frozenCtrl)
mc.select(frozenCtrl, r=True)



