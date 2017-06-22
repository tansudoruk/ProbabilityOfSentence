import re
import string
from nltk import ngrams
import mysql.connector
conn = mysql.connector.connect(user='root', password='8267836785', host='127.0.0.1', database='sys')
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

cur = conn.cursor(buffered=True)


cur.execute('''SELECT * FROM database_nlp''')
rows=cur.fetchall();
corpus_size = len(rows)



sentence = input('Enter sentence for bigram probability : ')
wordList = re.sub("[^\w]", " ",  sentence).split()
counter_second_word_after_first_word =0
probabilities=[]
exact_prob=1


first_word=wordList[0]
cur.execute('''SELECT count(*) FROM database_nlp WHERE WORD like " '''+first_word+''' " and IX like 1''')
counter_first_word=cur.fetchall()
if(counter_first_word[0][0]==0):
  counter_first_word=1/corpus_size
cur.execute('''SELECT count(*) FROM database_nlp WHERE IX like 1''')
counter_first_word_of_sentence=cur.fetchall()
probab=counter_first_word[0][0]/counter_first_word_of_sentence[0][0]
if(probab==0):
  probab=1/corpus_size
probabilities.append(probab)


bigrams = ngrams(sentence.split(), 2)
for grams in bigrams:
  first_word=grams[0]
  second_word=grams[1]

  cur.execute('''SELECT count(*) FROM database_nlp WHERE WORD like " '''+first_word+''' "''')
  counter_first_word=cur.fetchall()
  if(counter_first_word[0][0]==0):
    counter_first_word=1/corpus_size
  cur.execute('''Select COUNT(*) from database_nlp as R INNER JOIN
  (select FILENAME, NO, IX, WORD from database_nlp where WORD like " '''+first_word+''' ") AS T
  where R.FILENAME = T.FILENAME AND R.NO = T.NO AND R.IX = T.IX + 1 and R.WORD like " '''+second_word+''' "''')
  counter_second_word_after_first_word=cur.fetchall()
  prob=counter_second_word_after_first_word[0][0]/counter_first_word[0][0]
  if(prob==0.0):
    prob=1/corpus_size
  probabilities.append(prob)



  counter_second_word_after_first_word=0


print("probabilities")
print(probabilities)


for i in range (0,len(probabilities)):
  exact_prob=exact_prob*probabilities[i]
print("Multiplied (result) probability:")
print(exact_prob)


conn.commit()
conn.close()
