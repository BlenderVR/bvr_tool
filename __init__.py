#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "BlenderVR",
    "author": "David Poirier-Quinot",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "3D View > Toolbox",
    "description": "A collection of tools to configure your BlenderVR environment.",
    "warning": "",
    'tracker_url': 'https://github.com/BlenderVR/source/issues',
    "wiki_url": "http://blendervr.limsi.fr",
    'support': 'COMMUNITY',
    "category": "Game Engine"
}

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    import bpy
    from bpy.props import (
            StringProperty,
            EnumProperty,
            PointerProperty
            )
    from bpy.types import (
            PropertyGroup
            )
    from . import (
            ui,
            operators
            )
import imp

class BlenderVRSettings(PropertyGroup):
    screen_setup = EnumProperty(
            name="Screen",
            description="VR architecture screen setup",
            items=(('console_debug', "Console Debug", ""),
                   ('dk2_debug', "DK2 Debug", "")),
            default='console_debug',
            )
    # config_file_path = StringProperty(
    #         name="Configuration File Path",
    #         description="Path to the configuration file",
    #         default="//", maxlen=1024, subtype="FILE_PATH",
    #         )
    config_file_path = StringProperty(
            name="Configuration File Path",
            description="Path to the configuration file",
            default="/Users/AstrApple/.config/blendervr/main_pers1.1.xml", maxlen=1024, subtype="FILE_PATH",
            )
    blend_scene_file_path = StringProperty(
            name="Blender File Path",
            description="Path to the blend scene",
            default="//", maxlen=1024, subtype="FILE_PATH",
            )
    processor_file_path = StringProperty(
            name="Processor File Path",
            description="Path to the processor file",
            default="//", maxlen=1024, subtype="FILE_PATH",
            )
# ############################################################
# Un/Registration
# ############################################################

def register():

    bpy.utils.register_class(BlenderVRSettings)

    ui.register()
    operators.register()

    bpy.types.Scene.blendervr = PointerProperty(type=BlenderVRSettings)


def unregister():

    bpy.utils.unregister_class(BlenderVRSettings)

    ui.unregister()
    operators.unregister()

    del bpy.types.Scene.blendervr
