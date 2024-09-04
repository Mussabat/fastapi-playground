# Users can create posts. Posts can contain texts of at most 63,206 characters.
#
# Users can send friend request to other users.
#
# Users can accept or reject friend requests from other users.
#
# Users become friends when a friend request is accepted
#
# Users can see posts from all their friends. Posts should be ordered by descending order of creation
# time, i.e more recent posts should appear first.
#
# Users can search their posts with keywords. A search with "hello world" should show all posts
# containing either "hello" or "world". No need to do a ranking for results matching the search query,
# but order them by descending order of creation time as before.

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


class PostSchema(BaseModel):
    post_id: int
    post_text: str
    user_id: int
    creation_time: datetime


class PostDto(BaseModel):
    post_id: int | None = None
    post_text: str
    user_id: int | None = None
    creation_time: datetime


class FriendSchema(BaseModel):
    friend_id: int
    user_id: int
    is_friend: bool


class FriendDto(BaseModel):
    friend_id: list[UserDto]
    user_id: int
    is_friend: bool


class FriendPostDto(BaseModel):
    friend_post: list[PostDto]
    friend_id: int
    user_id: int


class FriendRequestSchema(BaseModel):
    from_user_id: int
    to_user_id: int
    request_date: datetime


class FriendRequestDto(BaseModel):
    from_user_id: int
    to_user_id: int
    request_date: datetime


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

post_repo: list[PostSchema] = [
    PostSchema(
        user_id=1,
        post_id=1,
        post_text="Hey everyone All good?",
        creation_time=datetime.now(),
    ),
    PostSchema(
        user_id=2,
        post_id=2,
        post_text="Not feeling good",
        creation_time=datetime.now(),
    ),
]

friends_repo: list[FriendSchema] = [
    FriendSchema(
        is_friend=True,
        user_id=2,
        friend_id=1,
    )
]

friend_request_repo: list[FriendRequestSchema] = []

max_user_id = len(user_repo)
max_post_id = len(post_repo)

app = FastAPI()


def convert_post_schema_to_post_dto(post_data: PostSchema):
    return PostDto(
        user_id=post_data.user_id,
        post_id=post_data.post_id,
        post_text=post_data.post_text,
        creation_time=post_data.creation_time,
    )


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


@app.post("/post")
def create_post(post_data: PostDto):
    if len(post_data.post_text) > 63206:
        return Response("sorry text is too long", status_code=403)

    global max_post_id
    max_post_id += 1

    post_repo.append(
        PostSchema(
            post_id=max_post_id,
            creation_time=datetime.now(),
            post_text=post_data.post_text,
            user_id=post_data.user_id or 0,
        )
    )

    return Response(status_code=201)


@app.get("/searchPost")
def search_post(search_query: str):
    result: list[PostDto] = []

    search_words = search_query.split(" ")
    for search in post_repo:
        for word in search_words:
            if search.post_text.find(word) != -1:
                result.append(convert_post_schema_to_post_dto(search))
                break

    result = sorted(result, key=lambda x: x.creation_time, reverse=True)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)


@app.post("/user/{userId}/friendRequest/{friendId}")
def sent_friend_request(friend_id: int, user_id: int):
    for row_friend in friends_repo:
        if row_friend.user_id == user_id and row_friend.friend_id == friend_id:
            return Response("You are already friend!", status_code=403)

    for friend_request in friend_request_repo:
        if (
            friend_request.from_user_id == user_id
            and friend_request.to_user_id == friend_id
        ):
            return Response("Friend request already sent", status_code=403)
        if (
            friend_request.from_user_id == friend_id
            and friend_request.to_user_id == user_id
        ):
            return Response(
                "You have already received a friend request", status_code=403
            )

    friend_request_repo.append(
        FriendRequestSchema(
            from_user_id=user_id,
            to_user_id=friend_id,
            request_date=datetime.now(),
        )
    )
    return Response(status_code=201)


@app.get("/user/{userId}/friendRequest")
def get_friend_requests(user_id: int):
    result: list[FriendRequestDto] = []
    for friend_request in friend_request_repo:
        if friend_request.to_user_id == user_id:
            result.append(
                FriendRequestDto(
                    from_user_id=friend_request.from_user_id,
                    to_user_id=friend_request.to_user_id,
                    request_date=friend_request.request_date,
                )
            )

    result = sorted(result, key=lambda x: x.request_date, reverse=True)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)


@app.post("/user/{userId}/friendRequest/{request_user_id}/accept")
def accept_friend_request(user_id: int, request_user_id: int):
    for friend_request in friend_request_repo:
        if (
            friend_request.from_user_id == request_user_id
            and friend_request.to_user_id == user_id
        ):
            friends_repo.append(
                FriendSchema(
                    friend_id=request_user_id,
                    user_id=user_id,
                    is_friend=True,
                )
            )

            friend_request_repo.remove(friend_request)
            return Response(status_code=201)

    return Response(status_code=404)


@app.delete("/user/{userId}/friendRequest/{request_user_id}/reject")
def reject_friend_request(user_id: int, request_user_id: int):
    for friend_request in friend_request_repo:
        if (
            friend_request.from_user_id == request_user_id
            and friend_request.to_user_id == user_id
        ):
            friend_request_repo.remove(friend_request)
            return Response(status_code=204)

    return Response(status_code=404)


@app.get("/user/{userId}/friend/{friendId}/post")
def see_friends_post(user_id: int, friend_id: int):
    result: list[PostDto] = []
    for row_friend in friends_repo:
        if row_friend.user_id == user_id and row_friend.friend_id == friend_id:

            for row_friend in post_repo:
                if row_friend.user_id == friend_id:
                    result.append(convert_post_schema_to_post_dto(row_friend))

    result = sorted(result, key=lambda x: x.creation_time, reverse=True)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)


@app.get("/user/{userId}/friend/posts")
def get_all_friends_post(user_id: int):
    result: list[PostDto] = []
    for row_friend in friends_repo:
        if row_friend.user_id == user_id:
            for row_post in post_repo:
                if row_post.user_id == row_friend.friend_id:
                    result.append(convert_post_schema_to_post_dto(row_post))

    result = sorted(result, key=lambda x: x.creation_time, reverse=True)

    if len(result) > 0:
        return result
    else:
        return Response(status_code=404)
