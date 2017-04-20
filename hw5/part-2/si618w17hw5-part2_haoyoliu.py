import json
from pyspark import SparkContext

sc = SparkContext(appName="counting_stars")

city_file = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_business_updated.json")
review_file = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_review_updated.json")

def cat_review(data):
    cat_review_list = []
    user = data.get('user_id', None)
    buss = data.get('business_id', None)
    star = data.get('stars', None)
    cat_review_list.append((user, buss, star))

    return cat_review_list

def cat_city(data):
    cat_city_list = []
    city = data.get('city', None)
    buss = data.get('business_id', None)
    cat_city_list.append((city, buss))

    return cat_city_list

# Count the number of distinct cities that Yelp users wrote reviews in
def counting_users(users, cities, hist):
    distinct = users.fullOuterJoin(cities).map(lambda x: (x[1][0], x[1][1])).distinct()
    distinct = distinct.map(lambda x: (x[0], 1)).reduceByKey(lambda x, y: x+y)
    result = distinct.map(lambda x: x[1]).histogram(range(1, hist))

    return result

# Print the final result in required format
def print_result(result, filename):
    print_result = ['cities,yelp users']
    for i in range(len(result[1])):
        outstr = str(result[0][i]) + ',' + str(result[1][i])
        print_result.append(outstr)

    print_result = sc.parallelize(print_result)
    print_result.saveAsTextFile(filename)

city_data = city_file.map(lambda line: json.loads(line)).flatMap(lambda x: cat_city(x))
review_data = review_file.map(lambda line: json.loads(line)).flatMap(lambda x: cat_review(x))

cities = city_data.map(lambda x: (x[1], x[0]))

# Overall pattern
users = review_data.map(lambda x: (x[1], x[0]))

result = counting_users(users, cities, 32)
print_result(result, 'si618w17hw5-part2_haoyoliu')

# Good review
good_review = review_data.filter(lambda x: x[2] > 3).map(lambda x: (x[1], x[0]))

result = counting_users(good_review, cities, 26)
print_result(result, 'si618w17hw5-part2_haoyoliu_goodreview')

# Bad review
bad_review = review_data.filter(lambda x: x[2] < 3).map(lambda x: (x[1], x[0]))

result = counting_users(bad_review, cities, 17)
print_result(result, 'si618w17hw5-part2_haoyoliu_badreview')
