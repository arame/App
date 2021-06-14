from googletrans import Translator

class TweetTranslator:
    def to_english(text, language):
        if language == "und":
            return ""

        translator = Translator()
        # translate raw tweet
        try:
            en_text = translator.translate(text, src=language, dest='en')
            # create column extracting the translated text
            #en_text = trans.apply(lambda x: x.text)
            return en_text
        except ValueError:
            print(f"invalid language: {language}")
            return ""
