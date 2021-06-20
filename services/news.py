from pygooglenews import GoogleNews
from newspaper import Article
gn = GoogleNews()
search = gn.search('TLSA', from_='2021-06-15', to_='2021-06-19')
for entry in search['entries'][:2]:

    url = entry['link']
    article = Article(url)
    article.download()
    article.parse()
    print('====================================================')
    print(entry['title'])
    print('====================================================')
    print(article.text)
    print('----------------------------------------------------')
    print(entry['source']['title'])
    print('----------------------------------------------------')



"""
for every stock in stock the db get the last three months worth of news and 
added it to the news table


for every unique news date in the the set of news for the past three months 
create sets of date ranges
where a news date is the midpoint of a start and end date range

these date ranges will create our sentiment nodes

then in the reddit db section we will pull all of the posts on a specific stock 
and pass them through the sentiment analysis and we will update there entries in the db with there sentiment score
next we will group the posts in these date ranges created above and we will create sentiments nodes for the time period
"""