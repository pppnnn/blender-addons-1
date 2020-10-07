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

import bpy

class GP_PT_sidebarPanel(bpy.types.Panel):
    bl_label = "Grease Pencil Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Grease Pencil"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        # Box deform ops
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('gp.latticedeform', icon ="MOD_MESHDEFORM")# MOD_LATTICE, LATTICE_DATA

        # Straight line ops
        layout.operator('gp.straight_stroke', icon ="CURVE_PATH")# IPO_LINEAR


        # Expose Native view operators
        # if context.scene.camera:
        row = layout.row(align=True)
        row.operator('view3d.zoom_camera_1_to_1', text = 'Zoom 1:1', icon = 'ZOOM_PREVIOUS')# FULLSCREEN_EXIT?
        row.operator('view3d.view_center_camera', text = 'Zoom Fit', icon = 'FULLSCREEN_ENTER')


def menu_boxdeform_entry(self, context):
    """Transform shortcut to append in existing menu"""
    layout = self.layout
    obj = bpy.context.object
    # {'EDIT_GPENCIL', 'PAINT_GPENCIL','SCULPT_GPENCIL','WEIGHT_GPENCIL', 'VERTEX_GPENCIL'}
    if obj and obj.type == 'GPENCIL' and context.mode in {'OBJECT', 'EDIT_GPENCIL', 'PAINT_GPENCIL'}:
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('gp.latticedeform', text='Box Deform')

def menu_stroke_entry(self, context):
    layout = self.layout
    # Gpencil modes : {'EDIT_GPENCIL', 'PAINT_GPENCIL','SCULPT_GPENCIL','WEIGHT_GPENCIL', 'VERTEX_GPENCIL'}
    if context.mode in {'EDIT_GPENCIL', 'PAINT_GPENCIL'}:
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('gp.straight_stroke', text='Straight Stroke')

def menu_brush_pack(self, context):
    layout = self.layout
    # if context.mode in {'EDIT_GPENCIL', 'PAINT_GPENCIL'}:
    self.layout.operator_context = 'INVOKE_DEFAULT'
    layout.operator('gp.import_brush_pack')#, text='Import brush pack'


def register():
    bpy.utils.register_class(GP_PT_sidebarPanel)
    ## VIEW3D_MT_edit_gpencil.append# Grease pencil menu
    bpy.types.VIEW3D_MT_transform_object.append(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_gpencil_transform.append(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_gpencil_stroke.append(menu_stroke_entry)
    bpy.types.VIEW3D_MT_brush_gpencil_context_menu.append(menu_brush_pack)


def unregister():
    bpy.types.VIEW3D_MT_brush_gpencil_context_menu.remove(menu_brush_pack)
    bpy.types.VIEW3D_MT_transform_object.remove(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_gpencil_transform.remove(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_gpencil_stroke.remove(menu_stroke_entry)
    bpy.utils.unregister_class(GP_PT_sidebarPanel)
