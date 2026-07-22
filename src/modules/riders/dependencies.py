from .services import RiderService
from fastapi import Depends
from typing import Annotated


def get_rider_service() -> RiderService:
    return RiderService()


RiderServiceDep = Annotated[RiderService, Depends(get_rider_service)]
