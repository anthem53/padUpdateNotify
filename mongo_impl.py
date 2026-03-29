import LJH_SDK.mongo_db as mongo
from datetime import datetime, timezone
import LJH_SDK.log as log

CONNECTION_NAME ="CONNECTION_NAME"
DATABASE_NAME = "monitoring"
COLLECTION_NAME = "logs"
APP_NAME = "PAD_NOTIFY"

target_collection = None

def set_mongo():
    global target_collection
    mongo.init_mongo()
    target_collection = mongo.get_collection_direct(CONNECTION_NAME,DATABASE_NAME,COLLECTION_NAME)


def create_sample_logs(app_name, message, data = None):
    log = {
        "app_name":app_name,
        "timestamp" : datetime.now(timezone.utc),
        "message"   : message,
        "detail" : data
    }
    return log

def create_log(app_name, message, data = None):
    log = {
        "app_name":app_name,
        "timestamp" : datetime.now(timezone.utc),
        "message"   : message,
        "detail" : data
    }
    return log

def insert_log(message, data= None):
    global target_collection
    log = create_log(APP_NAME,message,data)
    result_id = mongo.insert_one(target_collection, log)
    return result_id
    

if __name__ == '__main__':
    mongo.init_mongo()
    set_mongo()
    result_id = insert_log("테스트용")
    log.info(f"{result_id} : 완료")

