import maya.cmds as cmds

def rename(oldNames, newNames):
    i = 0
    for joint in oldNames:
        cmds.select(joint)
        cmds.rename(joint, newNames[i])
        i += 1


def deleteChildren(joint):
    # Get the children of the parent joint
    children = cmds.listRelatives(joint, children=True, fullPath=True) or []

    # Delete each child joint
    for child in children:
        cmds.delete(child)


def parent(jointChild, jointParent):
    cmds.select(jointChild)
    cmds.select(jointParent, add=True)
    cmds.parent()

# ----------------------------------------- Variables ---------------------------------------------


jointsToDelete = ["RightUpLeg", "RightShoulder"]
jointsToUnparent = ["LeftUpLeg", "LeftShoulder"]
jointsToRenameSpine = ["Hips", "Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End"]
newNamesSpine = ["spine01_BIND", "spine02_BIND", "spine03_BIND", "spine04_BIND", "neck01_BIND", "head_BIND", "head_END"]
jointsToRenameArm = ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"]
newNamesArm = ["clavicle_l_BIND", "upperarm_l_BIND", "lowerarm_l_BIND", "hand_l_BIND"]

# clean up mixamo rig
for joint in jointsToDelete:
    cmds.select(joint)
    cmds.delete()

for joint in jointsToUnparent:
    cmds.select(joint)
    cmds.parent(w=True)

rename(jointsToRenameSpine, newNamesSpine)

# ------------------------------------------ Spine -------------------------------------------------

# orient spine
cmds.select("spine01_BIND")
cmds.joint("spine01_BIND", edit=True, oj="xzy", sao="xup", ch=True, zso=True)

# create neck02 joint
cmds.select("neck01_BIND")
cmds.duplicate("neck01_BIND", "-rr")
cmds.select("neck01_BIND1")
cmds.rename("neck01_BIND1", "neck02_BIND")
deleteChildren("neck02_BIND")

# parent neck02 between neck and head
parent("neck02_BIND", "neck01_BIND")
parent("head_BIND", "neck02_BIND")

# Select head_BIND joint
cmds.select('head_BIND', replace=True)


# pelvis
cmds.duplicate("spine01_BIND", "-rr")
cmds.rename("spine01_BIND1", "pelvis_BIND")
deleteChildren("pelvis_BIND")

# Select the joint
cmds.select("pelvis_BIND", replace=True)

# Move the selected object relative to its current position
cmds.move(-2.735468, 0, 0, relative=True, objectSpace=True, worldSpaceDistance=True)

# Set the jointOrientY attribute to 0
cmds.setAttr("{}.jointOrientY".format("pelvis_BIND"), 0)

cmds.parent("spine01_BIND", "pelvis_BIND")

# --------------------------------- ARM -------------------------------------------------------------
rename(jointsToRenameArm, newNamesArm)
cmds.select("LeftHandThumb1")
cmds.parent(w=True)
cmds.select("LeftHandIndex1")
cmds.parent(w=True)

# orient
cmds.joint("clavicle_l_BIND", edit=True, oj="xyz", sao="zup", ch=True, zso=True)

# Set the jointOrient
cmds.setAttr("{}.jointOrientX".format("hand_l_BIND"), 0)
cmds.setAttr("{}.jointOrientY".format("hand_l_BIND"), 0)
cmds.setAttr("{}.jointOrientZ".format("hand_l_BIND"), 0)

# -------------------------------------------- HAND ---------------------------------------------------
newNamesHand = ["thumb", "index", "middle", "ring", "pinky"]
cmds.duplicate("LeftHandIndex1", "-rr")
cmds.duplicate("LeftHandIndex1", "-rr")
cmds.duplicate("LeftHandIndex1", "-rr")

# loop through each finger chain and rename
# index for parent of finger chain
i = 0
# index for descendants
k = 0
while i < 8:

    if i == 0:
        joint = "LeftHandThumb1"
    else:
        joint = "LeftHandIndex" + str(i)

    # Get all descendants (child joints and beyond) of the specified parent joint
    descendants = cmds.listRelatives(joint, allDescendents=True, type="joint", fullPath=True) or []

    # Loop through each finger chain and rename each descendant with a new prefix
    j = len(descendants)+1
    for descendant in descendants:
        if j == len(descendants)+1:
            new_name = newNamesHand[k] + "_l_END"
        else:
            new_name = newNamesHand[k] + "_l_0" + str(j)
            new_name += "_BIND"

        cmds.rename(descendant, new_name)
        j -= 1

    # rename parent of each finger chain and parent
    cmds.rename(joint, newNamesHand[k] + "_l_01_BIND")
    parent(newNamesHand[k] + "_l_01_BIND", "hand_l_BIND")

    # check numbers assigned from duplicates
    if i == 1:
        i = 5
    else:
        i += 1

    k += 1

parent("clavicle_l_BIND", "spine04_BIND")

# -------------------------------------------- thigh ------------------------------------------------------
jointsToRenameLeg = ["LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", "LeftToe_End"]
newNamesLeg = ["thigh_l_BIND", "knee_l_BIND", "foot_l_BIND", "toe_l_BIND", "foot_l_END"]
rename(jointsToRenameLeg, newNamesLeg)

# orient thigh
cmds.joint("thigh_l_BIND", edit=True, oj="xzy", sao="xdown", ch=True, zso=True)
cmds.setAttr("{}.jointOrientX".format("thigh_l_BIND"), 90)
cmds.setAttr("{}.jointOrientX".format("knee_l_BIND"), 0)
cmds.setAttr("{}.jointOrientY".format("knee_l_BIND"), 0)
cmds.setAttr("{}.jointOrientX".format("foot_l_END"), 0)
cmds.setAttr("{}.jointOrientY".format("foot_l_END"), 0)
cmds.setAttr("{}.jointOrientZ".format("thigh_l_BIND"), -83.597)

# Mirror the joint across YZ plane
cmds.mirrorJoint("thigh_l_BIND", mirrorYZ=True, mirrorBehavior=True, searchReplace=("_l_", "_r_"))

cmds.parent("thigh_l_BIND", "pelvis_BIND")
cmds.parent("thigh_r_BIND", "pelvis_BIND")
