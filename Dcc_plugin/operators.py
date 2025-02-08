import bpy
import requests

class SendTransformOperator(bpy.types.Operator):
    """Send Object Transform to Server"""
    bl_idname = "object.send_transform"
    bl_label = "Send Transform"

    def execute(self, context):
        obj = context.object
        if obj:
            endpoint = context.scene.dcc_selected_endpoint  # Get selected API endpoint
            url = f"http://127.0.0.1:5000/{endpoint}"

            data = {
                "name": obj.name,
                "position": [obj.location.x, obj.location.y, obj.location.z],
                "rotation": [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
                "scale": [obj.scale.x, obj.scale.y, obj.scale.z]
            }

            try:
                response = requests.post(url, json=data)
                self.report({'INFO'}, f"Server Response: {response.json()}")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to send data: {str(e)}")

        return {'FINISHED'}
