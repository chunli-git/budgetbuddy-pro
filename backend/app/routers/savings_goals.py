from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.savings_goal import SavingsGoal
from app.models.user import User
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalRead

router = APIRouter(prefix="/savings-goals", tags=["savings goals"])


@router.post("/", response_model=SavingsGoalRead, status_code=status.HTTP_201_CREATED)
def create_savings_goal(
    goal_data: SavingsGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = SavingsGoal(
        name=goal_data.name,
        target_amount=goal_data.target_amount,
        current_amount=goal_data.current_amount,
        target_date=goal_data.target_date,
        user_id=current_user.id,
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal