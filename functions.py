import bpy
from mathutils import *


def create_controller_armature():

    if 'Control_Bones' in bpy.data.collections:
        control_bones_col = bpy.data.collections['Control_Bones']

    else:
        control_bones_col = bpy.data.collections.new('Control_Bones')
        bpy.context.scene.collection.children.link(control_bones_col)



    current_active_object = bpy.context.view_layer.objects.active

    armature_name = "KEYER_CTRL_BONES"

    pivot_bone = bpy.data.armatures.new(armature_name)
    obj = bpy.data.objects.new(armature_name, pivot_bone)

    control_bones_col.objects.link(obj)

    arm_obj = bpy.data.objects[armature_name]
    bpy.context.view_layer.objects.active = arm_obj

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    edit_bones = arm_obj.data.edit_bones

    b = edit_bones.new('root_action_bone')
    b.head = (0.0, 0.0, 0.0)
    b.tail = (0.0, 0.0, 1.0)

    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    bpy.data.armatures['KEYER_CTRL_BONES'].bones['root_action_bone'].hide = True

    bpy.context.view_layer.objects.active = current_active_object


def create_controller(user_defined_name):

    cursor_location = bpy.context.scene.cursor.location

    current_cursor_x = cursor_location[0]
    current_cursor_y = cursor_location[1]
    current_cursor_z = cursor_location[2]

    bpy.context.scene.cursor.location = (0, 0, 0)

    current_active_object = bpy.context.view_layer.objects.active
    current_mode = bpy.context.object.mode

    current_bone_count = []

    bpy.context.view_layer.objects.active = bpy.data.objects['KEYER_CTRL_BONES']
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    for bone in bpy.context.view_layer.objects.active.data.edit_bones[:]:
        current_bone_count += [bone]

    bpy.context.scene.cursor.location = (len(current_bone_count), 0, 0)

    bone_name = user_defined_name + "_action_CTRL_bone"
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.armature.bone_primitive_add(name=bone_name)

    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    bpy.data.objects["KEYER_CTRL_BONES"].data.bones.active = bpy.data.objects["KEYER_CTRL_BONES"].pose.bones[bone_name].bone

    bpy.context.object.data.bones[bone_name].hide = True

    # set to previous state
    bpy.ops.object.mode_set(mode=current_mode, toggle=False)
    bpy.context.scene.cursor.location = (current_cursor_x, current_cursor_y, current_cursor_z)
    bpy.context.view_layer.objects.active = current_active_object


def add_custom_properties(user_defined_name, selected_armature):
    """Adds custom property to selected armature in and creates a slider in add-on UI"""

    current_active_object = bpy.context.view_layer.objects.active

    # add custom property to current armature
    bpy.context.view_layer.objects.active = bpy.data.objects[selected_armature]
    custom_property_definition(user_defined_name)

    bpy.context.view_layer.objects.active = current_active_object


def custom_property_definition(user_defined_name):

    user_custom_property = "action_driver_" + user_defined_name

    context = bpy.context
    obj = context.object

    rna_ui = obj.get('_RNA_UI')
    if rna_ui is None:
        obj['_RNA_UI'] = {}
        rna_ui = obj['_RNA_UI']

    obj[user_custom_property] = 0.0

    if bpy.context.scene.inverted_action:
        rna_ui[user_custom_property] = {"description": "Drives " + user_defined_name,
                                        "default": 0.0,
                                        "min": -1.0,
                                        "max": 1.0,
                                        "soft_min": -1.0,
                                        "soft_max": 1.0,
                                        }
    else:
        rna_ui[user_custom_property] = {"description": "Drives " + user_defined_name,
                                        "default": 0.0,
                                        "min": 0.0,
                                        "max": 1.0,
                                        "soft_min": 0.0,
                                        "soft_max": 1.0,
                                        }


def add_driver_to_bone(user_defined_name):

    user_custom_property = "action_driver_" + user_defined_name

    bone_name = user_defined_name + "_action_CTRL_bone"
    selected_armature = bpy.context.selected_objects[0].id_data.name

    if bpy.context.scene.inverted_action:
        # adds driver to Y axis
        driver = bpy.data.objects['KEYER_CTRL_BONES'].pose.bones[bone_name].driver_add("location", 0).driver

    else:
        # adds driver to Y axis
        driver = bpy.data.objects['KEYER_CTRL_BONES'].pose.bones[bone_name].driver_add("location", 1).driver
    driver.type = 'SCRIPTED'
    var = driver.variables.new()

    # set variable to type object
    var.targets[0].id_type = 'OBJECT'

    var.targets[0].id = bpy.data.objects[selected_armature]

    var.targets[0].data_path = '["{}"]'.format(user_custom_property)

    var.name = "Input"

    if not bpy.context.scene.inverted_action:
        driver.expression = "Input"
    else:
        driver.expression = "-Input"


