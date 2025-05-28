from fastapi import APIRouter

router_v1 = APIRouter()
router_v2 = APIRouter()


@router_v1.get("/login", tags=["auth"])
@router_v2.get("/login", tags=["auth"])
def login():
    return {"message": "TODO something with oauth2!"}


# TODO: just an example of how a newer api can have extra routes. Remove before going live
@router_v2.get("/login2", tags=["auth"])
def login2():
    return {"message": "TODO something with oauth2, example versioning!"}
