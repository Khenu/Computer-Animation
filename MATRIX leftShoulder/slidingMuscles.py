# slidingMuscles.py
# Created by Laushon Neferkara on 3/3/14.
# Copyright (c) 2013 Skin+Bones Modeling and Rigging Company. All rights reserved.

'''

'''


def setAffectSliding(mObj, state):

	if mObj.find('skel') == 0:
		mc.setAttr('%sShape.affectSliding' % mObj, state)
	else:
		mc.setAttr('cMuscleObject_%sShape1.affectSliding' % mObj, state)


# All of the connected muscle objects
musObjList = [
	'mus_skull_pBone', 
	'mus_jaw_pBone', 
	'bones_sternum_geo1', 
	'skel_L_thumbDistPhalanx_jnt', 
	'mus_L_thumbProxPhalanx_pBone', 
	'mus_L_thumbMetacarpal_pBone', 
	'skel_L_indexDistPhalanx_jnt', 
	'mus_L_indexMidPhalanx_pBone', 
	'mus_L_indexProxPhalanx_pBone', 
	'mus_L_indexMetacarpal_pBone', 
	'skel_L_middleDistPhalanx_jnt', 
	'mus_L_middleMidPhalanx_pBone', 
	'mus_L_middleProxPhalanx_pBone', 
	'mus_L_middleMetacarpal_pBone', 
	'skel_L_ringDistPhalanx_jnt', 
	'mus_L_ringMidPhalanx_pBone', 
	'mus_L_ringProxPhalanx_pBone', 
	'mus_L_ringMetacarpal_pBone', 
	'skel_L_littleDistPhalanx_jnt', 
	'mus_L_littleMidPhalanx_pBone', 
	'mus_L_littleProxPhalanx_pBone', 
	'mus_L_littleMetacarpal_pBone', 
	'mus_L_carpals_pBone', 
	'mus_L_radius_pBone', 
	'mus_L_ulna_pBone', 
	'mus_L_scapula_pBone', 
	'mus_L_clavicle_pBone', 
	'mus_L_rib6_pBone', 
	'mus_L_rib7_pBone', 
	'mus_L_rib8_pBone', 
	'mus_L_rib9_pBone', 
	'mus_L_rib10_pBone', 
	'mus_L_rib11_pBone', 
	'mus_L_rib12_pBone', 
	'mus_pelvis_pBone', 
	'cMuscleSurfaceMus_throat1', 
	'cMuscleSurfaceMus_L_platysmaA1',
	'cMuscleSurfaceMus_L_sternocleidomastoidA1', 
	'cMuscleSurfaceMus_L_sternocleidomastoidB1', 
	'cMuscleSurfaceMus_L_neck2A1', 
	'cMuscleSurfaceMus_L_trapezius5A1', 
	'cMuscleSurfaceMus_L_trapezius5B1', 
	'cMuscleSurfaceMus_L_trapezius3A1', 
	'cMuscleSurfaceMus_L_trapezius3C1', 
	'cMuscleSurfaceMus_L_trapezius5C1', 
	'cMuscleSurfaceMus_L_trapezius5D1', 
	'cMuscleSurfaceMus_L_trapezius2D1', 
	'cMuscleSurfaceMus_L_trapezius2E1', 
	'cMuscleSurfaceMus_L_trapezius2F1', 
	'cMuscleSurfaceMus_L_trapezius2G1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorA1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorB1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorC1', 
	'cMuscleSurfaceMus_L_deltoidLateralA1', 
	'cMuscleSurfaceMus_L_deltoidLateralB1', 
	'cMuscleSurfaceMus_L_deltoidLateralC1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorA1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorB1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorC1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorD1', 
	'cMuscleSurfaceMus_L_pectoralisA1', 
	'cMuscleSurfaceMus_L_pectoralisB1', 
	'cMuscleSurfaceMus_L_pectoralisC1', 
	'cMuscleSurfaceMus_L_pectoralisD1', 
	'cMuscleSurfaceMus_L_pectoralisE1', 
	'cMuscleSurfaceMus_L_pectoralisF1', 
	'cMuscleSurfaceMus_L_pectoralisG1', 
	'cMuscleSurfaceMus_L_pectoralisH1', 
	'cMuscleSurfaceMus_L_pectoralisJ1', 
	'cMuscleSurfaceMus_L_pectoralisK1', 
	'cMuscleSurfaceMus_L_pectoralisL1', 
	'cMuscleSurfaceMus_L_pectoralisM1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2A1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2B1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2C1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2D1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2E1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2F1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2G1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2H1', 
	'cMuscleSurfaceMus_L_teresMajor1', 
	'cMuscleSurfaceMus_L_teresMinor21', 
	'cMuscleSurfaceMus_L_infraspinatusA1', 
	'cMuscleSurfaceMus_L_infraspinatusB1', 
	'cMuscleSurfaceMus_L_infraspinatusC1', 
	'cMuscleSurfaceMus_L_trapeziusO1', 
	'cMuscleSurfaceMus_L_trapeziusP1', 
	'cMuscleSurfaceMus_L_trapeziusQ1', 
	'cMuscleSurfaceMus_L_trapeziusR1', 
	'cMuscleSurfaceMus_L_trapeziusS1', 
	'cMuscleSurfaceMus_L_bicepsBrachiiShort21', 
	'cMuscleSurfaceMus_L_bicepsBrachiiLong21', 
	'cMuscleSurfaceMus_L_brachialisA1', 
	'cMuscleSurfaceMus_L_tricepsBrachiiMedial21', 
	'cMuscleSurfaceMus_L_tricepsLateral1', 
	'cMuscleSurfaceMus_L_tricepsLong1', 
	'cMuscleSurfaceMus_L_coracobrachialisB1', 
	'cMuscleSurfaceMus_L_flexorGrp2A1', 
	'cMuscleSurfaceMus_L_flexorGrpB1', 
	'cMuscleSurfaceMus_L_extensorGrp2A1', 
	'cMuscleSurfaceMus_L_brachioradialis31', 
	'cMuscleSurfaceMus_L_brachioradialis3B1', 
	'cMuscleSurfaceMus_L_ECRL51', 
	'cMuscleSurfaceMus_L_ECRL5C1', 
	'cMuscleSurfaceMus_L_ECRB21', 
	'cMuscleSurfaceMus_L_anconeusA1', 
	'cMuscleSurfaceMus_L_erectorSpinae_E1', 
	'cMuscleSurfaceMus_L_erectorSpinae_F1', 
	'cMuscleSurfaceMus_erectorSpinae_G1', 
	'cMuscleSurfaceMus_L_extOblique2A1', 
	'cMuscleSurfaceMus_L_extOblique2B1', 
	'cMuscleSurfaceMus_L_extOblique2C1', 
	'cMuscleSurfaceMus_L_extOblique2D1', 
	'cMuscleSurfaceMus_L_extOblique2E1', 
	'cMuscleSurfaceMus_L_rectusAbdominis2A1', 
	'cMuscleSurfaceMus_L_rectusAbdominis2B1', 
	'cMuscleSurfaceMus_L_serratusAnteriorA1', 
	'cMuscleSurfaceMus_L_serratusAnteriorB1', 
	'cMuscleSurfaceMus_L_serratusAnteriorC1', 
	'cMuscleSurfaceMus_L_serratusAnteriorD1', 
	'cMuscleSurfaceMus_L_serratusAnteriorE1', 
	'cMuscleSurfaceMus_L_breastA1'
	]

