import json
import traceback
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
#from fastapi import APIRouter
#router = APIRouter()


class SimpleRequest(BaseModel):
    data:str

#@router.post("/request/field/test")
#async def field_test(data:SimpleRequest):return await default_request_handler(data,field_requests.test)



async def default_request_handler(data,func,parent=None):
    headers={"cache-control":"no-store"}
    try:
        try:d=json.loads(data.data)
        except:raise Exception("Request in invalid format.")
        result = await func(d,parent)
        # check if result instance of Result, else return ValueResult
        if not isinstance(result,Result):result = ValueResult(result)
        return JSONResponse(content=result.data, headers=headers)
    except Exception as e:
        return JSONResponse(content=ErrorResult(e).data, headers=headers)   
    
async def stream_request_handler(data,func,parent=None):
    headers={"cache-control":"no-store"}
    try:
        try:d=json.loads(data)
        except:raise Exception("Request in invalid format.")
        return await func(d,parent)
    except Exception as e:
        return JSONResponse(content=ErrorResult(e).data, headers=headers)   


    
class Result:
    def __init__(self):
        self.data = {}
        self.data["type"]="generic"
        self.data["success"]=True
    def to_json(self):return json.dumps(self.data)
class ValueResult(Result):
    def __init__(self,value):
        self.data = {}
        self.data["type"]="value"
        self.data["value"]=value
        self.data["success"]=True
class DictResult(Result):
    def __init__(self,obj:dict):
        self.data = {}
        self.data["type"]="dict"
        self.data["success"]=True
        self.data.update(obj)
class ObjectResult(Result):
    def __init__(self,obj):
        self.data = {}
        self.data["type"]="dict"
        self.data["success"]=True
        self.data["data"]=obj

class ErrorResult(Result):
    def __init__(self,message_or_ex):
        super().__init__()
        self.data["type"]="error"
        self.data["success"]=False

        if isinstance(message_or_ex,str): error_message = message_or_ex
        if isinstance(message_or_ex, Exception):
            error_message = str(message_or_ex)
            #self.data["traceback"]=traceback.format_exc()
            self.data["traceback_full"]=traceback.format_exception(type(message_or_ex), message_or_ex, message_or_ex.__traceback__)
            tb = message_or_ex.__traceback__
            traceback_info = traceback.extract_tb(tb)
             # Remove the upmost stack frames
            traceback_info = traceback_info[1:]

            # Format the modified traceback information
            self.data["traceback"] = traceback.format_list(traceback_info) + traceback.format_exception_only(type(message_or_ex), message_or_ex)
        self.data["error"]=error_message