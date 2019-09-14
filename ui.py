import bpy

class ACTION_DRIVER_PT_ui(bpy.types.Panel):
    '''Draws UI Panel'''
    bl_label = "Action Driver"
    bl_idname = "UI_PT_TEST"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Action Driver"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scn = context.scene

        col = self.layout.column(align=True)
        col.prop(context.scene, "action_namer")

        row = layout.row()
        row.operator("object.make_bone_controller", text="Make Slider")

        row = layout.row()
        row.prop(scn, "inverted_action")


class ACTION_DRIVER_PT_sliders_ui(bpy.types.Panel):
    '''Draws UI Panel'''
    bl_label = "Actions"
    bl_idname = "UI_PT_TEST_TWO"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Action Driver"

    # @classmethod
    # def poll(cls, context):
    #
    #     obj = bpy.context.object
    #     action_driver_props = []
    #     for prop in obj.keys():
    #         if prop.startswith('action_driver_'):
    #          action_driver_props += [prop]
    #     armature_has_keys = len(action_driver_props) > 0
    #     return armature_has_keys

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.object

        for obj in bpy.context.scene.objects:
            # draws sliders for custom properties.
            for prop in obj.keys():
                if not prop.startswith('_'):
                    if prop.startswith('action_driver_'):
                        row = layout.row()
                        row.prop(obj, '["{}"]'.format(prop), slider=True, text=prop[14:])



