import re, string

class DataCleaner:
    # Data cleaning methods taken from https://www.kaggle.com/friskycodeur/nlp-with-disaster-tweets-bert-explained
    def lowercase_text(text):
        return text.lower()

    def remove_noise(text):
        #print(f"Before clean: {text}")
        text = re.sub('\[.*?\]<.*?>+', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        #text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\w*\d\w*', '', text)
        #print(f"After clean: {text}")
        return text