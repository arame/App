import datetime as dt
#import wget
import os
import pandas as pd 
from twarc import Twarc
import jsonlines, json, csv, sys
from config import Hyper
from hydratedTweets import HydratedTweets

def main():
    hyper = Hyper()
    if not os.path.exists(hyper.dirOutput):
        os.makedirs(hyper.dirOutput)
    else:
        sys.exit("output directory already exists")
        
    os.chdir(hyper.dirOutput)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    consumer_key = "JLuZDxu7NcuPnTno0qgztrsoZ"                                  #@param {type:"string"}
    consumer_secret = "KL16xLRhvErmrMPOUvex3KbiGk3Ao9e0ziGhaDNq1y4tNuI9uW"      #@param {type:"string"}
    access_token = "1253768165923880961-Yhct3tMh9LYpdrFkazJl1KqvDzOTg2"         #@param {type:"string"}
    access_token_secret = "QpQykkfzvnVKg5pVyP0Kf3V1ZPAR30617XfoN3o43fDMu"       #@param {type:"string"}

    t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

    #@title Check Keywords to Hydrate { run: "auto" }
    coronavirus = True #@param {type:"boolean"}
    virus = False #@param {type:"boolean"}
    covid = False #@param {type:"boolean"}
    ncov19 = False #@param {type:"boolean"}
    ncov2019 = False #@param {type:"boolean"}
    keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}

    #@title Enter range of dates to Hydrate { run: "auto" }
    start_date = '2020-03-22' #@param {type:"date"}
    end_date = '2020-03-23' #@param {type:"date"}

    files = []
    covid_loc = "../COVID19_Tweets_Dataset"
    # Looks at each folder
    for folder in os.listdir(covid_loc):
        foldername = os.fsdecode(folder)
        # The folder name is a keyword. We continue for keywords selected above
        if keyword_dict.get(foldername.split()[0].lower()) == True:
            folderpath = os.path.join(covid_loc, foldername)
            # Each file is of the format [keyword]_yyyy_mm_dd.txt
            for file in os.listdir(folderpath):
                filename = os.fsdecode(file)
                date = filename[filename.index("_")+1:filename.index(".")]

                # If the date is within the required range, it is added to the
                # list of files to read.
                if (dt.datetime.strptime(start_date, "%Y-%m-%d").date() 
                <= dt.datetime.strptime(date, '%Y_%m_%d').date()
                <= dt.datetime.strptime(end_date, "%Y-%m-%d").date()):
                    files.append(os.path.join(folderpath, filename))
    # The final list is read, and each of the individual IDs is stored in a collective
    # set of IDs. Duplicates are removed.
    ids = set()
    for filename in files:
        with open(filename) as f:
            # The files are of the format: [id1,id2,id3,...,idn]
            # Remove the brackets and split on commas
            for i in f.readline().strip('][').replace(" ", "").split(","):
                ids.add(i) 
    # Number of tweets read.
    print(round((len(ids)/1000000), 3), "million unique tweets.")

    #@title Enter ID output file {run: "auto"}
    final_tweet_ids_filename = "final_ids.txt" #@param {type: "string"}
    # The set of IDs is stored in this file.
    with open(final_tweet_ids_filename, "w+") as f:
        for id in ids:
            f.write('%s\n' % id)

    #@title Set up Directory { run: "auto"}
    final_tweet_ids_filename = "final_ids.txt" #@param {type: "string"}
    output_filename = "output.csv" #@param {type: "string"}

    # Stores hydrated tweets here as jsonl objects
    # Contains one json object per line
    output_json_filename = output_filename[:output_filename.index(".")] + ".txt"
    ids = []
    with open(final_tweet_ids_filename, "r") as ids_file:
        ids = ids_file.read().split()
    hydrated_tweets = []
    ids_to_hydrate = set(ids)

    # Looks at the output file for already hydrated tweets
    if os.path.isfile(output_json_filename):
        with jsonlines.open(output_json_filename, "r") as reader:
            for i in reader.iter(type=dict, skip_invalid=True):
                # These tweets have already been hydrated. So remove them from ids_to_hydrate
                hydrated_tweets.append(i)
                ids_to_hydrate.remove(i["id_str"])
    print("Total IDs: " + str(len(ids)) + ", IDs to hydrate: " + str(len(ids_to_hydrate)))
    print("Hydrated: " + str(len(hydrated_tweets)))

    count = len(hydrated_tweets)
    start_index = count # The index from where tweets haven't been saved to the output_json_file
    # Stores hydrated tweets to output_json_file every num_save iterations.
    num_save  = 1000

    # Now, use twarc and start hydrating
    for tweet in t.hydrate(ids_to_hydrate):
        hydrated_tweets.append(tweet)
        count += 1
        # If num_save iterations have passed,
        if (count % num_save) == 0:
            if hyper.IsOutputCsv:
                tweets = HydratedTweets(hydrated_tweets[start_index:])
                tweets.output_to_csv()
            else:
                # Open the output file
                # NOTE: Even if the code stops during IO, only tweets from the current iteration are lost.
                # Older tweets are preserved as the file is written in append mode.
                with jsonlines.open(output_json_filename, "a") as writer:
                    print("Started IO")
                    # Now write the tweets from start_index. The other tweets don't have to be written
                    # as they were already written in a previous iteration or run.
                    for hydrated_tweet in hydrated_tweets[start_index:]:
                        writer.write(hydrated_tweet)
                    print("Finished IO")
            print("Saved " + str(count) + " hydrated tweets.")
            # Now, since everything has been written. Reset start_index
            start_index = count
    # There might be tweets unwritten in the last iteration if the count is not a multiple of num_tweets.
    # In that case, just write out the remainder of tweets.
    if count != start_index:
        print("Here with start_index", start_index)
        if hyper.IsOutputCsv:
            tweets = HydratedTweets(hydrated_tweets[start_index:])
            tweets.output_to_csv()
        else:
            with jsonlines.open(output_json_filename, "a") as writer:
                for hydrated_tweet in hydrated_tweets[start_index:]:
                    writer.write(hydrated_tweet) 

    if hyper.IsOutputCsv:
        sys.exit("** Completed output **")

    # Convert jsonl to csv
    output_json_filename = output_filename[:output_filename.index(".")] + ".txt"
    # These are the column name that are selected to be stored in the csv
    keyset = ["created_at", "id", "id_str", "full_text", "source", "truncated", "in_reply_to_status_id",
            "in_reply_to_status_id_str", "in_reply_to_user_id", "in_reply_to_user_id_str", 
            "in_reply_to_screen_name", "user", "coordinates", "place", "quoted_status_id",
            "quoted_status_id_str", "is_quote_status", "quoted_status", "retweeted_status", 
            "quote_count", "reply_count", "retweet_count", "favorite_count", "entities", 
            "extended_entities", "favorited", "retweeted", "possibly_sensitive", "filter_level", 
            "lang", "matching_rules", "current_user_retweet", "scopes", "withheld_copyright", 
            "withheld_in_countries", "withheld_scope", "geo", "contributors", "display_text_range",
            "quoted_status_permalink"]
    hydrated_tweets = []
    # Reads the current tweets
    with jsonlines.open(output_json_filename, "r") as reader:
        for i in reader.iter(type=dict, skip_invalid=True):
            hydrated_tweets.append(i)
    # Writes them out
    with  open(output_filename, "w+") as output_file:
        d = csv.DictWriter(output_file, keyset)
        d.writeheader()
        d.writerows(hydrated_tweets)

if __name__ == "__main__":
    main()

