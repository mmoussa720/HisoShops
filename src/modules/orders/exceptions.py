from fastapi import HTTPException, status


class OrderExistsError(HTTPException):
    def __init__(self, detail: str = "Order already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class OrderNotFoundError(HTTPException):
    def __init__(self, detail: str = "Order not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class OrderCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create order"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class RiderNotAvailableError(HTTPException):
    def __init__(self, detail: str = "Rider is not available"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
