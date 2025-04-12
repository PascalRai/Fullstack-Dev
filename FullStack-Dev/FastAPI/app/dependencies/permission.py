from fastapi import Depends, HTTPException

from app.models.models import User
from app.dependencies.authentication import get_current_user

def has_permission(permission_name: str):
    def wrapper(user: User = Depends(get_current_user)):
        if not any(p.name == permission_name for p in user.role.permissions):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper