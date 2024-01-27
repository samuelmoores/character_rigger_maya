import maya.cmds as cmds
import maya.mel as mel


def set_attribute(control):
    attributes = [".t", ".s", ".v", ".radius"]
    axes = ["x", "y", "z"]

    i = 0
    for attribute in attributes:
        if i < 2:
            for axis in axes:
                cmds.setAttr(control + attribute + axis, lock=True, keyable=False, channelBox=False)
        else:
            cmds.setAttr(control + attribute, lock=True, keyable=False, channelBox=False)
        i += 1


def parent_shape(curve, joint):

    # Replace these with your actual joint and curve names
    joint_name = joint
    curve_name = curve

    # Get all shape nodes of the curve
    curve_shapes = cmds.listRelatives(curve_name, shapes=True) or []

    # Parent each shape node to the joint
    for shape_node in curve_shapes:
        cmds.parent(shape_node, joint_name, shape=True, add=True)


def freeze_transforms(joint):

    # Select the clavicle_l_CRV
    cmds.select(joint, replace=True)

    # Apply Make Identity transformation
    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=0, preserveNormals=True)


def match_transformations(source_node, target_node):
    # Get the transformation values from the source node
    translation = cmds.xform(source_node, query=True, translation=True, worldSpace=True)
    rotation = cmds.xform(source_node, query=True, rotation=True, worldSpace=True)
    scale = cmds.xform(source_node, query=True, scale=True, worldSpace=True)

    # Apply the transformation values to the target node
    cmds.xform(target_node, translation=translation, rotation=rotation, scale=scale, worldSpace=True)


def search_replace_names_in_hierarchy(root_node):
    # Get all descendants (child joints and beyond) of the specified parent joint
    descendants = cmds.listRelatives(root_node, allDescendents=True, type="joint", fullPath=True) or []

    for descendant in descendants:
        new_name = str(str(descendant).rsplit('|', 1)[-1]).replace("BIND", "CTRL")

        if new_name == "foot_l_END":
            new_name += "_CTRL"

        if new_name == "foot_r_END":
            new_name += "_CTRL"

        cmds.rename(descendant, new_name)

        if new_name[-3:] == "END" and new_name[0] != 'f':
            cmds.delete(descendant)


# -------------------------------- Variables -------------------------------------------------------
joints = ["clavicle", "upperarm", "lowerarm", "hand", "spine01", "spine03", "head", "neck01", "pelvis"]
side = ["_l", "_r"]
postfix = ["_CRV", "_CTRL"]
attributes = [".t", ".r", ".s", ".v"]
axes = ["x", "y", "z"]

cmds.mirrorJoint("clavicle_l_BIND", mirrorYZ=True,  searchReplace=("_l_", "_r_"), mirrorBehavior=True)

cmds.duplicate("pelvis_BIND")
cmds.rename("pelvis_BIND1", "pelvis_CTRL")

search_replace_names_in_hierarchy("pelvis_CTRL")

cmds.group(empty=True, name="head_OFFSET")
match_transformations("pelvis_CTRL|spine01_CTRL|spine02_CTRL|spine03_CTRL|spine04_CTRL|neck01_CTRL|neck02_CTRL|head_CTRL", "head_OFFSET")

cmds.parent("head_OFFSET", "neck02_CTRL")

cmds.parent("head_CTRL", "head_OFFSET")


# ----------------------- Parent Shape nodes for spine and arms ----------------------
i = 0
for joint in joints:
    if i < 4:
        for j in [0, 1]:
            cmds.parent(joint + side[j] + postfix[0], joint + side[j] + postfix[1])
            freeze_transforms(joint + side[j] + postfix[0])
            parent_shape(joint + side[j] + postfix[0], joint + side[j] + postfix[1])
            set_attribute(joint + side[j] + "_CTRL")
            cmds.delete(joint + side[j] + "_CRV")
    else:
        cmds.parent(joint + postfix[0], joint + postfix[1])
        freeze_transforms(joint + postfix[0])
        parent_shape(joint + postfix[0], joint + postfix[1])
        set_attribute(joint + "_CTRL")
        cmds.delete(joint + "_CRV")

    i += 1

cmds.select(clear=True)

cmds.joint(position=(0, 0, 0), radius=3.0, name="root_CTRL")

# Specify the target objects
target_objects = ["root_CTRL", "head_OFFSET"]

# Create an orient constraint with the specified arguments
orient_constraint = cmds.orientConstraint(*target_objects, mo=True, weight=1, name="head_OC")[0]

i = 0
for attribute in attributes:
    if i < 3:
        for axis in axes:
            cmds.setAttr("head_OFFSET" + attribute + axis, lock=True, keyable=False, channelBox=False)
    else:
        cmds.setAttr("head_OFFSET" + attribute, lock=True, keyable=False, channelBox=False)
    i += 1

# ------------------------ Reverse Foot --------------------------------------------
newNames = ["toe_l_REV", "ball_l_REV"]
oldNames = ["foot_l_REV|toe_l_CTRL|foot_l_END_CTRL", "foot_l_REV|toe_l_CTRL"]

cmds.select("foot_l_CTRL")
cmds.duplicate("foot_l_CTRL")
cmds.rename("foot_l_CTRL1", "foot_l_REV")

feet_joints = cmds.listRelatives("foot_l_REV", allDescendents=True, type="joint")

i = 0
for joint in feet_joints:
    cmds.rename(oldNames[i], newNames[i])
    i += 1

cmds.duplicate("ball_l_REV")
cmds.rename("ball_l_REV1", "footInner_l_REV")
cmds.rename("footInner_l_REV|toe_l_REV", "footOuter_l_REV")

cmds.parent("footInner_l_REV|footOuter_l_REV", world=True)
cmds.parent("footInner_l_REV", world=True)
cmds.parent("ball_l_REV|toe_l_REV", world=True)
cmds.parent("ball_l_REV", world=True)
cmds.parent("foot_l_REV", world=True)

cmds.parent("footInner_l_REV", "footOuter_l_REV")
cmds.parent("toe_l_REV", "footOuter_l_REV|footInner_l_REV")
cmds.parent("ball_l_REV", "footOuter_l_REV|footInner_l_REV|toe_l_REV")
cmds.parent("foot_l_REV", "footOuter_l_REV|footInner_l_REV|toe_l_REV|ball_l_REV")

cmds.mirrorJoint("footOuter_l_REV", mirrorYZ=True, searchReplace=("_l_", "_r_"), mirrorBehavior=True)


# ---------------------- Leg and Feet IK Handles ------------------------------------------

# Select leg_l_BIND and ankle_l_BIND
cmds.select("thigh_l_CTRL", r=True)
cmds.select("foot_l_CTRL", add=True)

# Create IK handle
cmds.ikHandle()

# Select leg_l_BIND and ankle_l_BIND
cmds.select("thigh_r_CTRL", r=True)
cmds.select("foot_r_CTRL", add=True)

# Create IK handle
cmds.ikHandle()

# Create IK handles for left foot
cmds.select("foot_l_CTRL", r=True)
cmds.select("toe_l_CTRL", add=True)
ik_handle1 = cmds.ikHandle(sol="ikSCsolver")[0]

cmds.select("toe_l_CTRL", r=True)
cmds.select("foot_l_END_CTRL", add=True)
ik_handle2 = cmds.ikHandle(sol="ikSCsolver")[0] 

# Create IK handle for right foot
cmds.select("foot_r_CTRL", r=True)
cmds.select("toe_r_CTRL", add=True)
ik_handle3 = cmds.ikHandle(sol="ikSCsolver")[0]

cmds.select("toe_r_CTRL", r=True)
cmds.select("foot_r_END_CTRL", add=True)
ik_handle4 = cmds.ikHandle(sol="ikSCsolver")[0]

