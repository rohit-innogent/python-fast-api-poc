from queue import Queue

from pydantic import BaseModel, ValidationError, field_serializer
from datetime import datetime, timezone
from collections import deque


# Example of a list
numbers = [1, 2, 3, 4, 5]

# Adding an element
numbers.append(6)

# Removing an element
numbers.remove(3)

# Accessing elements
print(numbers[2])  # Output: 4

# Iterating over the list
for number in numbers:
    print(number)


# Example of a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print(person["name"])
# Adding a new key-value pair
person["occupation"] = "Engineer"

# Iterating over the dictionary
for key, value in person.items():
    print(f"{key}: {value}")

# Example of a set
fruits = {"apple", "banana", "cherry"}

# Adding an element
fruits.add("orange")

# Removing an element
fruits.remove("banana")

# Checking for fruite
print("apple" in fruits)

# Iterating over the set
for fruit in fruits:
    print(fruit)


q = Queue()

# Adding elements to the queue
q.put("a")
q.put("b")
q.put("c")

print("queue: ", q.get())  # Output: 'a'
print("queue: ", q.get())

# Example of a dequeue
queue = deque(["a", "b", "c"])

# Adding elements to the queue
queue.append("d")
queue.append("e")

# Removing elements from the queue
print("it is deque - ", queue.popleft())  # Output: a

# Checking the queue
print(queue)  # Output should be: deque(['b', 'c', 'd', 'e'])


# Example of a stack
stack = [1, 2, 3, 4]

# Pushing an element onto the stack
stack.append(5)

# Popping an element from the stack
print(stack.pop())  # Output: 5

# Checking the stack
print(stack)  # Output: [1, 2, 3, 4]



# Example of a tuple

coordinates = (10, 20)

# Accessing elements
print(coordinates[0])  # Output: 10

# Tuples are immutable, so you cannot change elements or add new elements




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
