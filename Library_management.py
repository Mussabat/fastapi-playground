"""
Functional Requirements for a Library Management System
The following are the functional requirements for a Library Management System:

Ability to add and remove books from the library *
Ability to search for books in the library by title, author, or ISBN *
Ability to check out and return books*
Ability to display a list of all books in the library *
Ability to store and retrieve information about library patrons, including their name and ID number*
Ability to track which books are currently checked out and when they are due to be returned
Ability to generate reports on library usage and checkouts

"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from datetime import datetime


class BookSchema(BaseModel):
    book_id: int
    book_title: str
    book_author_name: str
    book_isbn: str
    book_available: bool


class BookDto(BaseModel):
    book_id: int | None
    book_title: str
    book_author_name: str
    book_isbn: str
    book_available: bool


class PetronSchema(BaseModel):
    petrons_id: int
    petrons_name: str
    petrons_mail: str


class PetronDto(BaseModel):
    petrons_id: int | None
    petrons_name: str
    petrons_mail: str


class ParchaseSchema(BaseModel):
    parchase_id: int
    petrons_id: int
    book_id: int


class ParchaseDto(BaseModel):
    parchase_id: int
    petrons_id: int
    book_id: int


app = FastAPI()

book_repo: list[BookSchema] = [
    BookSchema(
        book_id=1,
        book_author_name="Martin",
        book_isbn="123456",
        book_title="Clean Code",
        book_available=True,
    ),
    BookSchema(
        book_id=2,
        book_author_name="Robert Luis",
        book_isbn="345678",
        book_title="Treasure Island",
        book_available=True,
    ),
]
petrons_repo: list[PetronSchema] = [
    PetronSchema(
        petrons_id=1,
        petrons_mail="nafisa@gmail.com",
        petrons_name="Nafisa Tabassum",
    ),
    PetronSchema(
        petrons_id=2,
        petrons_mail="tanha@gmail.com",
        petrons_name="Tanha Mahajabin",
    ),
]
parchase_repo: list[ParchaseSchema] = []

max_book_id = 2
max_petron_id = 2
max_parchase_id = 0


def book_schema_to_dto(book: BookSchema):
    return BookDto(
        book_id=book.book_id if book.book_id else None,
        book_title=book.book_title,
        book_author_name=book.book_author_name,
        book_isbn=book.book_isbn,
        book_available=book.book_available,
    )


@app.post("/books")
def add_books(book_data: BookDto):
    global max_book_id
    max_book_id += 1

    book_repo.append(
        BookSchema(
            book_id=max_book_id,
            book_author_name=book_data.book_author_name,
            book_isbn=book_data.book_isbn,
            book_title=book_data.book_title,
            book_available=book_data.book_available,
        )
    )

    return Response(status_code=201)


@app.delete("/books/{book_id}")
def remove_book(book_id: int):
    for book in book_repo:
        if book.book_id != book_id:
            continue

        book_repo.remove(book)
        return Response(status_code=204)

    return Response(status_code=404)


@app.get("/books/{book_id}")
def get_single_book(book_id: int):

    for book in book_repo:
        if book.book_id != book_id:
            continue

        return book_schema_to_dto(book)

    return Response(status_code=404)


@app.get("/books")
def show_all_books():
    result: list[BookDto] = []

    for book in book_repo:
        result.append(book_schema_to_dto(book))

    return result


@app.get("/books/search")
def search_books(search_query: str | None = None):
    result: list[BookDto] = []

    for book in book_repo:
        if search_query == None:
            result.append(book_schema_to_dto(book))

            continue

        if (
            book.book_author_name.find(search_query) != -1
            or book.book_title.find(search_query) != -1
            or book.book_isbn.find(search_query) != -1
        ):
            result.append(book_schema_to_dto(book))

    return result


@app.post("/parchase/{petrons_id}")
def check_out(parchase_data: ParchaseDto):
    global max_parchase_id
    for user in petrons_repo:
        if user.petrons_id != parchase_data.petrons_id:
            continue

        for book in book_repo:
            if book.book_id != parchase_data.book_id and book.book_available == False:
                continue

            max_parchase_id += 1
            book.book_available = False
            parchase_repo.append(
                ParchaseSchema(
                    book_id=parchase_data.book_id,
                    petrons_id=parchase_data.petrons_id,
                    parchase_id=max_parchase_id,
                )
            )

            return Response(status_code=201)

    return Response(status_code=404)


@app.delete("/parchase/{parchase_id}")
def check_out(parchase_id: int):
    for parchase in parchase_repo:
        if parchase.parchase_id != parchase_id:
            continue

        parchase_repo.remove(parchase)
        return Response(status_code=204)
    return Response(status_code=404)


@app.post("/petrons")
def add_petrons(petrons_data: PetronDto):
    global max_petron_id
    max_petron_id += 1

    petrons_repo.append(
        PetronSchema(
            petrons_id=max_petron_id,
            petrons_mail=petrons_data.petrons_mail,
            petrons_name=petrons_data.petrons_mail,
        )
    )

    return Response(status_code=201)


@app.get("/petrons/{petrons_id}")
def show_petron(petrons_id: int):
    for petron in petrons_repo:
        if petron.petrons_id != petrons_id:
            continue

        return PetronDto(
            petrons_id=petron.petrons_id,
            petrons_name=petron.petrons_name,
            petrons_mail=petron.petrons_mail,
        )

    return Response(status_code=404)
