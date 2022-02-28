from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    return {'Mensagem': 'MyFlix back-end API'}
