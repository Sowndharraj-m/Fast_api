from fastapi import APIRouter , Depends , status , HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models , schemas , utilits   

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(user_credentials:schemas.userlogin,b:Session = Depends(get_db)):
    user = b.query(models.User).filter(models.User.email==user_credentials.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_credentials.email} not found"
        )
    user_password = utilits.verify_password(user_credentials.password, user.password)
    if not user_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
#create token

    return user