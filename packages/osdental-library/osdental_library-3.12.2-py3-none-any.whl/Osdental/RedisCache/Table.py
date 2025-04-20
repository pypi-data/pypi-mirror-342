import os
from uuid import UUID
from Osdental.Database.Connection import Connection
from dotenv import load_dotenv
load_dotenv()

class RedisTable:

    def __init__(self):
        self.db = Connection(os.getenv('DATABASE_SECURITY'))

    
    async def create_redis_key(self, user_id:UUID, method_controller:str, key:str) -> None:
        query = """ 
        EXEC SECURITY.spi_InsertRedisTable
        @i_idUser = :user_id,
        @i_microService = :microservice,
        @i_methodController = :method_controller,
        @i_keyName = :key_name
        """
        params = {
            'user_id': user_id,
            'microservice': os.getenv('MICROSERVICE_NAME'),
            'method_controller': method_controller,
            'key_name': key
        }
        await self.db.execute_query(query, params)

    
    async def delete_redis_key(self, key:str) -> None:
        query = """ 
        EXEC SECURITY.spd_DeleteRedisTable
        @i_keyName = :key_name
        """
        params = {
            'key_name': key
        }
        await self.db.execute_query(query, params)