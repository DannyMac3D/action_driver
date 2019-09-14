import bpy

from .functions import create_controller, \
    record_animation, \
    add_action_constraints, \
    create_action, \
    create_controller_armature, \
    show_message_box, \
    add_custom_properties, \
    add_driver_to_bone, \
    custom_property_definition


class ACTION_DRIVER_OT_MakeController(bpy.types.Operator):
    """Makes Bone Controller"""
    bl_label = "Make Bone Controller"
    bl_idname = "object.make_bone_controller"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):

        scn = context.scene

        # takes name from text input box
        user_defined_name = context.scene.action_namer
        selected_armature = bpy.context.selected_objects[0].id_data.name
        control_bone = user_defined_name + "_action_CTRL_bone"
        selected_bones = bpy.context.selected_pose_bones

        if user_defined_name == "":
            show_message_box("Name cannot be empty", "Error", 'ERROR')

        else:

            if bpy.data.objects.get("KEYER_CTRL_BONES") is None:
                create_controller_armature()

            if scn.inverted_action:
                # check name already exists - maybe convert to a drop-down box
                if control_bone in bpy.data.objects['KEYER_CTRL_BONES'].data.bones.keys():
                    record_animation(selected_bones, selected_armature)
                    create_action(user_defined_name)
                    add_action_constraints(user_defined_name, selected_bones)
                    custom_property_definition(user_defined_name)
                    add_driver_to_bone(user_defined_name)
                else:
                    show_message_box("Can't invert non-existent action", "Error", 'ERROR')

            else:

                if control_bone in bpy.data.armatures['KEYER_CTRL_BONES'].bones:
                    show_message_box("Name is already in use", "Error", 'ERROR')

                else:
                    if len(selected_bones) != 0:
                        record_animation(selected_bones, selected_armature)
                        create_controller(user_defined_name)
                        create_action(user_defined_name)
                        add_action_constraints(user_defined_name, selected_bones)
                        add_custom_properties(user_defined_name, selected_armature)
                        add_driver_to_bone(user_defined_name)

                        bpy.context.scene.action_namer = ""

                    else:
                        show_message_box("No bones are selected", "Error", 'ERROR')

        return {'FINISHED'}

