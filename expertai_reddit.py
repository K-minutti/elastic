from config import config
import psycopg2
import psycopg2.extras
from expert import expert_ai_analysis


def expertai_reddit():
    connection = None
    try:
        params= config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


        cursor.execute("SELECT * from reddit")
        subs = cursor.fetchall()

        reddit_posts = {}
        for sub in subs:
            reddit_posts[sub['id']] = sub['content']



        #SQL to execute for each reddit post
        insert_expert_analysis = "INSERT INTO expert_ai_reddit(source_id, entities, main_phrases, main_lemmas, topics, sentiment) VALUES(%s, %s::text[], %s::text[], %s::text[], %s::text[], %s)"
                
        for post_id in reddit_posts:
            text = reddit_posts[post_id]
            values = expert_ai_analysis(text)
            print("post_id", post_id)
            print("expert ai values", values)
            if values != None:
                cursor.execute(insert_expert_analysis, (post_id,values['entities'], values['main_phrases'], values['main_lemmas'], values['topics'], values['sentiment']))
            
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
    expertai_reddit()
