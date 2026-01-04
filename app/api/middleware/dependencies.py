from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.services.user_service import UserService
from app.infrastructure.db.session import get_db
# -----------------------------
# UserService dependency
# -----------------------------
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

# # -----------------------------
# # AgentService dependency
# # -----------------------------
# def get_agent_service(db: Session = Depends(get_db)):
#     return AgentService(db)

# # -----------------------------
# # CourseService dependency
# # -----------------------------
# def get_course_service(db: Session = Depends(get_db)):
#     return CourseService(db)

# # -----------------------------
# # LMSService dependency
# # -----------------------------
# def get_lms_service(db: Session = Depends(get_db)):
#     return LMSService(db)
