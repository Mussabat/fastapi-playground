from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from datetime import datetime


class UserSchema(BaseModel):
    user_id: int
    user_mail: str
    user_name: str


class UserDto(BaseModel):
    user_id: int | None = None
    user_mail: str
    user_name: str


class TweetSchema(BaseModel):
    tweet_id: int
    tweet_text: str
    creation_time: datetime
    user_id: int


class TweetDto(BaseModel):
    tweet_id: int | None = None
    tweet_text: str
    creation_time: datetime | None = None
    user_id: int


class FollowSchema(BaseModel):
    user_id: int
    follow_id: int
    tweet_id: int


class FollowDto(BaseModel):
    user_id: int
    follow_id: list[UserDto]


class FollowerTweetDto(BaseModel):
    user_id: int
    follow_id: int
    follow_tweet: list[TweetDto]


user_repo: list[UserSchema] = [
    UserSchema(
        user_id=1,
        user_mail="nafisa@gmail.com",
        user_name="nafisa",
    ),
    UserSchema(
        user_id=2,
        user_mail="suvha@gmail.com",
        user_name="Suvha",
    ),
]

tweet_repo: list[TweetSchema] = [
    TweetSchema(
        tweet_text="How are you all?",
        creation_time=datetime.now(),
        user_id=1,
        tweet_id=1,
    )
]

follower_repo: list[FollowSchema] = [FollowSchema(user_id=2, follow_id=1, tweet_id=1)]

max_user_id = len(user_repo)
max_tweet_id = len(tweet_repo)

app = FastAPI()


@app.post("/user")
def create_new_user(user_data: UserDto):
    global max_user_id
    max_user_id += 1
    user_repo.append(
        UserSchema(
            user_id=max_user_id,
            user_name=user_data.user_name,
            user_mail=user_data.user_mail,
        )
    )

    return Response(status_code=201)


@app.post("/tweet")
def create_tweet(tweet_data: TweetDto):
    if len(tweet_data.tweet_text) > 120:
        return Response(status_code=404)

    global max_tweet_id
    max_tweet_id += 1

    tweet_repo.append(
        TweetSchema(
            user_id=tweet_data.user_id,
            tweet_id=max_tweet_id,
            tweet_text=tweet_data.tweet_text,
            creation_time=datetime.now(),
        )
    )

    return Response(status_code=201)


@app.get("/tweet/{userId}")
def get_all_tweets(user_id: int):
    result: list[TweetDto] = []

    for user in tweet_repo:
        if user.user_id != user_id:
            continue

        result.append(
            TweetDto(
                tweet_id=user.tweet_id,
                tweet_text=user.tweet_text,
                creation_time=user.creation_time,
                user_id=user_id,
            )
        )

    result = sorted(result, key=lambda x: x.creation_time, reverse=True)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)


@app.post("/follow/{userId}/{followerId}")
def follow(user_id: int, follower_id: int):
    for ppl in follower_repo:
        if ppl.user_id == user_id and ppl.follow_id == follower_id:
            return Response("You are already following!", status_code=404)

    follower_repo.append(
        FollowSchema(follow_id=follower_id, user_id=user_id, tweet_id=0)
    )

    return Response(status_code=201)


@app.delete("/follow/{userId}/{followerId}")
def unfollow(user_id: int, follower_id: int):
    for ppl in follower_repo:
        if ppl.user_id == user_id and ppl.follow_id == follower_id:
            follower_repo.remove(
                FollowSchema(follow_id=follower_id, user_id=user_id, tweet_id=0)
            )
            return Response(status_code=201)

    return Response("You are not following!", status_code=404)


@app.get("/tweet/{userId}/{followerId}")
def show_tweets_of_follower(user_id: int, follower_id: int):
    result: list[str] = []
    for ppl in follower_repo:
        if ppl.user_id == user_id and ppl.follow_id == follower_id:

            for user in tweet_repo:
                if user.user_id == ppl.follow_id:
                    result.append(user.tweet_text)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)
    
