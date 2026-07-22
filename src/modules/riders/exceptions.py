from fastapi import HTTPException, status


class RiderExistsError(HTTPException):
    def __init__(self, detail: str = "Rider already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class RiderNotFoundError(HTTPException):
    def __init__(self, detail: str = "Rider not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class RiderCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create rider"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