cmds.rename("ikHandle1", "leg_l_IKH")
cmds.rename("ikHandle2", "leg_r_IKH")
cmds.rename("ikHandle3", "ball_l_IKH")
cmds.rename("ikHandle4", "toe_l_IKH")
cmds.rename("ikHandle5", "ball_r_IKH")
cmds.rename("ikHandle6", "toe_r_IKH")

# ------------------------ Knee Control --------------------------------------

# Create pole vector constraint
cmds.poleVectorConstraint("knee_l_CRV", "leg_l_IKH")
cmds.poleVectorConstraint("knee_r_CRV", "leg_r_IKH")

cmds.parent("leg_l_IKH", "foot_l_REV")
cmds.parent("ball_l_IKH", "ball_l_REV")
cmds.parent("toe_l_IKH", "toe_l_REV")

cmds.parent("leg_r_IKH", "foot_r_REV")
cmds.parent("ball_r_IKH", "ball_r_REV")
cmds.parent("toe_r_IKH", "toe_r_REV")

# -------------------------- Foot Offset and parent reverse foot to control -------------------------------
cmds.group(empty=True, name="leg_l_OFFSET")
cmds.group(empty=True, name="leg_r_OFFSET")

match_transformations("footOuter_l_REV|footInner_l_REV|toe_l_REV|ball_l_REV", "leg_l_OFFSET")
match_transformations("footOuter_r_REV|footInner_r_REV|toe_r_REV|ball_r_REV", "leg_r_OFFSET")



i = 0
for attribute in attributes:
    if i < 3:
        for axis in axes:
            cmds.setAttr("leg_l_OFFSET" + attribute + axis, lock=True, keyable=False, channelBox=False)
    else:
        cmds.setAttr("leg_l_OFFSET" + attribute, lock=True, keyable=False, channelBox=False)
    i += 1

i = 0
for attribute in attributes:
    if i < 3:
        for axis in axes:
            cmds.setAttr("leg_r_OFFSET" + attribute + axis, lock=True, keyable=False, channelBox=False)
    else:
        cmds.setAttr("leg_r_OFFSET" + attribute, lock=True, keyable=False, channelBox=False)
    i += 1

cmds.parent("foot_l_CRV", "leg_l_OFFSET")
freeze_transforms("foot_l_CRV")

cmds.parent("foot_r_CRV", "leg_r_OFFSET")
freeze_transforms("foot_r_CRV")

cmds.parent("footOuter_l_REV", "foot_l_CRV")
cmds.parent("footOuter_r_REV", "foot_r_CRV")

cmds.joint("footOuter_l_REV", edit=True, zeroScaleOrient=True, orientJoint='none')
cmds.joint("footOuter_r_REV", edit=True, zeroScaleOrient=True, orientJoint='none')

# Move the joint relative to its scale pivot and rotate pivot
cmds.move(-0.707778, -0.109562, -7.146428, "footOuter_l_REV" + ".scalePivot", "footOuter_l_REV" + ".rotatePivot", relative=True)
cmds.move(4.614037, 0.14974, -0.459267, "footOuter_l_REV" + ".scalePivot", "footOuter_l_REV" + ".rotatePivot", relative=True)

cmds.move(-4.837607, -0.156995, 0.481521, "footInner_l_REV" + ".scalePivot", "footInner_l_REV" + ".rotatePivot", relative=True)

# Replace "footOuter_r_REV" with the actual name of your joint
joint_name = "footOuter_r_REV"

# Move the joint relative to its scale pivot and rotate pivot
cmds.move(0.719009, -0.111301, -7.259823, joint_name + ".scalePivot", joint_name + ".rotatePivot", relative=True)
cmds.move(4.549912, -0.147659, 0.452884, joint_name + ".scalePivot", joint_name + ".rotatePivot", relative=True)

# Replace "footInner_r_REV" with the actual name of your joint
joint_name = "footInner_r_REV"

# Move the joint relative to its scale pivot and rotate pivot
cmds.move(-4.601903, 0.149346, -0.458059, joint_name + ".scalePivot", joint_name + ".rotatePivot", relative=True)

# ----------------------- Head Offset -------------------------------------





