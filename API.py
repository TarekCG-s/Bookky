import requests as rq
api_key = 'pbv0u9wn9bHWm6v5NakhA'
res = rq.get('https://www.goodreads.com/book/review_counts.json', params={"key": api_key, "isbns":"0751532711"})
print(res.status_code)
data = res.json()
print(data)
