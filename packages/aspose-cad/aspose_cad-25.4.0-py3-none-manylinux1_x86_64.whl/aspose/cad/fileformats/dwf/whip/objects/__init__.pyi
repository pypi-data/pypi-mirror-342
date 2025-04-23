from typing import List, Optional, Dict, Iterable
import io
import aspose.pycore
import aspose.pydrawing
import aspose.cad
import aspose.cad.annotations
import aspose.cad.cadexceptions
import aspose.cad.cadexceptions.compressors
import aspose.cad.cadexceptions.imageformats
import aspose.cad.exif
import aspose.cad.exif.enums
import aspose.cad.fileformats
import aspose.cad.fileformats.bitmap
import aspose.cad.fileformats.bmp
import aspose.cad.fileformats.cad
import aspose.cad.fileformats.cad.cadconsts
import aspose.cad.fileformats.cad.cadobjects
import aspose.cad.fileformats.cad.cadobjects.acadtable
import aspose.cad.fileformats.cad.cadobjects.assoc
import aspose.cad.fileformats.cad.cadobjects.attentities
import aspose.cad.fileformats.cad.cadobjects.background
import aspose.cad.fileformats.cad.cadobjects.blocks
import aspose.cad.fileformats.cad.cadobjects.datatable
import aspose.cad.fileformats.cad.cadobjects.dictionary
import aspose.cad.fileformats.cad.cadobjects.dimassoc
import aspose.cad.fileformats.cad.cadobjects.field
import aspose.cad.fileformats.cad.cadobjects.hatch
import aspose.cad.fileformats.cad.cadobjects.mlinestyleobject
import aspose.cad.fileformats.cad.cadobjects.objectcontextdata
import aspose.cad.fileformats.cad.cadobjects.perssubentmanager
import aspose.cad.fileformats.cad.cadobjects.polylines
import aspose.cad.fileformats.cad.cadobjects.section
import aspose.cad.fileformats.cad.cadobjects.sunstudy
import aspose.cad.fileformats.cad.cadobjects.tablestyle
import aspose.cad.fileformats.cad.cadobjects.underlaydefinition
import aspose.cad.fileformats.cad.cadobjects.vertices
import aspose.cad.fileformats.cad.cadobjects.wipeout
import aspose.cad.fileformats.cad.cadparameters
import aspose.cad.fileformats.cad.cadtables
import aspose.cad.fileformats.cad.dwg
import aspose.cad.fileformats.cad.dwg.acdbobjects
import aspose.cad.fileformats.cad.dwg.appinfo
import aspose.cad.fileformats.cad.dwg.r2004
import aspose.cad.fileformats.cad.dwg.revhistory
import aspose.cad.fileformats.cad.dwg.summaryinfo
import aspose.cad.fileformats.cad.dwg.vbaproject
import aspose.cad.fileformats.cf2
import aspose.cad.fileformats.cgm
import aspose.cad.fileformats.cgm.classes
import aspose.cad.fileformats.cgm.commands
import aspose.cad.fileformats.cgm.elements
import aspose.cad.fileformats.cgm.enums
import aspose.cad.fileformats.cgm.export
import aspose.cad.fileformats.cgm.import
import aspose.cad.fileformats.collada
import aspose.cad.fileformats.collada.fileparser
import aspose.cad.fileformats.collada.fileparser.elements
import aspose.cad.fileformats.dgn
import aspose.cad.fileformats.dgn.dgnelements
import aspose.cad.fileformats.dgn.dgntransform
import aspose.cad.fileformats.dicom
import aspose.cad.fileformats.draco
import aspose.cad.fileformats.dwf
import aspose.cad.fileformats.dwf.dwfxps
import aspose.cad.fileformats.dwf.dwfxps.fixedpage
import aspose.cad.fileformats.dwf.dwfxps.fixedpage.dto
import aspose.cad.fileformats.dwf.emodelinterface
import aspose.cad.fileformats.dwf.eplotinterface
import aspose.cad.fileformats.dwf.whip
import aspose.cad.fileformats.dwf.whip.objects
import aspose.cad.fileformats.dwf.whip.objects.drawable
import aspose.cad.fileformats.dwf.whip.objects.drawable.text
import aspose.cad.fileformats.dwf.whip.objects.service
import aspose.cad.fileformats.dwf.whip.objects.service.font
import aspose.cad.fileformats.fbx
import aspose.cad.fileformats.glb
import aspose.cad.fileformats.glb.animations
import aspose.cad.fileformats.glb.geometry
import aspose.cad.fileformats.glb.geometry.vertextypes
import aspose.cad.fileformats.glb.io
import aspose.cad.fileformats.glb.materials
import aspose.cad.fileformats.glb.memory
import aspose.cad.fileformats.glb.runtime
import aspose.cad.fileformats.glb.scenes
import aspose.cad.fileformats.glb.toolkit
import aspose.cad.fileformats.glb.transforms
import aspose.cad.fileformats.glb.validation
import aspose.cad.fileformats.ifc
import aspose.cad.fileformats.ifc.header
import aspose.cad.fileformats.ifc.ifc2x3
import aspose.cad.fileformats.ifc.ifc2x3.entities
import aspose.cad.fileformats.ifc.ifc2x3.types
import aspose.cad.fileformats.ifc.ifc4
import aspose.cad.fileformats.ifc.ifc4.entities
import aspose.cad.fileformats.ifc.ifc4.types
import aspose.cad.fileformats.ifc.ifc4x3
import aspose.cad.fileformats.ifc.ifc4x3.entities
import aspose.cad.fileformats.ifc.ifc4x3.types
import aspose.cad.fileformats.iges
import aspose.cad.fileformats.iges.commondefinitions
import aspose.cad.fileformats.iges.drawables
import aspose.cad.fileformats.jpeg
import aspose.cad.fileformats.jpeg2000
import aspose.cad.fileformats.obj
import aspose.cad.fileformats.obj.elements
import aspose.cad.fileformats.obj.mtl
import aspose.cad.fileformats.obj.vertexdata
import aspose.cad.fileformats.obj.vertexdata.index
import aspose.cad.fileformats.pdf
import aspose.cad.fileformats.plt
import aspose.cad.fileformats.plt.pltparsers
import aspose.cad.fileformats.plt.pltparsers.pltparser
import aspose.cad.fileformats.plt.pltparsers.pltparser.pltplotitems
import aspose.cad.fileformats.png
import aspose.cad.fileformats.psd
import aspose.cad.fileformats.psd.resources
import aspose.cad.fileformats.shx
import aspose.cad.fileformats.stl
import aspose.cad.fileformats.stl.stlobjects
import aspose.cad.fileformats.stp
import aspose.cad.fileformats.stp.helpers
import aspose.cad.fileformats.stp.items
import aspose.cad.fileformats.stp.reader
import aspose.cad.fileformats.stp.stplibrary
import aspose.cad.fileformats.stp.stplibrary.core
import aspose.cad.fileformats.stp.stplibrary.core.models
import aspose.cad.fileformats.svg
import aspose.cad.fileformats.threeds
import aspose.cad.fileformats.threeds.elements
import aspose.cad.fileformats.tiff
import aspose.cad.fileformats.tiff.enums
import aspose.cad.fileformats.tiff.filemanagement
import aspose.cad.fileformats.tiff.instancefactory
import aspose.cad.fileformats.tiff.tifftagtypes
import aspose.cad.fileformats.u3d
import aspose.cad.fileformats.u3d.elements
import aspose.cad.imageoptions
import aspose.cad.imageoptions.svgoptionsparameters
import aspose.cad.measurement
import aspose.cad.palettehelper
import aspose.cad.primitives
import aspose.cad.sources
import aspose.cad.timeprovision
import aspose.cad.watermarkguard

