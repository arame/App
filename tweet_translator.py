from googletrans import Translator
import sys
from config import Hyper

class TweetTranslator:
    def to_english(text, language):
        if language == "und":
            return ""

        translator = Translator()
        # translate raw tweet
        try:
            translated = translator.translate(text, src=language, dest='en')
            if translated.src == language and translated.dest == 'en':
                en_text = translated.text
                return en_text

            if Hyper.MustTranslate:
                sys.exit(f"Problem with Translator. Language: {language} not translated to English")

            return ""

        except ValueError:
            print(f"invalid language: {language}")
            return ""
