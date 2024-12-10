import motor.motor_asyncio
from config import CDB_NAME, DB_URI

DATABASE_NAME = CDB_NAME
DATABASE_URI = DB_URI


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id=id,
            title=title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    async def add_user(self, id, name):
        try:
            user = self.new_user(id, name)
            await self.col.insert_one(user)
        except Exception as e:
            print(f"Error adding user: {e}")

    async def is_user_exist(self, id):
        try:
            user = await self.col.find_one({'id': id})
            return bool(user)
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False

    async def total_users_count(self):
        try:
            return await self.col.count_documents({})
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0

    async def get_all_users(self):
        try:
            return self.col.find({})
        except Exception as e:
            print(f"Error getting all users: {e}")
            return None

    async def delete_user(self, user_id):
        try:
            await self.col.delete_many({'id': user_id})
        except Exception as e:
            print(f"Error deleting user: {e}")

    async def get_start_text(self, bot_id):
        """Retrieve the start text for a specific bot."""
        try:
            bot = await self.db.bots.find_one({'bot_id': bot_id})
            return bot.get('start_text', None) if bot else None
        except Exception as e:
            print(f"Error getting start text: {e}")
            return None


# Initialize the database instance
db = Database(DATABASE_URI, DATABASE_NAME)
