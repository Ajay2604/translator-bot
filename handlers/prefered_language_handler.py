from handlers.database import db
from handlers.helpers import parse_langs

async def get_prefered_language(source):
    if(source["type"] == "user"):
        user = await db.is_user_exist(source["userId"])
        if not user:
            await db.add_user(source["userId"])
            return False
        return user["languages"]
    elif(source["type"] == "group"):
        group = await db.is_group_exist(source["groupId"])
        if not group:
            await db.add_group(source["groupId"])
            return False
        return group["languages"]
    

async def lang_update(source,msgArgs):
    langs = parse_langs(msgArgs)
    if(source["type"] == "user"):
        user = await db.is_user_exist(source["userId"])
        if user :
            await db.user_langs_update(source['user_id',langs])
            return True
    elif(source["type"] == "group"):
        group = await db.is_group_exist(source["groupId"])
        if group:
            await db.group_langs_update(source['groupId',langs])
            return True
    return False
    
        


# usage
# pytesting.py
