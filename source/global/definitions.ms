--Top level definitions for extra attributes that objects need for RoR data.
------------------------------------------------------------
Global RoRBeam = attributes BeamsType
(
	parameters BeamParameters rollout:beamRollout
	(
		spring       ui:UiSpring       type:#integer default: -1
		damping      ui:UiDamping      type:#integer default: -1
		deformation  ui:UiDeformation  type:#integer default: -1
		breaking     ui:UiBreaking     type:#integer default: -1
		diameter     ui:UiDiameter     type:#float   default: -1
		ror_material ui:UiRoR_Material type:#string  default:"tracks/beam"
		invisible    ui:UiInvisible    type:#boolean default:false
		rope         ui:UiRope         type:#boolean default:false
		support      ui:UiSupport      type:#boolean default:false
		support_len  ui:UiSupportLen   type:#float   default: 0
	)
	rollout BeamRollout "RoR data"
	(
		spinner  UiSpring       "Spring"      range:[-1,999999999999999,-1]
		spinner  UiDamping      "Damping"     range:[-1,999999999999999,-1]
		spinner  UiDeformation  "Deformation" range:[-1,999999999999999,-1]
		spinner  UiBreaking     "Breaking"    range:[-1,999999999999999,-1]
		spinner  UiDiameter     "Diameter"    range:[-1,100,-1] scale:0.001
		edittext UiRoR_Material "Material"
		checkbox UiInvisible    "Invisibile"
		checkbox UiRope         "Rope"
		checkbox UiSupport	"Support"
		spinner  UiSupportLen   "Support Length"
	)
)