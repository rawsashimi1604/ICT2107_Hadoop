import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# df = pd.read_csv(
#   "/Users/damon/Documents/SIT/Y2T2/ICT2107/wordcount.csv", index_col=0)

df = pd.read_csv(
    "./hadoop_data/part-r-00000", delimiter='\t', usecols=['word', 'count'], names=['word', 'count'])
print(df)


df = df[df['word'].str.startswith('CASE3_')]
dfByteDance = df[df['word'].str.startswith('CASE3_ByteDance')]
dfIBM = df[df['word'].str.startswith('CASE3_IBM')]
dfMicrosoft = df[df['word'].str.startswith('CASE3_Microsoft')]
dfSAP = df[df['word'].str.startswith('CASE3_SAP')]
dfNCS = df[df['word'].str.startswith('CASE3_NCS')]

dfIBM['word'] = dfIBM['word'].replace({'CASE3_IBM_': ''}, regex=True)
dfMicrosoft['word'] = dfMicrosoft['word'].replace(
    {'CASE3_Microsoft_': ''}, regex=True)
dfSAP['word'] = dfSAP['word'].replace({'CASE3_SAP_': ''}, regex=True)
dfNCS['word'] = dfNCS['word'].replace({'CASE3_NCS_': ''}, regex=True)
dfByteDance['word'] = dfByteDance['word'].replace(
    {'CASE3_ByteDance_': ''}, regex=True)

dfIBM = dfIBM.sort_values(by=['count'], ascending=False).head(40)
dfMicrosoft = dfMicrosoft.sort_values(by=['count'], ascending=False).head(40)
dfSAP = dfSAP.sort_values(by=['count'], ascending=False).head(40)
dfNCS = dfNCS.sort_values(by=['count'], ascending=False).head(40)
dfByteDance = dfByteDance.sort_values(by=['count'], ascending=False).head(40)
print(dfIBM)


word_dictIBM = dfIBM.set_index('word')['count'].to_dict()
word_dictMicrosoft = dfMicrosoft.set_index('word')['count'].to_dict()
word_dictSAP = dfSAP.set_index('word')['count'].to_dict()
word_dictNCS = dfNCS.set_index('word')['count'].to_dict()
word_dictByteDance = dfByteDance.set_index('word')['count'].to_dict()

wordcloudIBM = WordCloud(width=800, height=400,
                         background_color='white').generate_from_frequencies(word_dictIBM)

wordcloudIBM.to_file('wordcloudIBM.png')

wordcloudMicrosoft = WordCloud(width=800, height=400,
                               background_color='white').generate_from_frequencies(word_dictMicrosoft)
wordcloudMicrosoft.to_file('wordcloudMicrosoft.png')

wordcloudSAP = WordCloud(width=800, height=400,
                         background_color='white').generate_from_frequencies(word_dictSAP)
wordcloudSAP.to_file('wordcloudSAP.png')

wordcloudNCS = WordCloud(width=800, height=400,
                         background_color='white').generate_from_frequencies(word_dictNCS)
wordcloudNCS.to_file('wordcloudNCS.png')

wordcloudByteDance = WordCloud(width=800, height=400,
                               background_color='white').generate_from_frequencies(word_dictByteDance)
wordcloudByteDance.to_file('wordcloudByteDance.png')

# plot the wordcloud
plt.figure(figsize=(12, 10))
plt.imshow(wordcloudIBM, interpolation='bilinear')
plt.axis('off')
plt.show()
