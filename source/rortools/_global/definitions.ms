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

global RoRWheel = attributes WheelsType
(
	parameters WheelParameters rollout:WheelRollout
	(
		radius           ui:UiRadius       type:#float   default:0.4
		rays             ui:UiRays         type:#integer default:12
		braked           ui:UiBraking      type:#integer default:1
		driven           ui:UiAcceleration type:#integer default:1
		mass             ui:UiMass         type:#float   default:200
		spring           ui:UiSpring       type:#float   default:400000
		damp             ui:UiDamping      type:#float   default:3000
		face_material    ui:UiRoRMaterial1 type:#string  default:"tracks/wheelfaceb"
		tread_material   ui:UiRoRMaterial2 type:#string  default:"tracks/wheelband2"
		
		on radius set val do
		(
			selection.render_thickness = val * 2
		)
		on rays set val do
		(
			selection.render_sides = val
		)
	)
	Rollout WheelRollout "RoR Data"
	(
		spinner      UiRadius       "Radius"       range:[0,100,0] scale: 0.01
		spinner      UiRays         "Rays"         range:[3,50,0]
		button       RigidityButton "Select rigidity node"
		dropdownlist UiBraking      "Braking"      items:#("Unbraked","Braked","Left steering","Right steering")
		dropdownlist UiAcceleration "Acceleration" items:#("Unaccelerated","Accelerated","Reverse driven")
		button       RefButton      "Select reference arm node"
		spinner      UiMass         "Mass"         range:[0,10000,0]
		spinner      UiSpring       "Spring"       range:[0,999999999999,0]
		spinner      UiDamping      "Damping"      range:[-999999999999,999999999999,0]
		edittext     UiRoRMaterial1 "Face material"  
		edittext     UiRoRMaterial2 "Band material"  
		on RigidityButton pressed do
		(
			try
			(
				Local RigidNode = (execute ("$rigidity_node_" + $.name))
				RigidNode.isHidden = false
				select RigidNode
			)
			Catch
			(
				messagebox "Rigidity node not found"
			)
		)
		on RefButton pressed do
		(
			try
			(
				Local RigidNode = (execute ("$ReferenceArmNode_" + $.name))
				RigidNode.isHidden = false
				select RigidNode
			)
			Catch
			(
				messagebox "Reference arm node not found"
			)
		)
	)
)