#!pip install wordcloud
# pip install matplotlib

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# df = pd.read_csv(
#   "/Users/damon/Documents/SIT/Y2T2/ICT2107/wordcount.csv", index_col=0)

df = pd.read_csv(
    "/Users/damon/Documents/SIT/Y2T2/ICT2107/wordcount_sampleoutput.txt", sep=",", usecols=['word', 'count'], names=['word', 'count'], header=0)
print(df)

word_dict = df.set_index('word')['count'].to_dict()

wordcloud = WordCloud(width=800, height=400,
                      background_color='white').generate_from_frequencies(word_dict)

wordcloud.to_file('wordcloud.png')

# plot the wordcloud
plt.figure(figsize=(12, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
