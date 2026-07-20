import random
from datetime import datetime
from uuid import uuid4

def generate_unique_user_data(prefix:str="user")->dict:
    timestamp=int(datetime.now().timestamp())
    random_suffix=random.randint(1000,9999)
    return {
        "id":str(uuid4()),
        "user_name":f"{prefix}_user_{timestamp}_{random_suffix}",
        "first_name":f"First{random_suffix}",
        "last_name":f"Last{random_suffix}",
        "email":f"{prefix}_{timestamp}_{random_suffix}@example.com",
        "is_superuser":False,
        "is_active":True,
        "is_superUser":False
    }

def generate_super_user_data(prefix:str="admin"):
    super_user=generate_unique_user_data(prefix=prefix)
    super_user["is_superUser"]=True
    return super_user

def generate_bulk_users(count:int,prefix:str="bulk")->list[dict]:
    return [generate_super_user_data(f"{prefix}_{i}") for i in range(count)]

def generate_test_user_update_data()->dict:
    timestamp=int(datetime.now().timestamp())
    return {
        "first_name":f"UpdatedFirst{timestamp}",
        "last_name":f"UpdatedLast{timestamp}",
        "user_name":f"updated_user_{timestamp}"
    }
