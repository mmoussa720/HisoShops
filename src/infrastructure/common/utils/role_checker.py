
from ...auth.dependencies import getCurrentUserDep
from ...auth.exceptions import NotAuthorizedError
class RoleChecker:
    def __init__(self,allowed_roles:list[str]):
        self.allowed_roles=allowed_roles

    async def __call__(self,user:getCurrentUserDep):
        if user["is_super_user"]:
            return True
        if user["role"] is not None and user["role"] in self.allowed_roles:
            return True
        raise NotAuthorizedError("This user doesn't have enough permissions")