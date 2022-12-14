# -*- coding: utf-8 -*-
"""Naive Bayes .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X1ItYol6nmvw-pYAFq4ry5EenhhX4t3H
"""

# Commented out IPython magic to ensure Python compatibility.
##### 2020 ####

!pip install --upgrade pandas
import pandas as pd
import re
import string
import warnings
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
!pip install Sastrawi
from wordcloud import WordCloud
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import gensim
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


pd.set_option('display.max_colwidth',250)
warnings.filterwarnings('ignore',category=DeprecationWarning)
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive',force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
from wordcloud import WordCloud
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import gensim
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


pd.set_option('display.max_colwidth',250)
warnings.filterwarnings('ignore',category=DeprecationWarning)
# %matplotlib inline

"""# New Section"""

url_dataset = '/content/drive/MyDrive/Datasets/vaksin/vaksin_data_kelompok3_label.csv'
dataset = pd.read_csv(url_dataset)

from google.colab import drive
drive.mount('/content/drive')

dataset.head(10)

pd.options.mode.chained_assignment = None  # default='warn'
dataset.VALUE[dataset.VALUE == 'SETUJU VAKSIN'] = 1
dataset.VALUE[dataset.VALUE == 'ANTI VAKSIN'] = 0

print(dataset.shape)

train = dataset[:350]
test = dataset [351:]

print(dataset.shape)
dataset.info()
dataset.head(10)

dataset.describe()



train['VALUE'].value_counts()

panjang_train_dataset = train['Tweet'].str.len()
panjang_test_dataset = test['Tweet' ].str.len()
plt.hist(panjang_train_dataset, bins=10, label='Train tweets')
plt.hist(panjang_test_dataset, bins = 10,label='Test tweets')
plt.legend()
plt.show()

gabung = train.append(test, ignore_index = True)
gabung['Tweet'] = gabung['Tweet'].fillna("aaa")
gabung.shape

gabung['Tweet'] = gabung['Tweet'].apply(lambda x:' '.join([w for w in x.split()if len(w)>3]))
gabung.head(3)

tokenisasi = gabung['Tweet'].apply(lambda x:x.split())
tokenisasi.head(3)

#bagian code 
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer() 
tokenisasi = tokenisasi.apply(lambda x: [stemmer.stem(i) for i in x])

for i in range(len(tokenisasi)):
    tokenisasi[i] = ' '.join(tokenisasi[i])
gabung['Tweet']=tokenisasi

"""#pemetaan kata2
kata2 = ' '.join([text for text in gabung['Tweet']])
wordcloud = WordCloud(width = 900, height= 600, random_state = 20, max_font_size = 80,background_color = 'white',min_font_size = 20).generate(kata2)
plt.figure(figsize=(10,7))

plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()
"""

#pemetaan kata2
kata2 = ' '.join([text for text in gabung['Tweet']])
wordcloud = WordCloud(width = 900, height= 600,random_state = 20, background_color = 'white', min_font_size = 12,max_font_size = 180).generate(kata2)
plt.figure(figsize=(10,7))

plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()

#setuju vaksin
kata_waras = ' '.join([text for text in gabung['Tweet'][gabung['VALUE']== 1]])
wordcloud = WordCloud(width = 900, height= 600, random_state = 20, background_color = 'white', min_font_size = 12,max_font_size = 180).generate(kata_waras)
plt.figure(figsize=(10,7))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()

#anti vaksin
kata_sakit = ' '.join([text for text in gabung['Tweet'][gabung['VALUE']== 0]])
wordcloud = WordCloud(width = 900, height= 600, random_state = 20, background_color = 'white', min_font_size = 12,max_font_size = 180).generate(kata_sakit)
plt.figure(figsize=(10,7))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()

#hashtag human (Kode tidak berguna)
def hashtag_unik(x):
    hashtag = []
    for i in x :
        ht = re.findall(r"#(\w+)",i)
        hashtag.append(ht)
    return hashtag

ht_normal = hashtag_unik(gabung['Tweet'][gabung['VALUE']=='SETUJU VAKSIN'])
ht_abnormal = hashtag_unik(gabung['Tweet'][gabung['VALUE']=='ANTI VAKSIN'])
ht_normal = sum(ht_normal,[])
ht_abnormal = sum(ht_abnormal,[])

tweet_normal = nltk.FreqDist(ht_normal)
df = pd.DataFrame({'Hashtag': list(tweet_normal.keys()),'Count': list(tweet_normal.values())})

df = df.nlargest(columns = 'Count', n = 20)
plt.figure(figsize=(16,5))
ax = sns.barplot(data=df, x = 'Hashtag', y = 'Count')
ax.set(ylabel= 'Count')
plt.show()

#setiap baris di matrix m menampung frekuensi token di dokumen 
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=0, max_features = 4)
bow = bow_vectorizer.fit_transform(gabung['Tweet'])
bow.shape
print(bow)

#TF-IDF

#TF = (berapa kali munculnya sebuah istilah di dokumen)/(jumlah istilah di dukumen)
#IDF = log(N/n) (N adalah jumlah dokumen dan n adalah jumlah dokumen yang memiliki istilah tersebut)

#TF-IDF = TF*IDF
tfidf_vectorizer = TfidfVectorizer(max_df = 0.9, max_features = 4)
tfidf = tfidf_vectorizer.fit_transform(gabung['Tweet'])
tfidf.shape

gabung = gabung.fillna(0)
X_train,X_test,y_train, y_test = train_test_split(bow,gabung['VALUE'], test_size = 0.1, random_state = 69)

print('X_train shape : ',X_train.shape)
print('X_test shape: ',X_test.shape)
print('y_train shape : ',y_train.shape)
print('y_test shape : ',y_test.shape)

print(y_test)

#multinomial naive bayes

model_naive_bayesnya = MultinomialNB().fit(X_train,y_train)
prediksi_naifnya = model_naive_bayesnya.predict(X_test)

dataset.info

#confusion matrix

plt.figure(dpi=600)
mat = confusion_matrix(y_test, prediksi_naifnya)
sns.heatmap(mat.T)

plt.title('Confusion matrix untuk bayes bodoh')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.show

score = accuracy_score(prediksi_naifnya,y_test)
print('akurasinya adalah : ', score*100,'%')



