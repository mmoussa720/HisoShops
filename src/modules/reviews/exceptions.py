from fastapi import HTTPException, status


class ReviewExistsError(HTTPException):
    def __init__(self, detail: str = "Review already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ReviewNotFoundError(HTTPException):
    def __init__(self, detail: str = "Review not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ReviewCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create review"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserNotFoundForReviewError(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ProductNotFoundForReviewError(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
