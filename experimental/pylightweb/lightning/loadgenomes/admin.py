from django.contrib import admin
from nested_inlines.admin import NestedModelAdmin, NestedTabularInline

# We only want the annotations to be modifiable by the admin, not the tiles
from loadgenomes.models import Tile, TileVariant, TileVarAnnotation, varLocusAnnotation, tileLocusAnnotation

class AnnotationInLine(NestedTabularInline):
    model = TileVarAnnotation
    extra = 0
    can_delete=False

##class LocusInLine(NestedTabularInline):
##    model = varLocusAnnotation
##    extra = 0
##    can_delete=False
    
class UpperLocusInLine(NestedTabularInline):
    model = tileLocusAnnotation
    extra = 0
    can_delete=False
    
class TileVarInLine(NestedTabularInline):
    model = TileVariant
    extra = 0
    #Awesome thing would be to customize whether the tags are collapsed if the tags are actually different
    fieldsets = [
        (None, {'fields':['length', 'population_size', 'md5sum', 'sequence']}),
        ('Tags', {'fields':['start_tag', 'end_tag'], 'classes': ['collapse']}),
    ]
    #inlines = [LocusInLine, AnnotationInLine,]
    inlines = [AnnotationInLine,]
    can_delete=False

class TileAdmin(NestedModelAdmin):
    list_display = ('getTileString', 'created')
    #search_fields = ['tilename']
    inlines = [UpperLocusInLine,TileVarInLine,]
    can_delete=False
    
admin.site.register(Tile, TileAdmin)
