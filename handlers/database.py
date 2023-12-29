import datetime
import os
import motor.motor_asyncio
DATABASE_URL = os.getenv('DATABASE_URL', None)
BOT_USERNAME = "Line-Translator-Bot"

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.userCol = self.db.users
        self.groupCol = self.db.groups

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            languages = ['en','ja'],
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )
    
    def new_group(self, id):# group 
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            languages = ['en','ja'],
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.userCol.insert_one(user)

    async def add_group(self, id): # group 
        group = self.new_group(id)
        await self.groupCol.insert_one(group)

    async def is_user_exist(self, id):
        user = await self.userCol.find_one({'id': id})
        return user if user else False

    async def is_group_exist(self, id):# group 
        group = await self.groupCol.find_one({'id': id})
        return group if group else False
    
    async def user_langs_update(self, id, langs):# user
        await self.userCol.update_one({'id': id}, {'$set': {'languages': langs}}) 

    
    async def group_langs_update(self, id, langs):# group
        await self.groupCol.update_one({'id': id}, {'$set': {'languages': langs}}) 

    async def total_users_count(self):
        count = await self.userCol.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.userCol.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.userCol.delete_many({'id': user_id})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.userCol.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.userCol.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def ban_group(self, group_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.groupCol.update_one({'id': group_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.userCol.find_one({'id': id})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.userCol.find({'ban_status.is_banned': True})
        return banned_users


db = Database(DATABASE_URL, BOT_USERNAME)
