# MongoDB attributes
from fastapi import FastAPI
mongodb_uri = 'mongodb+srv://Tae:Potae8211@apiplatform.qexwo.mongodb.net/ApiList?retryWrites=true&w=majority'

app = FastAPI()
app.listen(process.env.PORT || 8000)