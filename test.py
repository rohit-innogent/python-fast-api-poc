from pydantic import BaseModel, ValidationError, field_serializer
from datetime import datetime, timezone


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


p1 = Person(first_name="first", last_name="last", age="22")


# print("P1: ", p1)
# Excepstions
# try:
#     Person(first_name="first", last_name=100, age="sss")
# except ValidationError as ex:
#     print(ex.json())
#     print("exceptions: ", ex)

# validattions
# data = {
#     "first_name": "first",
#     "last_name": "last",
#     "age": 33
# }
# print(Person.model_validate(data))

# required vs optinal


# custom serialization

class Model(BaseModel):
    number: float

    @field_serializer("number")
    def serializer(self, value):
        return round(value, 2)


m = Model(number=1 / 3)

print(m.model_dump())

# dt = datetime.now(timezone.utc)

# print(dt.isoformat())
