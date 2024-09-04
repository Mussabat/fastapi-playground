"""
1. Search for flights*, 
2. Reserve seats,
3. Cancel Reservations and View Reservations. 
4. View Flight Information, *
5. Modify Flight Status, 
6. Add/Update Flight Details, 
7. Create/View Staff Account.

"""

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


class FlightSchema(BaseModel):
    flight_id: int
    departure_city: str
    arrival_city: str
    is_seat_available: bool


class FlightDto(BaseModel):
    flight_id: int | None = None
    departure_city: str
    arrival_city: str
    is_seat_available: bool


class ReserveSeatSchema(BaseModel):
    seat_id: int
    flight_id: int
    seat_researvation: bool


class ReserveSeatDto(BaseModel):
    seat_id: int | None = None
    flight_id: int
    seat_researvation: bool


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

flight_repo: list[FlightSchema] = [
    FlightSchema(
        flight_id=1,
        arrival_city="Dhaka",
        departure_city="Khulna",
        is_seat_available=True,
    ),
    FlightSchema(
        flight_id=2,
        arrival_city="Dhaka",
        departure_city="Malaysia",
        is_seat_available=True,
    ),
]

reserve_repo: list[ReserveSeatSchema] = []

max_user_id = len(user_repo)
max_flight_id = len(flight_repo)
max_reverse_id = len(reserve_repo)

app = FastAPI()


def convert_flight_schema_to_fligt_dto(flight: FlightSchema):
    return FlightDto(
        flight_id=flight.flight_id,
        arrival_city=flight.arrival_city,
        departure_city=flight.departure_city,
        is_seat_available=flight.is_seat_available,
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


@app.get("/viewFlights")
def view_flights():
    result: list[FlightDto] = []
    for flight in flight_repo:
        result.append(convert_flight_schema_to_fligt_dto(flight))

    if len(result) > 0:
        return result

    else:
        return Response(status_code=404)


@app.get("/searchFlight")
def search_flight(search_query: str):
    result: list[FlightDto] = []
    for flight in flight_repo:
        if flight.departure_city.find(search_query) != -1:
            result.append(convert_flight_schema_to_fligt_dto(flight))

    if len(result) > 0:
        return result

    else:
        return Response(status_code=404)


@app.get("/viewFlights/{flight_id}")
def view_flights(flight_id: int):
    result: list[FlightDto] = []
    for flight in flight_repo:
        if flight.flight_id == flight_id:
            result.append(convert_flight_schema_to_fligt_dto(flight))

    if len(result) > 0:
        return result

    else:
        return Response(status_code=404)
