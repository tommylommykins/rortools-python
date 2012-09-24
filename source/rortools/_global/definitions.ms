--Top level definitions for extra attributes that objects need for RoR data.
------------------------------------------------------------
Global RoRBeam = attributes BeamsType
(
	parameters BeamParameters rollout:beamRollout
	(
		spring         ui:UiSpring        type:#float   default: -1
		damp           ui:UiDamping       type:#float   default: -1
		deform         ui:UiDeformation   type:#float   default: -1
		break_force    ui:UiBreaking      type:#float   default: -1
		diameter       ui:UiDiameter      type:#float   default: -1
		ror_material   ui:UiRoR_Material  type:#string  default:"tracks/beam"
		deform_plastic ui:UiDeformPlastic type:#float   default: -1
		invisible      ui:UiInvisible     type:#boolean default:false
		rope           ui:UiRope          type:#boolean default:false
		support        ui:UiSupport       type:#boolean default:false
		support_len    ui:UiSupportLen    type:#float   default: 0
	)
	rollout BeamRollout "RoR data"
	(
		spinner  UiSpring        "Spring"              range:[-1,999999999999999,-1]
		spinner  UiDamping       "Damping"             range:[-1,999999999999999,-1]
		spinner  UiDeformation   "Deformation"         range:[-1,999999999999999,-1]
		spinner  UiBreaking      "Breaking"            range:[-1,999999999999999,-1]
		spinner  UiDiameter      "Diameter"            range:[-1,100,-1] scale:0.001
		edittext UiRoR_Material  "Material"
		spinner  UiDeformPlastic "Plastic deformation" range:[-1,999999999999999,-1]
		checkbox UiInvisible     "Invisibile"
		checkbox UiRope          "Rope"
		checkbox UiSupport   	 "Support"
		spinner  UiSupportLen    "Support Length"
	)
)

Global RoRGlobals = attributes RoRGlobalsType
(
	parameters RoRGlobalParameters rollout:RoRGlobalsRollout
	(
		global_data ui:ui_global_data type:#string default:""
	)
	rollout RoRGlobalsRollout "Global Data"
	(
		edittext ui_global_data "" height:300
	)
)

global RoRCinecam = attributes CinecamsType
(
	parameters CinecamParameters rollout:CinecamRollout
	(
		Spring  ui:UiSpring    type:#float   default:-1 --8000
		Damping ui:UiDamping   type:#float   default:-1 --800
	)
	Rollout CinecamRollout "RoR Data"
	(
		spinner UiSpring  "Spring"  range:[-1,999999999999,0]
		spinner UiDamping "Damping" range:[-999999999999,999999999999,0]
	)
)