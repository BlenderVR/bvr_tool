import bpy
from bpy.types import Operator

class BlenderVRLoadConfigurationFile(Operator):
    """"""
    bl_label = "Load Configuration File"
    bl_idname = 'bvr.loadconfigfile'
    bl_options = {'REGISTER', 'UNDO'}

    arg = bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        option = self.arg

        # cleanup before we start
        # bpy.ops.object.select_all(action='DESELECT')

        if option == 'new':
            return {'FINISHED'}

        if option == 'load':

            # get file path
            scene = context.scene
            blendervr = scene.blendervr
            filepath = bpy.path.abspath(blendervr.config_file_path)
            # file_path = bpy.path.ensure_ext(filepath, ".x3d")

            # get console
            # bpy.ops.screen.new()
            # bpy.ops.screen.area_dupli()
            # bpy.ops.screen.userpref_show()
            print('configuration file: ' + filepath)


        return {'FINISHED'}

class BlenderVRLoadBlenderScene(Operator):
    """"""
    bl_label = "Load Configuration File"
    bl_idname = 'bvr.loadblenderscene'
    bl_options = {'REGISTER', 'UNDO'}

    arg = bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        loadType = self.arg

        # cleanup before we start
        bpy.ops.object.select_all(action='DESELECT')

        if loadType == 'new':
            return {'FINISHED'}

        if loadType == 'load':
            return {'FINISHED'}

class BlenderVRLauncher(bpy.types.Operator):
    """"""
    bl_label = "BlenderVR Launcher"
    bl_idname = 'bvr.launcher'
    bl_options = {'REGISTER', 'UNDO'}

    arg = bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        # arg = self.arg.split('.')
        arg = self.arg

        # get file path
        scene = context.scene
        blendervr = scene.blendervr

        if arg == 'start':
            # tryout, start blenderplayer
            # bpy.ops.wm.blenderplayer_start()

            import subprocess
            args = ['python3', '/Users/AstrApple/WorkSpace/Blender_Workspace/addons/blendervr/source/blenderVR', 'controller']
            blendervr.proc = subprocess.Popen(args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
            print('opened',blendervr.proc)

            # outs, errs = blendervr.proc.communicate(timeout=15)
            outs, errs = blendervr.proc.communicate()
            print('first words: \n', outs,errs)

            return {'FINISHED'}

        elif arg == 'stop':
            blendervr.proc.kill()
            outs, errs = blendervr.proc.communicate()
            print('subprocess killed, last words:')
            print(outs,errs)

            return {'FINISHED'}
        elif arg == 'debug.window':
            print('open debug window')
            area = bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            context.area.type = 'CONSOLE'
            # bpy.ops.screen.new('INVOKE_DEFAULT')


            return {'FINISHED'}

        else:
            self.report({'ERROR'}, 'arg (in launcher) not defined yet')
            return {'CANCELLED'}


# ############################################################
# Un/Registration
# ############################################################

classes = (
    BlenderVRLoadConfigurationFile,
    BlenderVRLoadBlenderScene,
    BlenderVRLauncher
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
