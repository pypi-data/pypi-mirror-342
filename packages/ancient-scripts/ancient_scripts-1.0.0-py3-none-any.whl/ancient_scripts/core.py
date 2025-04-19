"""
Ancient Scripts Conversion Module

This module provides functions to convert text to various ancient writing systems.
Supported scripts include Cuneiform, Pahlavi, Manichaean, Hieroglyphic, and more.

ماژول تبدیل متن به خطوط باستانی
این ماژول امکان تبدیل متن به سیستم‌های نوشتاری باستانی را فراهم می‌کند.
خطوط پشتیبانی شده شامل میخی، پهلوی، مانوی، هیروگلیف و ... می‌شود.
"""

from mappings import (
    persian_to_cuneiform_mapping, persian_to_manichaean_mapping, 
    persian_to_hieroglyph_mapping, english_to_cuneiform_mapping,
    english_to_pahlavi_mapping, persian_to_pahlavi_mapping,
    english_to_manichaean_mapping, english_to_hieroglyph_mapping,
    linear_b_dict, conversion_dict, convert_to_cuneiform,
    convert_to_pahlavi, convert_to_manichaean, convert_to_hieroglyph,
    text_to_linear_b_optimized, convert_to_akkadian, convert_to_oracle_bone
)

from deep_translator import GoogleTranslator




class  Ancientscripts:
    def __init__(self):
        self.supported_scripts = [
            'cuneiform', 'pahlavi', 'manichaean',
            'hieroglyph', 'hebrew', 'linear_b',
            'sanskrit', 'akkadian', 'oracle_bone'
        ]
    
    def cuneiform(self,text):
        """
        Convert text to Cuneiform script
        
        Args:
            text (str): Input text to be converted
            
        Returns:
            str: Text represented in Cuneiform characters
            
        مثال:
            >>> cuneiform("سلام")
            '𒀖𒇻𒀀𒈠'
            
        تبدیل متن به خط میخی
        ورودی:
            متن (رشته): متنی که باید تبدیل شود
        خروجی:
            رشته: متن به خط میخی
        """
        return convert_to_cuneiform(text)

    def pahlavi(self,text):
        """
        Convert text to Pahlavi (Middle Persian) script
        
        Args:
            text (str): Input text to be converted
            
        Returns:
            str: Text in Pahlavi script
            
        مثال:
            >>> pahlavi("دوست")
            '𐭃𐭅𐭎𐭕'
            
        تبدیل متن به خط پهلوی
        """
        return convert_to_pahlavi(text)

    def manichaean(self,text):
        """
        Convert text to Manichaean script
        
        Args:
            text (str): Input text to be converted
            
        Returns:
            str: Text in Manichaean characters
            
        مثال:
            >>> manichaean("نور")
            '𐫗𐫇𐫡'
            
        تبدیل متن به خط مانوی
        """
        return convert_to_manichaean(text)

    def hieroglyph(self,text):
        """
        Convert text to Egyptian Hieroglyphs
        
        Args:
            text (str): Input text to be converted
            
        Returns:
            str: Hieroglyphic representation
            
        مثال:
            >>> hieroglyph("خدا")
            '𓀭𓄿𓂝'
            
        تبدیل متن به هیروگلیف مصری
        """
        return convert_to_hieroglyph(text)

    def hebrew(self,text):
        """
        Translate text to Modern Hebrew
        
        Args:
            text (str): Text to translate
            
        Returns:
            str: Translated Hebrew text
            
        مثال:
            >>> hebrew("سلام")
            'שלום'
            
        ترجمه متن به زبان عبری مدرن
        """
        return GoogleTranslator(source='auto', target='iw').translate(text)

    def linear_b_optimized(self,text):
        """
        Convert text to Linear B script (optimized for Mycenaean Greek)
        
        Args:
            text (str): Input text
            
        Returns:
            str: Linear B representation
            
        مثال:
            >>> linear_b_optimized("پادشاه")
            '𐀞𐀅𐀯𐀀'
            
        تبدیل متن به خط Linear B (یونان باستان)
        """
        return text_to_linear_b_optimized(text)

    def sanskrit(self,text):
        """
        Translate text to Sanskrit
        
        Args:
            text (str): Text to translate
            
        Returns:
            str: Sanskrit translation
            
        مثال:
            >>> sanskrit("سلام")
            'नमस्ते'
             Input text
            
        Returns:
            str: Akkadian cuneiform representation
            
        مثال:
            >>> akkadian("شهر")
            '𒆠𒌁'
            
        تبدیل متن به خط
        ترجمه متن به زبان سانسکریت
        """
        return GoogleTranslator(source='auto', target='sa').translate(text)

    def akkadian(self,text):
        """
        Convert text to Akkadian cuneiform
        
        Args:
            text (str): آکدی (میخی)
        """
        return convert_to_akkadian(text)

    def oracle_bone(self,text):
        """
        Convert text to Oracle Bone script (Ancient Chinese)
        
        Args:
            text (str): Input text
            
        Returns:
            str: Oracle Bone characters
            
        مثال:
            >>> oracle_bone("آسمان")
            '𠀁𠕁'
            
        تبدیل متن به خط استخوان‌های پیشگویی (چین باستان)
        """
        return convert_to_oracle_bone(text)
    
        
        
        