class DwfFileHeuristics:
    '''Represents file heuristics'''
    
    def clone(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfFileHeuristics:
        ...
    
    @property
    def w2d_channel(self) -> bool:
        ...
    
    @w2d_channel.setter
    def w2d_channel(self, value : bool):
        ...
    
    @property
    def should_apply_transform(self) -> bool:
        ...
    
    @should_apply_transform.setter
    def should_apply_transform(self, value : bool):
        ...
    
    @property
    def transform(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfWhipTransform:
        '''Gets transform'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.cad.fileformats.dwf.whip.objects.DwfWhipTransform):
        '''Sets transform'''
        ...
    
    ...

class DwfString:
    '''Represents String'''
    
    @property
    def ascii_string(self) -> str:
        ...
    
    @ascii_string.setter
    def ascii_string(self, value : str):
        ...
    
    ...

class DwfWhipAttribute(DwfWhipObject):
    '''Represents object familt attributes'''
    
    @property
    def is_materialized(self) -> bool:
        ...
    
    ...

class DwfWhipLayer(DwfWhipAttribute):
    '''Represents Layer'''
    
    @property
    def is_materialized(self) -> bool:
        ...
    
    @property
    def name(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfString:
        '''Gets name of DwfWhipLayer'''
        ...
    
    @property
    def number(self) -> int:
        '''Gets number'''
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @property
    def incarnation(self) -> int:
        '''Gets incarnation'''
        ...
    
    ...

class DwfWhipLogicalBox:
    '''Represents logical box'''
    
    @property
    def min(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfWhipLogicalPoint:
        '''Gets minimal point of box'''
        ...
    
    @property
    def max(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfWhipLogicalPoint:
        '''Gets maximal point of box'''
        ...
    
    ...

class DwfWhipLogicalPoint:
    '''Represents Logical point'''
    
    @property
    def x(self) -> float:
        '''Gets X coordinate'''
        ...
    
    @x.setter
    def x(self, value : float):
        '''Sets X coordinate'''
        ...
    
    @property
    def y(self) -> float:
        '''Gets Y coordinate'''
        ...
    
    @y.setter
    def y(self, value : float):
        '''Sets Y coordinate'''
        ...
    
    ...

class DwfWhipObject:
    '''Represents base whip object'''
    
    @property
    def is_materialized(self) -> bool:
        ...
    
    ...

class DwfWhipTransform:
    '''Represents transform of scene'''
    
    def set_rotation(self, rotation : int) -> None:
        '''Sets rotation angle
        
        :param rotation: rotation angle'''
        ...
    
    @property
    def translate(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfWhipLogicalPoint:
        '''Gets translate'''
        ...
    
    @translate.setter
    def translate(self, value : aspose.cad.fileformats.dwf.whip.objects.DwfWhipLogicalPoint):
        '''Sets translate'''
        ...
    
    @property
    def x_scale(self) -> float:
        ...
    
    @x_scale.setter
    def x_scale(self, value : float):
        ...
    
    @property
    def y_scale(self) -> float:
        ...
    
    @y_scale.setter
    def y_scale(self, value : float):
        ...
    
    @property
    def rotation(self) -> int:
        '''Gets rotation angle'''
        ...
    
    @rotation.setter
    def rotation(self, value : int):
        '''Sets rotation angle'''
        ...
    
    ...

class DwfWhipViewPort(aspose.cad.fileformats.dwf.whip.objects.drawable.DwfWhipDrawable):
    '''Represents view port'''
    
    @property
    def is_materialized(self) -> bool:
        ...
    
    @property
    def id(self) -> str:
        ...
    
    @property
    def childs(self) -> Iterable[aspose.cad.IDrawingEntity]:
        ...
    
    @property
    def color(self) -> aspose.cad.Color:
        '''Gets Color'''
        ...
    
    @color.setter
    def color(self, value : aspose.cad.Color):
        '''Sets Color'''
        ...
    
    @property
    def line_weight(self) -> aspose.cad.fileformats.dwf.whip.objects.service.DwfWhipLineWeight:
        ...
    
    @line_weight.setter
    def line_weight(self, value : aspose.cad.fileformats.dwf.whip.objects.service.DwfWhipLineWeight):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def transform_matrix(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfWhipTransform:
        ...
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.cad.fileformats.dwf.whip.objects.DwfWhipTransform):
        ...
    
    @property
    def line_style(self) -> aspose.cad.fileformats.dwf.whip.objects.service.DwfWhipLineStyle:
        ...
    
    @line_style.setter
    def line_style(self, value : aspose.cad.fileformats.dwf.whip.objects.service.DwfWhipLineStyle):
        ...
    
    @property
    def layer_index(self) -> int:
        ...
    
    @layer_index.setter
    def layer_index(self, value : int):
        ...
    
    @property
    def min_point(self) -> aspose.cad.fileformats.cad.cadobjects.Cad3DPoint:
        ...
    
    @property
    def max_point(self) -> aspose.cad.fileformats.cad.cadobjects.Cad3DPoint:
        ...
    
    @property
    def contour_set(self) -> aspose.cad.fileformats.dwf.whip.objects.drawable.DwfWhipContourSet:
        ...
    
    @property
    def name(self) -> aspose.cad.fileformats.dwf.whip.objects.DwfString:
        '''Gets name of vieport'''
        ...
    
    @property
    def incarnation(self) -> int:
        '''Gets Incarnation'''
        ...
    
    ...

