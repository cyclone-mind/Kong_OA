from src import create_app
from src.settings import setting
import uvicorn
app = create_app()

if __name__ == '__main__':
    uvicorn.run(app,host = setting.APP_HOST,port = setting.APP_PORT)
