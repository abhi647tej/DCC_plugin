bl_info = {
    "name": "DCC Integration Plugin",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "category": "Object",
    "description": "A Blender plugin to send object transforms to a Flask server",
}

import bpy
from .panel import DCC_PT_Panel
from .operators import SendTransformOperator

def register():
    bpy.types.Scene.dcc_selected_endpoint = bpy.props.EnumProperty(
        name="Server Endpoint",
        items=[
            ('transform', "Transform", "Send full transform"),
            ('translation', "Translation", "Send position only"),
            ('rotation', "Rotation", "Send rotation only"),
            ('scale', "Scale", "Send scale only")
        ]
    )
    bpy.utils.register_class(DCC_PT_Panel)
    bpy.utils.register_class(SendTransformOperator)

def unregister():
    bpy.utils.unregister_class(DCC_PT_Panel)
    bpy.utils.unregister_class(SendTransformOperator)
    del bpy.types.Scene.dcc_selected_endpoint

if __name__ == "__main__":
    register()
