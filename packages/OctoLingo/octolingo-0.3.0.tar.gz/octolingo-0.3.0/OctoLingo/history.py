import json
import os

class TranslationHistory:
    def __init__(self, history_file='translation_history.json'):
        self.history_file = history_file
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def log_translation(self, source_text, translated_text, src_language, dest_language):
        """Log a translation to the history."""
        with open(self.history_file, 'r+') as f:
            history = json.load(f)
            history.append({
                'source_text': source_text,
                'translated_text': translated_text,
                'src_language': src_language,
                'dest_language': dest_language
            })
            f.seek(0)
            json.dump(history, f, indent=4)

    def get_history(self):
        """Retrieve the translation history."""
        with open(self.history_file, 'r') as f:
            return json.load(f)