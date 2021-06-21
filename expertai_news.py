from config import config
import psycopg2
import psycopg2.extras
from expert import expert_ai_analysis


def expertai_news():
    connection = None
    try:
        params= config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


        cursor.execute("SELECT * from news")
        news = cursor.fetchall()

        news_articles = {}
        for article in news:
            news_articles[article['id']] = article['content']
   
        #SQL to execute for each news article
        insert_expert_analysis = "INSERT INTO expert_ai_news(source_id, entities, main_phrases, main_lemmas, topics, sentiment) VALUES(%s, %s::text[], %s::text[], %s::text[], %s::text[], %s)"
                
        for article_id in news_articles:
            text = news_articles[article_id]
            values = expert_ai_analysis(text)
            if values != None:
                cursor.execute(insert_expert_analysis, (article_id, values['entities'], values['main_phrases'], values['main_lemmas'], values['topics'], values['sentiment']))
            
        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.rollback()
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    expertai_news()
