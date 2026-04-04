import pytest
from app.schemas import UserCreate

def test_can_create_user(service, db_fake):
    new_user = UserCreate(name = "Juan")
    #DB Length
    db_len_0 = len(db_fake)
    
    #Create the user with service
    res = service.create_user(new_user)
    #Asserts
    assert len(db_fake) == db_len_0 + 1
    assert res["id"] == 3
    assert res["name"] == "Juan"
    assert not res["accounts"]