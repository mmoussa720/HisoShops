from fastapi import APIRouter
from ....modules.users.routes import router as users_router
from ....infrastructure.auth.routes import router as auth_router

router=APIRouter(prefix="/v1")
router.include_router(users_router,prefix="/users")
router.include_router(auth_router,prefix="/auth")
