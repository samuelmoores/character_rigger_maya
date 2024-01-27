import maya.cmds as cmds


def match_transformations(source_node, target_node):
    # Get the transformation values from the source node
    translation = cmds.xform(source_node, query=True, translation=True, worldSpace=True)
    rotation = cmds.xform(source_node, query=True, rotation=True, worldSpace=True)
    scale = cmds.xform(source_node, query=True, scale=True, worldSpace=True)

    # Apply the transformation values to the target node
    cmds.xform(target_node, translation=translation, rotation=rotation, scale=scale, worldSpace=True)


def set_attribute(control):
    attributes = [".t", ".r", ".s", ".v"]
    axes = ["x", "y", "z"]

    i = 0
    for attribute in attributes:
        if i < 2:
            for axis in axes:
                cmds.setAttr(control + attribute + axis, lock=True, keyable=False, channelBox=False)
        else:
            cmds.setAttr(control + attribute, lock=True, keyable=False, channelBox=False)
        i += 1



# Add attribute
cmds.addAttr("pelvis_CTRL|spine01_CTRL", longName="lowerSpineFlex", attributeType='float', minValue=0, maxValue=1, defaultValue=0)

# Make the attribute keyable
cmds.setAttr("pelvis_CTRL|spine01_CTRL.lowerSpineFlex", keyable=True)

# Add attribute
cmds.addAttr("pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL", longName="upperSpineFlex", attributeType='float', minValue=0, maxValue=1, defaultValue=0)

# Make the attribute keyable
cmds.setAttr("pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL.upperSpineFlex", keyable=True)

# ------------------------------- neck flex ---------------------------------------

# Add attribute
cmds.addAttr("pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL|spine04_CTRL|neck01_CTRL", longName="neckFlex", attributeType='float', minValue=0, maxValue=1, defaultValue=0)

# Make the attribute keyable
cmds.setAttr("pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL|spine04_CTRL|neck01_CTRL.neckFlex", keyable=True)

# ------------------ create multiply divide node between spine01 and spine02 ------------------------------------

# Create a multiplyDivide node
multiply_divide_node = cmds.shadingNode('multiplyDivide', asUtility=True)

cmds.connectAttr('spine01_CTRL' + '.r', multiply_divide_node + '.input1', force=True)

# Connect lowerSpine_MD.outputX to spine02_JNT.rotateX
spine02_joint = 'spine02_CTRL'
cmds.connectAttr(multiply_divide_node + '.output', spine02_joint + '.r', force=True)


# Connect spine01_CTRL.lowerSpineFlex to multiplyDivide1.input2X
cmds.connectAttr('spine01_CTRL' + '.lowerSpineFlex', multiply_divide_node + '.input2X', force=True)
cmds.connectAttr('spine01_CTRL' + '.lowerSpineFlex', multiply_divide_node + '.input2Y', force=True)
cmds.connectAttr('spine01_CTRL' + '.lowerSpineFlex', multiply_divide_node + '.input2Z', force=True)


# ----------------------- spine03 and spine04 -----------------------------------------

multiply_divide_node = cmds.shadingNode('multiplyDivide', asUtility=True)

cmds.connectAttr('spine03_CTRL' + '.r', multiply_divide_node + '.input1', force=True)

# Connect lowerSpine_MD.outputX to spine02_JNT.rotateX
spine04_joint = 'spine04_CTRL'
cmds.connectAttr(multiply_divide_node + '.output', spine04_joint + '.r', force=True)


# Connect spine01_CTRL.lowerSpineFlex to multiplyDivide1.input2X
cmds.connectAttr('spine03_CTRL' + '.upperSpineFlex', multiply_divide_node + '.input2X', force=True)
cmds.connectAttr('spine03_CTRL' + '.upperSpineFlex', multiply_divide_node + '.input2Y', force=True)
cmds.connectAttr('spine03_CTRL' + '.upperSpineFlex', multiply_divide_node + '.input2Z', force=True)


# ----------------------- neck01 and neck02 ----------------------------------------------------------

multiply_divide_node = cmds.shadingNode('multiplyDivide', asUtility=True)

cmds.connectAttr('neck01_CTRL' + '.r', multiply_divide_node + '.input1', force=True)

# Connect lowerSpine_MD.outputX to neck02_JNT.rotateX
neck02_joint = 'neck02_CTRL'
cmds.connectAttr(multiply_divide_node + '.output', neck02_joint + '.r', force=True)

