import bpy

class DCC_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "DCC Integration"
    bl_idname = "OBJECT_PT_dcc_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DCC Plugin"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj:
            layout.label(text=f"Selected Object: {obj.name}")
            layout.prop(obj, "location")
            layout.prop(obj, "rotation_euler")
            layout.prop(obj, "scale")
            
            # Dropdown for API selection
            layout.prop(context.scene, "dcc_selected_endpoint")

            # Submit Button
            layout.operator("object.send_transform", text="Submit Transform")
