# Modified the code from Dr. Yuhang Wang and Josh Gardner

import json
from pyspark import SparkContext
sc = SparkContext(appName="counting_stars")

input_file = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_business_updated.json")

def cat_star(data):
  cat_star_list = []
  stars = data.get('stars', None)
  city = data.get('city', None)
  neigh = data.get('neighborhoods', None)
  reviews = data.get('review_count', None)
  if stars >= 4:
      flag = 1
  else:
      flag = 0
  if neigh == []:
      cat_star_list.append((city, 'Unknown', 1, reviews, flag))
  else:
      for i in neigh:
          cat_star_list.append((city, i, 1, reviews, flag))
  return cat_star_list

raw_data = input_file.map(lambda line: json.loads(line)).flatMap(lambda x: cat_star(x))
# Number of businesses
buss_num = raw_data.map(lambda x: ((x[0], x[1]), x[2])).reduceByKey(lambda a, b: a+b)
# Number of reviews
review_num = raw_data.map(lambda x: ((x[0], x[1]), x[3])).reduceByKey(lambda a, b: a+b)
# Number of 4-stars or higher reviews
star_num = raw_data.map(lambda x: ((x[0], x[1]), x[4])).reduceByKey(lambda a, b: a+b)

# Join
joined_data = buss_num.fullOuterJoin(review_num).fullOuterJoin(star_num)

# Sort
sorted_data = joined_data.sortBy(lambda x: (x[0][0], -x[1][0][0]))

# Format
result_data = sorted_data.map(lambda x: (x[0][0] + '\t' + x[0][1] + '\t' + str(x[1][0][0]) + '\t'
                                        + str(x[1][0][1]) + '\t' + str(x[1][1])).encode('utf-8'))

result_data.saveAsTextFile("si618w17hw5-part1_haoyoliu")
