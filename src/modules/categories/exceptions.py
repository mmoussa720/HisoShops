from fastapi import HTTPException, status


class CategoryExistsError(HTTPException):
    def __init__(self, detail: str = "Category already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class CategoryNotFoundError(HTTPException):
    def __init__(self, detail: str = "Category not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class CategoryCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create category"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
