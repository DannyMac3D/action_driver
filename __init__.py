# ##### BEGIN GPL LICENSE BLOCK #####
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
# ##### END GPL LICENSE BLOCK #####





bl_info = {
    "name": "Action Driver",
    "author": "Danny Mac",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging"
}

import bpy
from mathutils import *

from .operators import ACTION_DRIVER_OT_MakeController
from .ui import ACTION_DRIVER_PT_ui
from .ui import ACTION_DRIVER_PT_sliders_ui

classes = (ACTION_DRIVER_OT_MakeController,
           ACTION_DRIVER_PT_ui,
           ACTION_DRIVER_PT_sliders_ui)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.action_namer = bpy.props.StringProperty\
      (
        name = "Name Action",
        default=""
      )

    bpy.types.Scene.inverted_action = bpy.props.BoolProperty\
        (
            name="Inverted Action",
            default=False
        )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.action_namer
    del bpy.types.Scene.inverted_action