def record_animation(selected_bones, selected_armature):

    location_origin = Vector((0.0, 0.0, 0.0))
    scale_origin = Vector((1.0, 1.0, 1.0))
    rotation_quaternion_origin = Quaternion((1.0, 0.0, 0.0, 0.0))
    rotation_euler_origin = Euler((0.0, 0.0, 0.0))

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.data.objects['KEYER_CTRL_BONES'].select_set(False)
    bpy.data.objects[selected_armature].select_set(True)

    bpy.context.active_bone.select = False
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    # remove existing animation data
    bpy.context.active_object.animation_data_clear()

    # create animation
    for bone in selected_bones:
        bone.bone.select = True

        bone.keyframe_insert(data_path='location', frame=(11))
        bone.keyframe_insert(data_path='scale', frame=(11))
        bone.keyframe_insert(data_path='rotation_euler', frame=(11))
        bone.keyframe_insert(data_path='rotation_quaternion', frame=(11))

        bone.location = location_origin
        bone.scale = scale_origin
        bone.rotation_quaternion = rotation_quaternion_origin
        bone.rotation_euler = rotation_euler_origin

        bone.keyframe_insert(data_path='location', frame=(1))
        bone.keyframe_insert(data_path='scale', frame=(1))
        bone.keyframe_insert(data_path='rotation_euler', frame=(1))
        bone.keyframe_insert(data_path='rotation_quaternion', frame=(1))

    for fcurves in bpy.context.object.animation_data.action.fcurves:
        fcurves.extrapolation = 'LINEAR'

        for kp in fcurves.keyframe_points:
            kp.handle_left_type = 'VECTOR'
            kp.handle_right_type = 'VECTOR'


def create_action(user_defined_name):

    if bpy.context.scene.inverted_action:
        bpy.context.object.animation_data.action.name = user_defined_name + "_inverted"
    else:
        bpy.context.object.animation_data.action.name = user_defined_name

    # animation data can be cleared
    bpy.context.active_object.animation_data_clear()


def add_action_constraints(user_defined_name, selected_bones):

    #armature_name = bpy.context.active_object.id_data.name

    bone_name = user_defined_name + "_action_CTRL_bone"
    inverted_bone_name = user_defined_name + "_inverted"

    for bone in selected_bones:

        bone.constraints.new(type="ACTION")

        if bpy.context.scene.inverted_action:
            bone.constraints["Action"].name = inverted_bone_name
            bone.constraints[inverted_bone_name].target_space = "LOCAL"
            bone.constraints[inverted_bone_name].target = bpy.data.objects['KEYER_CTRL_BONES']
            bone.constraints[inverted_bone_name].subtarget = bone_name
            bone.constraints[inverted_bone_name].transform_channel = 'LOCATION_X'
            bone.constraints[inverted_bone_name].action = bpy.data.actions[inverted_bone_name]

            bone.constraints[inverted_bone_name].frame_start = 0
            bone.constraints[inverted_bone_name].frame_end = 10

            bone.constraints[inverted_bone_name].min = 0
            bone.constraints[inverted_bone_name].max = 1

        else:
            bone.constraints["Action"].name = user_defined_name
            # set to local space
            bone.constraints[user_defined_name].target_space = "LOCAL"
            # set target to CTRL Armature
            bone.constraints[user_defined_name].target = bpy.data.objects['KEYER_CTRL_BONES']
            # set subtarget to newly created bone
            bone.constraints[user_defined_name].subtarget = bone_name

            # from target = Y Location
            bone.constraints[user_defined_name].transform_channel = 'LOCATION_Y'

            # set action
            bone.constraints[user_defined_name].action = bpy.data.actions[user_defined_name]
            # set action range
            bone.constraints[user_defined_name].frame_start = 1
            bone.constraints[user_defined_name].frame_end = 11
            # set target range
            bone.constraints[user_defined_name].min = 0
            bone.constraints[user_defined_name].max = 1


def show_message_box(message="", title="Message Box", icon='INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)