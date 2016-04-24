import twitter as tw
import json
import requests
from textblob import TextBlob
from nltk.tokenize import BlanklineTokenizer
import random


def tweet_content():
    """Generate tweet string (140 characters or less)
    """

#    with open('basho.txt', 'r') as content_file:
#        content = content_file.read()
    r = requests.get("http://novicevagabond.com/projects/haiku/basho.txt")
    content = r.content

#print content

    tokenizer = BlanklineTokenizer()
    cleaned_content = content.lower()
    corpus = TextBlob(cleaned_content,  tokenizer=tokenizer)

    haiku = corpus.sentences
#print haiku

    bigrams = corpus.ngrams(n=2)
    trigrams = corpus.ngrams(n=3)

#print bigrams
    dict = {}
    for bigram in bigrams:
        k = bigram[0]
        v = bigram[1]
        if k in dict:
            if v in dict[k]:
                dict[k][v] = dict[k][v] + 1
            else:
                dict[k][v] = 1
        else:
            dict[k] = { v : 1}

#print dict

    def weighted_choice(map):
        choices = [] 
        for k in map:
            #print k 
            for n in range(1, map[k] + 1):
                choices.append(k)
        #print choices
        choice = random.choice(choices)
        #print choice
        return choice

    seed = random.choice(dict.keys())
    length = random.randint(11,15) 

    output = [seed]
#print output
    for i in range(length):
        output.append(weighted_choice(dict[output[i]]))

    whitespace = " "
    line1 = whitespace.join(output[0:4])
    line2 = whitespace.join(output[4:9])
    line3 = whitespace.join(output[9:])
    line4 = "-- #markov_basho_haiku"
    sep = "\n"
    tweet = sep.join([line1, line2, line3, line4]);
#    print tweet
    return tweet 
#    return "test tweet"


def send_tweet(event, context):
    """Post tweet
    """
    with open("twitter_credentials.json", "r") as f:
        credentials = json.load(f)
    t = tw.Api(**credentials)
    try:
        status = tweet_content()
        t.PostUpdate(status=status)
        return "Tweeted {}".format(status)
    except Exception as e:
        return e.message

if __name__ == '__main__':
    print send_tweet(None, None)
    #print tweet_content()
