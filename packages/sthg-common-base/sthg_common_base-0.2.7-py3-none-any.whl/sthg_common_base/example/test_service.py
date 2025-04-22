from time import sleep

from sthg_common_base.response.exception import CustomException
from sthg_common_base.response.httpCodeEnum import ResponseEnum
from sthg_common_base.response.response import BaseResponse
from sthg_common_base.utils.log_wrapper import service_log

class Person:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def get_id(self):
        return self.ID

    def get_name(self):
        return self.name

    def set_id(self, new_id):
        self.ID = new_id

    def set_name(self, new_name):
        self.name = new_name

    def __str__(self):
        return f"Person(ID={self.ID}, name='{self.name}')"

@service_log(printReq=True,printResp=True)
def get_Object(id:str)->Person:
    per = Person("1","anne")
    return per

@service_log(printReq=True,printResp=True)
def get_baseRes(id:str)->BaseResponse:
    per = Person("2","anne2")
    result = BaseResponse(ResponseEnum.OK,per)

    return result


@service_log(printReq=True, printResp=True)
def get_Object_Exception(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    raise CustomException(ResponseEnum.InternalError,None)

    return result


@service_log(printReq=True, printResp=True,throwException=False)
def get_Object_Exception2(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    raise CustomException(ResponseEnum.InternalError,None)

    return result

@service_log(printReq=True, printResp=True)
def get_Object_MaxRt(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    result = BaseResponse(ResponseEnum.OK, per)
    sleep(1)
    return result




@service_log(printReq=True,printResp=True)
async def get_Object_ansyc(id:str)->Person:
    per = Person("1","anne")
    return per

@service_log(printReq=True,printResp=True)
async def get_baseRes_ansyc(id:str)->BaseResponse:
    per = Person("2","anne2")
    result = BaseResponse(ResponseEnum.OK,per)

    return result


@service_log(printReq=True, printResp=True)
async def get_Object_Exception_ansyc(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    raise CustomException(ResponseEnum.InternalError,None)

    return result


@service_log(printReq=True, printResp=True,throwException=False)
async def get_Object_Exception2_ansyc(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    raise CustomException(ResponseEnum.InternalError,None)

    return result

@service_log(printReq=True, printResp=True)
async def get_Object_MaxRt_ansyc(id: str) -> BaseResponse:
    per = Person("2", "anne2")

    result = BaseResponse(ResponseEnum.OK, per)
    sleep(1)
    return result
