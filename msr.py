# Code heavily borrowed from openreview-py's examples: https://openreview-py.readthedocs.io/en/latest/examples.html

from collections import defaultdict, deque

import openreview
import io
import os
import json
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class MSR:
    def _init_():
     guest_client = openreview.Client(baseurl='https://api.openreview.net')
     submissions = openreview.tools.iterget_notes(
             guest_client, invitation='ICLR.cc/2021/Conference/-/Blind_Submission')
     submissions_by_forum = {n.forum: n for n in submissions}
     print('getting metadata...')

# There should be 3 reviews per forum.
     reviews = openreview.tools.iterget_notes(
         guest_client, invitation='ICLR.cc/2021/Conference/Paper.*/-/Official_Review')
     reviews_by_forum = defaultdict(list)
     for review in reviews:
         reviews_by_forum[review.forum].append(review)

# Build a list of metadata.
# For every paper (forum), get the review ratings
     metadata = []
     means, medians, all_scores = [], [], []
     for forum in submissions_by_forum:
         forum_reviews = reviews_by_forum[forum]
         review_ratings = [n.content['rating'] for n in forum_reviews]
         review_scores = []
         for score in review_ratings:
             idx = score.find(':')
             review_scores.append(int(score[:idx]))

         for s in review_scores:
             all_scores.append(s)
         mean = statistics.mean(review_scores)
         median = statistics.median(review_scores)
         means.append(mean)
         medians.append(median)

         forum_metadata = {
             'forum': forum,
             'url': 'https://openreview.net/forum?id=' + forum,
             'title': submissions_by_forum[forum].content['title'],
             'scores': review_scores,
             'avg_score': mean
         }
         metadata.append(forum_metadata)
     pd.set_option('display.max_columns', None)
     pd.set_option('display.max_rows', None)

     df = pd.DataFrame(metadata)
     df = df.sort_values(by=['avg_score'], ascending=False)
     print('Mean: ', statistics.mean(means))
     print('Medians: ', statistics.mean(medians))
     sns.distplot(means, kde=False, color='red').set_title('Distribution of Average Scores')
     sns.despine()

     def make_clickable(val):
    # target _blank to open new window
         return '<a target="_blank" href="{}">{}</a>'.format(val, val)
     df.style.format({'url': make_clickable})
     df.style.hide_index()
     df = df.drop(columns=['forum'])
     df = df.round(2)

     print(df.to_string())

     def sla_violation(a):
      if a==1 :
       return 0.01
      elif a==11 :
       return 0.06
      elif a==21:
       return 0.09
      elif a==31:
       return 0.12
      elif a==41:
       return 0.14