from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.services.user_service import UserService
from app.core.services.course_service import CourseService
from app.core.services.module_service import ModuleService
from app.core.services.topic_service import TopicService
from app.infrastructure.db.session import get_db

from app.infrastructure.db.repositories.user_repository import UserRepository
from app.infrastructure.db.repositories.course_repository import CourseRepository
from app.infrastructure.db.repositories.module_repository import ModuleRepository
from app.infrastructure.db.repositories.topic_repository import TopicRepository

def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository()

def get_course_repository(
    db: Session = Depends(get_db),
) -> CourseRepository:
    return CourseRepository()

def get_module_repository(
    db: Session = Depends(get_db),
) -> ModuleRepository:
    return ModuleRepository()

def get_topic_repository(
    db: Session = Depends(get_db),
) -> TopicRepository:
    return TopicRepository()

# -----------------------------
# UserService dependency
# -----------------------------
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db,get_user_repository(db))

# # -----------------------------
# # AgentService dependency
# # -----------------------------
# def get_agent_service(db: Session = Depends(get_db)):
#     return AgentService(db)

# # -----------------------------
# # CourseService dependency
# # -----------------------------
def get_course_service(db: Session = Depends(get_db)):
    return CourseService(db, get_course_repository(db))

# # -----------------------------
# # ModuleService dependency
# # -----------------------------
def get_module_service(db: Session = Depends(get_db)):
    return ModuleService(db, get_module_repository(db))

# # -----------------------------
# # TopicService dependency
# # -----------------------------
def get_topic_service(db: Session = Depends(get_db)):
    return TopicService(db, get_topic_repository(db))

# # # -----------------------------
# # # LMSService dependency
# # # -----------------------------
# # def get_lms_service(db: Session = Depends(get_db)):
# #     return LMSService(db)
