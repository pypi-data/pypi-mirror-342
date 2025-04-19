from googletrans import Translator
import asyncio
from OctoLingo.utils import split_text_into_chunks, cache_translation
from OctoLingo.exceptions import TranslationError
from typing import Union, Tuple
from OctoLingo.ocr import OctoOCR

class OctoLingo:
    def __init__(self):
        """Initialize the translator with Google Translate as the default provider."""
        self.translator = Translator()
        self.ocr = OctoOCR()

    def validate_language(self, language_code):
        """Validate if the target language is supported by the translation API."""
        # Hardcode supported languages for now
        supported_languages = ['ab', 'ace', 'ach', 'af', 'sq', 'alz', 'am', 'ar', 'hy', 'as', 'awa', 'ay', 'az', 'ban', 'bm','ba', 'eu', 'btx', 'bts', 'bbc', 'be', 'bem', 'bn', 'bew', 'bho', 'bik', 'bs', 'br', 'bg', 'bua', 'yue', 'ca', 'ceb', 'ny', 'zh', 'zh-CN', 'zh-TW', 'cv','co','crh','hr', 'cs', 'da','din', 'dv', 'doi', 'dov', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fj', 'fil','tl', 'fi', 'fr','fr-FR', 'fr-CA', 'fy', 'ff', 'gaa', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'cnh', 'ha', 'haw', 'iw', 'he', 'hil', 'hi', 'hmn', 'hu', 'hrx', 'is', 'ig', 'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'jv', 'kn', 'pam', 'kk', 'km', 'cgg', 'rw', 'ktu', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo', 'ltg', 'la', 'lv', 'lv', 'lij', 'li', 'ln', 'lt', 'lmo', 'luo', 'lb', 'mk', 'mai', 'mak', 'mg', 'ms', 'ms-Arab', 'ml', 'mt' , 'mi', 'mr', 'chm', 'mni-Mtei', 'min', 'lus', 'mn', 'my', 'nr', 'new', 'ne', 'nso', 'no', 'nus', 'oc', 'or', 'om', 'pag', 'pap', 'ps', 'ps', 'fa', 'pl', 'pt', 'pt-PT', 'pt-BR', 'pa', 'pa-Arab', 'qu', 'rom', 'ro', 'rn', 'ru', 'sm', 'sg', 'sa', 'gd', 'sr', 'st', 'crs', 'shn', 'sn', 'scn', 'szl', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'ss', 'sv', 'tg', 'ta', 'tt', 'te', 'tet', 'th', 'ti', 'ts','tn', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'yua'] 
        if language_code not in supported_languages:
            raise TranslationError(f"Unsupported language: {language_code}")
        return True

    def detect_language(self, text):
        """Detect the language of the input text."""
        try:
            detection = self.translator.detect(text)
            confidence = detection.confidence if detection.confidence is not None else 0.0
            return detection.lang, confidence
        except Exception as e:
            raise TranslationError(f"Language detection failed: {str(e)}")

    @cache_translation
    def translate(self, text, dest_language, src_language='auto', max_retries=3):
        """
        Translate text to the target language.
        :param text: Input text to translate.
        :param dest_language: Target language code (e.g., 'es' for Spanish).
        :param src_language: Source language code (default: 'auto' for auto-detection).
        :param max_retries: Maximum number of retries for failed translations.
        :return: Translated text and confidence score.
        """
        self.validate_language(dest_language)
        chunks = split_text_into_chunks(text)
        translated_chunks = []

        for chunk in chunks:
            for attempt in range(max_retries):
                try:
                    translated = self.translator.translate(chunk, dest=dest_language, src=src_language)
                    translated_chunks.append(translated.text)
                    break  # Exit retry loop if translation succeeds
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise TranslationError(f"Translation failed after {max_retries} retries: {str(e)}")

        return " ".join(translated_chunks), 1.0  # Confidence score is always 1.0 for now

    async def translate_async(self, text, dest_language, src_language='auto', max_retries=3):
        """Asynchronously translate text to the target language."""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.translate, text, dest_language, src_language, max_retries
        )

    def translate_batch(self, texts, dest_language, src_language='auto', max_retries=3):
        """
        Translate a batch of texts to the target language.
        :param texts: List of input texts to translate.
        :param dest_language: Target language code.
        :param src_language: Source language code (default: 'auto').
        :param max_retries: Maximum number of retries for failed translations.
        :return: List of translated texts and confidence scores.
        """
        return [self.translate(text, dest_language, src_language, max_retries) for text in texts]
    
    def translate_file(
        self,
        file_path: str,
        dest_language: str,
        src_language: str = 'auto',
        max_retries: int = 3
    ) -> Tuple[str, float]:
        """
        Translate text from a file (image, PDF, or Word document).
        
        Args:
            file_path (str): Path to the file to translate.
            dest_language (str): Target language code.
            src_language (str): Source language code (default: 'auto').
            max_retries (int): Maximum number of retries for failed translations.
            
        Returns:
            Tuple[str, float]: Translated text and confidence score.
        """
        extracted_text, _ = self.ocr.extract_text(file_path)
        return self.translate(extracted_text, dest_language, src_language, max_retries)
    
    async def translate_file_async(
        self,
        file_path: str,
        dest_language: str,
        src_language: str = 'auto',
        max_retries: int = 3
    ) -> Tuple[str, float]:
        """
        Asynchronously translate text from a file.
        
        Args:
            file_path (str): Path to the file to translate.
            dest_language (str): Target language code.
            src_language (str): Source language code (default: 'auto').
            max_retries (int): Maximum number of retries for failed translations.
            
        Returns:
            Tuple[str, float]: Translated text and confidence score.
        """
        extracted_text, _ = self.ocr.extract_text(file_path)
        return await self.translate_async(extracted_text, dest_language, src_language, max_retries)
    
    def translate_file_from_bytes(
        self,
        file_bytes: bytes,
        file_type: str,
        dest_language: str,
        src_language: str = 'auto',
        max_retries: int = 3
    ) -> Tuple[str, float]:
        """
        Translate text from file bytes.
        
        Args:
            file_bytes (bytes): File content as bytes.
            file_type (str): Type of file ('image', 'pdf', or 'word').
            dest_language (str): Target language code.
            src_language (str): Source language code (default: 'auto').
            max_retries (int): Maximum number of retries for failed translations.
            
        Returns:
            Tuple[str, float]: Translated text and confidence score.
        """
        extracted_text = self.ocr.extract_text_from_bytes(file_bytes, file_type)
        return self.translate(extracted_text, dest_language, src_language, max_retries)