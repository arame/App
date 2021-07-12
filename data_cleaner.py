import neattext.functions as nfx

class DataCleaner:
    # Data cleaning methods taken from https://www.kaggle.com/friskycodeur/nlp-with-disaster-tweets-bert-explained
    def lowercase_text(text):
        # The token id for a word should be the same whether it is capitalised or not
        # To ensure this happens, make the word lowercase
        return text.lower()

    def remove_noise(text):
        #print(f"Before clean: {text}")
        text = nfx.remove_userhandles(text)
        text = nfx.remove_currencies(text)
        text = nfx.remove_urls(text)
        text = nfx.remove_dates(text)
        text = nfx.remove_numbers(text)
        text = nfx.remove_html_tags(text)
        text = nfx.remove_multiple_spaces(text)     # also removes newline \n
        text = nfx.remove_punctuations(text)
        text = nfx.remove_special_characters(text)
        text = nfx.remove_non_ascii(text)
   
        #print(f"After clean: {text}")
        return text