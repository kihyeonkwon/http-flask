from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database  = database

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user_id = app.database.execute(text("""
        INSERT INTO users (
        name,
        email,
        profile,
        hashed_password
        ) VALUES (
        :name,
        :email, 
        :profile,
        :password
        )
        """), new_user).lastrowid

        row = current_app.database.execute(text("""
        SELECT
        id,
        name,
        email,
        profile
        FROM users
        WHERE id = :user_id
        """), {
            'user_id':new_user_id
            }).fetchone()


        created_user = {
                'id' : row['id'],
                'name':row['name'],
                'email':row['email'],
                'profile':row['profile']
                }if row else None

        return jsonify(created_user)

    @app.route('/tweet', methods=['POST'])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet['tweet']

        if len(tweet) > 300:
            return '300자를 초과했습니다', 400

        new_tweet_id = app.database.execute(text("""
        INSERT INTO tweets (
        user_id,
        tweet
        ) VALUES (
        :id,
        :tweet
        )
        """), user_tweet).lastrowid

        row = current_app.database.execute(text("""
        SELECT
        id,
        user_id,
        tweet,
        created_at
        FROM tweets WHERE id = :new_tweet_id
        """), {"new_tweet_id":new_tweet_id}).fetchone()

        created_tweet = {
                'id':row['id'],
                'user_id':row['user_id'],
                'tweet':row['tweet'],
                'created_at':row['created_at']
                } if row else None


        return jsonify(created_tweet)

    @app.route("/follow", methods=["POST"])
    def follow():
        payload = request.json
        
        app.database.execute(text("""
        INSERT INTO users_follow_list(
        user_id,
        follow_user_id
        ) VALUES(
        :id,
        :follow_user_id
        )"""), payload)


        user_id = payload["id"]
        
        rows = current_app.database.execute(text("""
        SELECT
        follow_user_id
        FROM users_follow_list WHERE user_id = :user_id
        """), {"user_id":user_id}).fetchall()

        follows = [row["follow_user_id"] for row in rows]

        return jsonify({'user_id':user_id, 'follows':follows})


    @app.route("/unfollow", methods=["POST"])
    def unfollow():
        payload = request.json

        app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow_user_id
        """), payload)



        user_id = payload["id"]
        
        rows = current_app.database.execute(text("""
        SELECT
        follow_user_id
        FROM users_follow_list WHERE user_id = :user_id
        """), {"user_id":user_id}).fetchall()

        follows = [row["follow_user_id"] for row in rows]

        return jsonify({'user_id':user_id, 'follows':follows})


    return app