# Turn off affectSliding for all the connected muscle objects
for mObj in musObjList:
	setAffectSliding(mObj, 0)

# Turn on affectSliding for muscle objects we want to affect sliding

# Muscle objects for sliding
slidingMusObjList = [
	# 'mus_skull_pBone', 
	# 'mus_jaw_pBone', 
	# 'bones_sternum_geo1', 
	# 'skel_L_thumbDistPhalanx_jnt', 
	# 'mus_L_thumbProxPhalanx_pBone', 
	# 'mus_L_thumbMetacarpal_pBone', 
	# 'skel_L_indexDistPhalanx_jnt', 
	# 'mus_L_indexMidPhalanx_pBone', 
	# 'mus_L_indexProxPhalanx_pBone', 
	# 'mus_L_indexMetacarpal_pBone', 
	# 'skel_L_middleDistPhalanx_jnt', 
	# 'mus_L_middleMidPhalanx_pBone', 
	# 'mus_L_middleProxPhalanx_pBone', 
	# 'mus_L_middleMetacarpal_pBone', 
	# 'skel_L_ringDistPhalanx_jnt', 
	# 'mus_L_ringMidPhalanx_pBone', 
	# 'mus_L_ringProxPhalanx_pBone', 
	# 'mus_L_ringMetacarpal_pBone', 
	# 'skel_L_littleDistPhalanx_jnt', 
	# 'mus_L_littleMidPhalanx_pBone', 
	# 'mus_L_littleProxPhalanx_pBone', 
	# 'mus_L_littleMetacarpal_pBone', 
	# 'mus_L_carpals_pBone', 
	# 'mus_L_radius_pBone', 
	# 'mus_L_ulna_pBone', 
	# 'mus_L_scapula_pBone', 
	# 'mus_L_clavicle_pBone', 
	# 'mus_L_rib6_pBone', 
	# 'mus_L_rib7_pBone', 
	# 'mus_L_rib8_pBone', 
	# 'mus_L_rib9_pBone', 
	# 'mus_L_rib10_pBone', 
	# 'mus_L_rib11_pBone', 
	# 'mus_L_rib12_pBone', 
	# 'mus_pelvis_pBone', 
	# 'cMuscleSurfaceMus_throat1', 
	# 'cMuscleSurfaceMus_L_platysmaA1',
	# 'cMuscleSurfaceMus_L_sternocleidomastoidA1', 
	# 'cMuscleSurfaceMus_L_sternocleidomastoidB1', 
	# 'cMuscleSurfaceMus_L_neck2A1', 
	# 'cMuscleSurfaceMus_L_trapezius5A1', 
	# 'cMuscleSurfaceMus_L_trapezius5B1', 
	# 'cMuscleSurfaceMus_L_trapezius3A1', 
	# 'cMuscleSurfaceMus_L_trapezius3C1', 
	# 'cMuscleSurfaceMus_L_trapezius5C1', 
	# 'cMuscleSurfaceMus_L_trapezius5D1', 
	# 'cMuscleSurfaceMus_L_trapezius2D1', 
	# 'cMuscleSurfaceMus_L_trapezius2E1', 
	# 'cMuscleSurfaceMus_L_trapezius2F1', 
	# 'cMuscleSurfaceMus_L_trapezius2G1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorA1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorB1', 
	'cMuscleSurfaceMus_L_deltoidAnteriorC1', 
	'cMuscleSurfaceMus_L_deltoidLateralA1', 
	'cMuscleSurfaceMus_L_deltoidLateralB1', 
	'cMuscleSurfaceMus_L_deltoidLateralC1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorA1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorB1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorC1', 
	'cMuscleSurfaceMus_L_deltoidPosteriorD1', 
	'cMuscleSurfaceMus_L_pectoralisA1', 
	'cMuscleSurfaceMus_L_pectoralisB1', 
	'cMuscleSurfaceMus_L_pectoralisC1', 
	'cMuscleSurfaceMus_L_pectoralisD1', 
	'cMuscleSurfaceMus_L_pectoralisE1', 
	'cMuscleSurfaceMus_L_pectoralisF1', 
	'cMuscleSurfaceMus_L_pectoralisG1', 
	'cMuscleSurfaceMus_L_pectoralisH1', 
	'cMuscleSurfaceMus_L_pectoralisJ1', 
	'cMuscleSurfaceMus_L_pectoralisK1', 
	'cMuscleSurfaceMus_L_pectoralisL1', 
	'cMuscleSurfaceMus_L_pectoralisM1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2A1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2B1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2C1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2D1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2E1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2F1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2G1', 
	'cMuscleSurfaceMus_L_latissimusDorsi2H1', 
	'cMuscleSurfaceMus_L_teresMajor1', 
	'cMuscleSurfaceMus_L_teresMinor21', 
	'cMuscleSurfaceMus_L_infraspinatusA1', 
	'cMuscleSurfaceMus_L_infraspinatusB1', 
	'cMuscleSurfaceMus_L_infraspinatusC1', 
	'cMuscleSurfaceMus_L_trapeziusO1', 
	'cMuscleSurfaceMus_L_trapeziusP1', 
	'cMuscleSurfaceMus_L_trapeziusQ1', 
	'cMuscleSurfaceMus_L_trapeziusR1', 
	'cMuscleSurfaceMus_L_trapeziusS1', 
	'cMuscleSurfaceMus_L_bicepsBrachiiShort21', 
	'cMuscleSurfaceMus_L_bicepsBrachiiLong21', 
	'cMuscleSurfaceMus_L_brachialisA1', 
	'cMuscleSurfaceMus_L_tricepsBrachiiMedial21', 
	'cMuscleSurfaceMus_L_tricepsLateral1', 
	'cMuscleSurfaceMus_L_tricepsLong1', 
	'cMuscleSurfaceMus_L_coracobrachialisB1', 
	# 'cMuscleSurfaceMus_L_flexorGrp2A1', 
	# 'cMuscleSurfaceMus_L_flexorGrpB1', 
	# 'cMuscleSurfaceMus_L_extensorGrp2A1', 
	# 'cMuscleSurfaceMus_L_brachioradialis31', 
	# 'cMuscleSurfaceMus_L_brachioradialis3B1', 
	# 'cMuscleSurfaceMus_L_ECRL51', 
	# 'cMuscleSurfaceMus_L_ECRL5C1', 
	# 'cMuscleSurfaceMus_L_ECRB21', 
	# 'cMuscleSurfaceMus_L_anconeusA1', 
	# 'cMuscleSurfaceMus_L_erectorSpinae_E1', 
	# 'cMuscleSurfaceMus_L_erectorSpinae_F1', 
	# 'cMuscleSurfaceMus_erectorSpinae_G1', 
	# 'cMuscleSurfaceMus_L_extOblique2A1', 
	# 'cMuscleSurfaceMus_L_extOblique2B1', 
	# 'cMuscleSurfaceMus_L_extOblique2C1', 
	# 'cMuscleSurfaceMus_L_extOblique2D1', 
	# 'cMuscleSurfaceMus_L_extOblique2E1', 
	# 'cMuscleSurfaceMus_L_rectusAbdominis2A1', 
	# 'cMuscleSurfaceMus_L_rectusAbdominis2B1', 
	'cMuscleSurfaceMus_L_serratusAnteriorA1', 
	'cMuscleSurfaceMus_L_serratusAnteriorB1', 
	# 'cMuscleSurfaceMus_L_serratusAnteriorC1', 
	# 'cMuscleSurfaceMus_L_serratusAnteriorD1', 
	# 'cMuscleSurfaceMus_L_serratusAnteriorE1', 
	'cMuscleSurfaceMus_L_breastA1'
	]

# Turn on affectSliding for muscle objects
for mObj in musObjList:
	setAffectSliding(mObj, 1)



