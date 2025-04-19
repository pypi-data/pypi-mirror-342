from .core import AncientScripts
from mappings import (
    persian_to_cuneiform_mapping, persian_to_manichaean_mapping, 
    persian_to_hieroglyph_mapping, english_to_cuneiform_mapping,
    english_to_pahlavi_mapping, persian_to_pahlavi_mapping,
    english_to_manichaean_mapping, english_to_hieroglyph_mapping,
    linear_b_dict, conversion_dict, convert_to_cuneiform,
    convert_to_pahlavi, convert_to_manichaean, convert_to_hieroglyph,
    text_to_linear_b_optimized, convert_to_akkadian, convert_to_oracle_bone
)
__version__ = "1.0.0"
__all__ = ['AncientScripts']