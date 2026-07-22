from fastapi import HTTPException, status


class CartItemExistsError(HTTPException):
    def __init__(self, detail: str = "This product is already in your cart"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class CartItemNotFoundError(HTTPException):
    def __init__(self, detail: str = "Cart item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class CartItemCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to add item to cart"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
