from fastapi import APIRouter
from ....modules.users.routes import router as users_router
from ....modules.categories.routes import router as categories_router
from ....modules.products.routes import router as products_router
from ....modules.reviews.routes import router as reviews_router
from ....infrastructure.auth.routes import router as auth_router

router=APIRouter(prefix="/v1")
router.include_router(users_router,prefix="/users")
router.include_router(categories_router,prefix="/categories")
router.include_router(products_router,prefix="/products")
router.include_router(reviews_router,prefix="/reviews")
router.include_router(auth_router,prefix="/auth")
