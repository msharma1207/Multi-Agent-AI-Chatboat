from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse, SignupRequest
from app.services.agent_orchestrator import orchestrate_agent_flow
from app.services.auth_service import AuthService

router = APIRouter()
service = AuthService()


@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest) -> LoginResponse:
    try:
        service.signup(payload.email, payload.password, payload.name)
    except Exception as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return LoginResponse(access_token="demo-token", refresh_token="demo-refresh", token_type="bearer")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    try:
        tokens = service.login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid credentials") from exc

    orchestrate_agent_flow("auth", "login")
    return LoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
    )