cmds.connectAttr('neck01_CTRL' + '.neckFlex', multiply_divide_node + '.input2X', force=True)
cmds.connectAttr('neck01_CTRL' + '.neckFlex', multiply_divide_node + '.input2Y', force=True)
cmds.connectAttr('neck01_CTRL' + '.neckFlex', multiply_divide_node + '.input2Z', force=True)


# ----------------------------- Foot Attributes -------------------------------------------

cmds.addAttr("leg_l_OFFSET|foot_l_CRV", longName="footControls", niceName="__________", attributeType="enum", enumName="Foot", keyable=True)

# Use addAttr command to add a float attribute
cmds.addAttr("foot_l_CRV", longName="bank", attributeType="float", keyable=True)
cmds.addAttr("foot_l_CRV" + "." + "bank", edit=True, minValue=-45.0)
cmds.addAttr("foot_l_CRV" + "." + "bank", edit=True, maxValue=45.0)

cmds.addAttr("foot_l_CRV", longName="ballRoll", attributeType="float", keyable=True)
cmds.addAttr("foot_l_CRV" + "." + "ballRoll", edit=True, maxValue=0.0)

cmds.addAttr("foot_l_CRV", longName="toeRoll", attributeType="float", keyable=True)
cmds.addAttr("foot_l_CRV" + "." + "toeRoll", edit=True, maxValue=0.0)

cmds.addAttr("foot_l_CRV", longName="toePivot", attributeType="float", keyable=True)

# ------ Right foot ---------------

cmds.addAttr("leg_r_OFFSET|foot_r_CRV", longName="footControls", niceName="__________", attributeType="enum", enumName="Foot", keyable=True)

# Use addAttr command to add a float attribute
cmds.addAttr("foot_r_CRV", longName="bank", attributeType="float", keyable=True)
cmds.addAttr("foot_r_CRV" + "." + "bank", edit=True, minValue=-45.0)
cmds.addAttr("foot_r_CRV" + "." + "bank", edit=True, maxValue=45.0)

cmds.addAttr("foot_r_CRV", longName="ballRoll", attributeType="float", keyable=True)
cmds.addAttr("foot_r_CRV" + "." + "ballRoll", edit=True, maxValue=0.0)

cmds.addAttr("foot_r_CRV", longName="toeRoll", attributeType="float", keyable=True)
cmds.addAttr("foot_r_CRV" + "." + "toeRoll", edit=True, maxValue=0.0)

cmds.addAttr("foot_r_CRV", longName="toePivot", attributeType="float", keyable=True)

# ------------------------------- Control foot attributes ----------------------------------------

cmds.connectAttr('foot_l_CRV.bank', "footOuter_l_REV" + '.rotateX', force=True)
cmds.connectAttr('foot_l_CRV.bank', "footInner_l_REV" + '.rotateX', force=True)

cmds.transformLimits("footOuter_l_REV", rx=(-45, 0), erx=(1, 1))
cmds.transformLimits("footInner_l_REV", rx=(0, 45), erx=(1, 1))

cmds.connectAttr('foot_l_CRV.ballRoll', "ball_l_REV" + '.rotateZ', force=True)
cmds.transformLimits("ball_l_REV", rz=(0, 0), erz=(0, 1))

cmds.connectAttr('foot_l_CRV.toeRoll', "toe_l_REV" + '.rotateZ', force=True)
cmds.transformLimits("toe_l_REV", rz=(0, 0), erz=(0, 1))

cmds.connectAttr('foot_l_CRV.toePivot', "toe_l_REV" + '.rotateX', force=True)

# ------------------ right -------------------------------

cmds.connectAttr('foot_r_CRV.bank', "footOuter_r_REV" + '.rotateX', force=True)
cmds.connectAttr('foot_r_CRV.bank', "footInner_r_REV" + '.rotateX', force=True)

cmds.transformLimits("footOuter_r_REV", rx=(0, 45), erx=(1, 1))
cmds.transformLimits("footInner_r_REV", rx=(-45, 0), erx=(1, 1))

cmds.connectAttr('foot_r_CRV.ballRoll', "ball_r_REV" + '.rotateZ', force=True)
cmds.transformLimits("ball_r_REV", rz=(0, 0), erz=(0, 1))

