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


class HotelSchema(BaseModel):
    hotel_id: int
    hotel_name: str
    hotel_location: str
    hotel_description: str
    cost: float
    avg_rating: float


class HotelDto(BaseModel):
    hotel_id: int
    hotel_name: str
    hotel_location: str
    hotel_description: str
    cost: float
    cost_display: str | None
    avg_rating: float | None


class ReviewSchema(BaseModel):
    review_id: int
    review_text: str
    user_id: int
    user_name: str
    hotel_id: int
    rating: int


class ReviewDto(BaseModel):
    review_id: int | None = None
    review_text: str
    user_id: int
    user_name: str
    hotel_id: int
    avg_rating: float
    avg_rating_display: str | None


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

hotel_repo: list[HotelSchema] = [
    HotelSchema(
        hotel_id=1,
        hotel_name="Sea Pearl Hotel",
        hotel_description="Surrounded by sea Nice view",
        hotel_location="Cox's Bazar",
        cost=10000,
        avg_rating=4.1,
    ),
    HotelSchema(
        hotel_id=2,
        hotel_name="Barbiedella Hotel",
        hotel_description="Surrounded by hills, Nice view, pool available",
        hotel_location="Shylet",
        cost=20000,
        avg_rating=3.8,
    ),
]


review_repo: list[ReviewSchema] = [
    ReviewSchema(
        user_name="nafisa",
        rating=4,
        hotel_id=1,
        review_text="Nice!",
        review_id=1,
        user_id=1,
    )
]

max_user_id = len(user_repo)
max_hotel_id = len(hotel_repo)
max_review_id = len(review_repo)


def hotel_schema_to_hotel_dto(hotel: HotelSchema):
    rating_sum = 0
    rating_count = 0
    for review in review_repo:
        if review.hotel_id == hotel.hotel_id:
            rating_sum += review.rating
            rating_count += 1

    avgrating = None
    if rating_count != 0:
        avgrating = rating_sum / rating_count

    return HotelDto(
        hotel_id=hotel.hotel_id,
        hotel_name=hotel.hotel_name,
        hotel_description=hotel.hotel_description,
        hotel_location=hotel.hotel_location,
        cost=hotel.cost,
        cost_display="{0:.2f}".format(hotel.cost),
        avg_rating=avgrating,
    )


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


@app.get("/hotels")
def show_all_hotels():
    result: list[HotelDto] = []

    for hotel in hotel_repo:
        result.append(hotel_schema_to_hotel_dto(hotel))

    return result


@app.get("/hotel")
def search_hotel(search_query: str):
    result: list[HotelDto] = []
    for hotel in hotel_repo:
        if (
            hotel.hotel_name.find(search_query) != -1
            or hotel.hotel_description.find(search_query) != -1
        ):
            result.append(hotel_schema_to_hotel_dto(hotel))

    if (len(result)) > 0:
        return result
    else:
        return Response(status_code=404)


@app.post("/review")
def leave_review(review_data: ReviewDto):
    global max_review_id
    max_review_id += 1

    review_repo.append(
        ReviewSchema(
            hotel_id=review_data.hotel_id,
            review_id=max_review_id,
            user_id=review_data.user_id,
            review_text=review_data.review_text,
            user_name=review_data.user_name,
            rating=review_data.rating,
        )
    )

    return Response(status_code=201)


@app.get("/review/{hotelId}")
def get_hotel_review(hotel_id: int):
    result: list[ReviewDto] = []
    for review in review_repo:
        if review.hotel_id == hotel_id:
            result.append(review.review_text)

    if (len(result)) > 0:
        return result
    else:
        return Response(status_code=404)
