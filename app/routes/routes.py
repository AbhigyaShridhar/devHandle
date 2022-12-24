from fastapi import Depends, APIRouter

router = APIRouter()

from app.utils.jwtHandler import hasAccess
from ..devHandle.user.controller import userRouter, authRouter
from ..devHandle.community.controller import communityRouter
from ..devHandle.investment.controller import investorRouter

router.include_router(
    authRouter,
    prefix='/auth',
    tags=['Auth']
)

router.include_router(
    userRouter,
    prefix='/user',
    tags=['User'],
    dependencies=[Depends(hasAccess)]
)

router.include_router(
    communityRouter,
    prefix='/community',
    tags=['Community'],
    dependencies=[Depends(hasAccess)]
)

router.include_router(
    investorRouter,
    prefix='/investments',
    tags=['Investments'],
    dependencies=[Depends(hasAccess)]
)