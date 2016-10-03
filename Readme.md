# Tasteful Tweets & Tasteful Graphs
A hackathon project from `#peacehackldn`

## Tasteful Tweets
Seeking to turn hateful tweets into something a little more funny

### Example
From

![Rude tweet from Donald Trump](./out/rude.png)

to

![Altered tweet by us](./out/less-rude.png)

### How
See `-h` flag for running instructions.

Sentiment analysis is done for an account to find most hateful tweet scoring using naive Bayes classifier and a formula we devised taking into account `./dict/terrible.txt` words, using words found under `./dict/bad...` and `./dict/good...` replacement is done.

### Todo
- Better replacement and training data [Hatebase]

## Tasteful Graphs
Find someone's influencing more friendly friends, via graph representation of a twitter account and their followers with colour coding according to sentiment analysis score

### Example
![Graph of Dan Telfer and followers](./out/graph.png)

### How
Averages our sentiment score from their most recent *n* tweets and from *p* followers and their followers <sub>and their followers and their...</sub>, repeated *q* times

### Todo
- Filter according to interests so you can find
- Hover show twitter handles

## Dependancies
- `nltk` plus `punkt` and  either `movie_reviews` or whatever corpus you wanna train on
- `twython`

# References
This code would not be possible without code shared from (streamhacker)[http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/] for NB classifier, (networkx)[https://github.com/networkx/networkx/tree/master/examples/javascript] for their json graph deployment and (heatmap)[http://bl.ocks.org/oyyd/859fafc8122977a3afd6] for colours and layout.
