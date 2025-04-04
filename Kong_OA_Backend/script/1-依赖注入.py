from fastapi import FastAPI, Depends, Query

app = FastAPI()
## 无参数依赖
def get_current_user():
    return {'code':100,'username':'zsy'}

@app.get("/get_user/")
async def get_user(current:dict = Depends(get_current_user)):
    return current
# ---
## 有参数依赖
def get_user_age(age:int):
    return {'code':100,'age':age}
@app.get("/get_user_age/")
async def get_user(current:dict = Depends(lambda : get_user_age(age=18))):
    return current
## 带传入参数依赖
def get_user_with_age(age: int = Query(...)):
    return {'code':100,'age':age}
@app.get("/get_user_ages/")
async def get_user_params(current: dict = Depends(get_user_with_age)):
    return current

def get_db():
    return "db_connections"
## 多层依赖
def get_user(db = Depends(get_db)):
    return {'code':100,'db':db}
@app.get("/get_user_db/")
async def get_user_db(current:dict = Depends(get_user)):
    return current
## 类注入依赖

class DemoClass:
    def __init__(self,q:str = None):
        self.q = q

@app.get("/demo/")
async def demo(com:DemoClass = Depends()):
    return {'code':100,'q':com.q}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)