cmds.connectAttr('foot_r_CRV.toeRoll', "toe_r_REV" + '.rotateZ', force=True)
cmds.transformLimits("toe_r_REV", rz=(0, 0), erz=(0, 1))

cmds.connectAttr('foot_r_CRV.toePivot', "toe_r_REV" + '.rotateX', force=True)


# ----------------------------- Head and Neck ---------------------------------------------------------------

cmds.addAttr("head_CTRL", longName="worldOrient", attributeType="bool", keyable=True)

# --------------------------- Hands Finger Curl --------------------------------------

cmds.addAttr("hand_l_CTRL", longName="curl", attributeType="float", keyable=True)
cmds.addAttr("hand_r_CTRL", longName="curl", attributeType="float", keyable=True)

cmds.addAttr("hand_l_CTRL", longName="thumb", attributeType="float", keyable=True)
cmds.addAttr("hand_r_CTRL", longName="thumb", attributeType="float", keyable=True)

descendants = cmds.listRelatives("hand_l_CTRL", allDescendents=True, type='joint')

for descendant in descendants:
    cmds.connectAttr("hand_l_CTRL.curl", descendant + ".rotateX")

cmds.connectAttr("hand_l_CTRL.thumb", "|pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL|spine04_CTRL|clavicle_l_CTRL|upperarm_l_CTRL|lowerarm_l_CTRL|hand_l_CTRL|thumb_l_01_CTRL.rotateZ")

descendants = cmds.listRelatives("hand_r_CTRL", allDescendents=True, type='joint')

for descendant in descendants:
    cmds.connectAttr("hand_r_CTRL.curl", descendant + ".rotateX")

cmds.connectAttr("hand_r_CTRL.thumb", "|pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL|spine04_CTRL|clavicle_r_CTRL|upperarm_r_CTRL|lowerarm_r_CTRL|hand_r_CTRL|thumb_r_01_CTRL.rotateZ")


# ------------------------------ root and cog ----------------------------------------

cmds.parent("root_CRV", "root_CTRL")

joint_name = "root_CTRL"
curve_name = "root_CRV"

# Get all shape nodes of the curve
curve_shapes = cmds.listRelatives(curve_name, shapes=True) or []

# Parent each shape node to the joint
for shape_node in curve_shapes:
    cmds.parent(shape_node, joint_name, shape=True, add=True)

cmds.delete("root_CRV")

cmds.group(empty=True, name="cog_OFFSET")
cmds.parent("cog_OFFSET", "root_CTRL")
match_transformations("pelvis_CTRL", "head_OFFSET")
set_attribute("cog_OFFSET")
cmds.parent("cog_CRV", "cog_OFFSET")
match_transformations("cog_CRV", "cog_OFFSET")

attributes = [".s", ".v"]
axes = ["x", "y", "z"]

i = 0
for attribute in attributes:
    if i < 1:
        for axis in axes:
            cmds.setAttr("cog_CRV" + attribute + axis, lock=True, keyable=False, channelBox=False)
    else:
        cmds.setAttr("cog_CRV" + attribute, lock=True, keyable=False, channelBox=False)
    i += 1

cmds.parent("pelvis_CTRL", "cog_CRV")

cmds.setAttr("spine01_CTRL" + '.translateX', lock=False)
cmds.setAttr("spine01_CTRL" + '.translateY', lock=False)
cmds.setAttr("spine01_CTRL" + '.translateZ', lock=False)

cmds.parent("spine01_CTRL", "cog_CRV")

cmds.setAttr("spine01_CTRL" + '.translateX', lock=True)
cmds.setAttr("spine01_CTRL" + '.translateY', lock=True)
cmds.setAttr("spine01_CTRL" + '.translateZ', lock=True)


# ------------------------ Connect ctrls to bind skeleton ----------------------------------------------------

descendantsCTRL = cmds.listRelatives("cog_CRV", allDescendents=True, type="joint") or []

for ctrl in descendantsCTRL:
    if str(ctrl)[-8:] != "END_CTRL":
        cmds.parentConstraint(ctrl, str(ctrl).replace("CTRL", "BIND"), name=str(ctrl).replace("CTRL", "PC"))


cmds.parent("knee_l_CRV", "root_CTRL")
cmds.parent("knee_r_CRV", "root_CTRL")
cmds.parent("leg_l_OFFSET", "root_CTRL")
cmds.parent("leg_r_OFFSET", "root_CTRL")
