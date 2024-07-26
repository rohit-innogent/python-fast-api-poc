# from pydantic import BaseModel
#
#
# class AppBase(BaseModel):
#     app_name: str
#     app_desc: str
#     dev_name: str
#     status: str
#
#
# class AppCreate(AppBase):
#     pass
#
#
# class AppResponse(AppBase):
#     id: int
#
#     class Config:
#         from_attributes = True

from pydantic import BaseModel


class AppBase(BaseModel):
    app_name: str
    app_desc: str


class AppCreate(AppBase):
    pass


class AppResponse(AppBase):
    id: int

    class Config:
        from_attributes = True
