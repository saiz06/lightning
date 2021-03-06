from rest_framework import serializers

from tile_library.models import TileLocusAnnotation, TileVariant
from tile_library.constants import SUPPORTED_ASSEMBLY_CHOICES, CHR_CHOICES
##################### For returning information ######################

class GenomeVariantSerializer(serializers.Serializer):
    tile_variant_start_locus = serializers.IntegerField()
    tile_variant_end_locus = serializers.IntegerField()
    ref_start_locus = serializers.IntegerField()
    ref_end_locus = serializers.IntegerField()
    reference_bases = serializers.CharField()
    alternate_bases = serializers.CharField()

class TileVariantSerializer(serializers.Serializer):
    tile_variant_hex_string = serializers.CharField(max_length=15)
    tile_variant_cgf_string = serializers.CharField(max_length=16)
    tile_variant_int = serializers.IntegerField()
    num_positions_spanned = serializers.IntegerField()
    length = serializers.IntegerField()
    genome_variants = GenomeVariantSerializer(many=True)
    md5sum = serializers.CharField(max_length=40)
    sequence = serializers.CharField()

class RoughTileVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TileVariant
        fields = ('tile_variant_int', 'tile', 'num_positions_spanned', 'variant_value', 'length', 'md5sum', 'created', 'last_modified',
            'sequence', 'start_tag', 'end_tag')

class LocusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TileLocusAnnotation
        fields = ('assembly', 'chromosome', 'begin_int', 'end_int')


class PopulationVariantSerializer(serializers.Serializer):
    human_name = serializers.CharField(max_length=200)
    sequence = serializers.ListField(
        child=serializers.CharField(style={'type': 'textarea'}, allow_blank=True)
    )
    phase_groups_known = serializers.BooleanField(default=False)

################## For User Inputs ##################################

class PopulationQuerySerializer(serializers.Serializer):
    INDEX_CHOICES = (
        (0, '0-indexed'),
        (1, '1-indexed'),
        )
    assembly = serializers.ChoiceField(choices=SUPPORTED_ASSEMBLY_CHOICES)
    chromosome = serializers.ChoiceField(choices=CHR_CHOICES)
    indexing = serializers.ChoiceField(choices=INDEX_CHOICES, default=0)
    target_base = serializers.IntegerField()
    number_around = serializers.IntegerField(default=0)
    def validate_number_around(self, value):
        if value < 0:
            raise serializers.ValidationError("number_around must be greater than or equal to 0")
        return value

class PopulationRangeQuerySerializer(serializers.Serializer):
    INDEX_CHOICES = (
        (0, '0-indexed'),
        (1, '1-indexed'),
        )
    assembly = serializers.ChoiceField(choices=SUPPORTED_ASSEMBLY_CHOICES)
    chromosome = serializers.ChoiceField(choices=CHR_CHOICES)
    indexing = serializers.ChoiceField(choices=INDEX_CHOICES, default=0)
    lower_base = serializers.IntegerField()
    upper_base = serializers.IntegerField()
