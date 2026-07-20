from fastapi import HTTPException, status


class ProductExistsError(HTTPException):
    def __init__(self, detail: str = "Product already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ProductNotFoundError(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ProductCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create product"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
