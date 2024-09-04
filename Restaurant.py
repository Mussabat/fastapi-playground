"""1. The system should allow employees to be added to the restaurant with their names and job types.
 
2. The system should allow the deactivation of employees, making them inactive in the system.
 
3.The system should allow branches to be added to the restaurant with their location details.
 
4. The system should allow menus to be created and added to the restaurant with their sections and items.
 
5. The system should allow orders to be created and added to tables with details about the items and quantities ordered.
 
6. The system should allow tables to be added to branches with their capacities and order history.
 
7. The system should allow the deactivation of branches, making them inactive in the system.
 
The system should allow the deactivation of tables, making them unavailable for orders."""

from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
from fastapi.responses import Response


class employeeSchema(BaseModel):
    employee_id: int
    employee_name: str
    employee_mail: str
    job_type: str
    is_employee_active: bool


class employeeDto(BaseModel):
    employee_id: int | None
    employee_name: str
    employee_mail: str
    job_type: str
    work_status: str


class resturantSchema(BaseModel):
    branch_id: int
    branch_location: str
    is_branch_active: bool
    capacity: int


class resturantDto(BaseModel):
    branch_id: int
    branch_location: str
    branch_mode: str
    capacity: int


class menuSchema(BaseModel):
    id: int
    item_name: str
    item_group: str
    item_price: float


class menuDto(BaseModel):
    id: int
    item_name: str
    item_group: str
    item_price: float
    item_price_display: str


class userSchema(BaseModel):
    user_id: int
    user_name: str
    user_email: str


class userDto(BaseModel):
    user_id: int
    user_name: str
    user_email: str


class tableSchema(BaseModel):
    table_id: int
    branch_id: int
    is_table_active: bool


class tableDto(BaseModel):
    table_id: int
    branch_id: int
    table_mode: str


class orderSchema(BaseModel):
    oder_id: int
    table_id: int
    order_time: datetime
    order_status: str
    total_price: float


class OrderItemSchema(BaseModel):
    order_id: int
    item_name: str
    quantity: int
    price: float


class OrderItemDto(BaseModel):
    order_id: int
    item_name: str
    quantity: int
    price: float
    price_display: str


class orderDto(BaseModel):
    oder_id: int
    table_id: int
    order_time: datetime
    order_status: str
    items: list[OrderItemDto]
    total_price: float
    total_price_display: str


app = FastAPI()


employee_repo: list[employeeSchema] = [
    employeeSchema(
        employee_id=1,
        employee_mail="naf@gmail.com",
        employee_name="nafisa",
        job_type="swe",
        is_employee_active=True,
    ),
    employeeSchema(
        employee_id=2,
        employee_mail="raf@gmail.com",
        employee_name="rafisa",
        job_type="sre",
        is_employee_active=True,
    ),
]
resturant_repo: list[resturantSchema] = []
menu_repo: list[menuSchema] = []
user_repo: list[userSchema] = []
table_repo: list[tableSchema] = []
order_repo: list[orderSchema] = []
order_item_repo: list[OrderItemSchema] = []

max_employee_id = 2
max_order_id = 0


@app.post("/employee")
def add_employee(employee_data: employeeDto):

    global max_employee_id
    max_employee_id += 1

    employee_repo.append(
        employeeSchema(
            employee_id=max_employee_id,
            employee_name=employee_data.employee_name,
            employee_mail=employee_data.employee_mail,
            job_type=employee_data.job_type,
            is_employee_active=employee_data.work_status == "active",
        )
    )

    return Response(status_code=201)


@app.post("/order/{user_id}")
def create_order(order_data: orderDto):
    global max_order_id
    max_order_id += 1

    order_repo.append(
        orderSchema(
            oder_id=max_order_id,
            table_id=order_data.table_id,
            order_time=order_data.order_time,
            order_status=order_data.order_status,
            total_price=order_data.total_price,
        )
    )

    for item in order_data.items:
        order_item_repo.append(
            OrderItemSchema(
                order_id=max_order_id,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.price,
            )
        )

    return Response(status_code=201)


@app.patch("/employee/{employee_id}")
def toggle_employee_status(
    employee_id: int,
):
    for employee in employee_repo:
        if employee.employee_id != employee_id:
            continue

        employee.is_employee_active = not employee.is_employee_active
        return Response(status_code=200)

    return Response(status_code=404)


@app.get("/employee/{employee_id}")
def employee_info(employee_id: int):
    for employee in employee_repo:
        if employee.employee_id != employee_id:
            continue

        return employeeDto(
            employee_id=employee.employee_id,  # DTO | Schema
            employee_name=employee.employee_name,
            employee_mail=employee.employee_mail,
            job_type=employee.job_type,
            work_status="active" if employee.is_employee_active else "inactive",
        )

    return Response(status_code=404)


@app.get("/order/{order_id}")
def order_info(order_id: int):
    for order in order_repo:
        if order.order_id != order_id:
            continue

        order_items = []

        for order_item in order_item_repo:
            if order_item.order_id != order_id:
                continue

            order_items.append(order_item)

        return orderDto(
            oder_id=order.order_id,
            table_id=order.table_id,
            order_time=order.order_time,
            order_status=order.order_status,
            order_item=order_items,
            total_price=order.total_price,
            total_price_display="{0:.2f}".format(order.total_price),
        )
