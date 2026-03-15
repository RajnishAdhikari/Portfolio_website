from fastapi import APIRouter
from .health import router as health_router
from .auth import router as auth_router
from .personal import router as personal_router
from .education import router as education_router
from .skill import router as skill_router
from .experience import router as experience_router
from .project import router as project_router
from .article import router as article_router
from .resource_paper import router as resource_paper_router
from .certification import router as certification_router
from .extracurricular import router as extracurricular_router

api_router = APIRouter()

# Include all routers
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(personal_router, prefix="/personal", tags=["personal"])
api_router.include_router(education_router, prefix="/education", tags=["education"])
api_router.include_router(skill_router, prefix="/skills", tags=["skills"])
api_router.include_router(experience_router, prefix="/experience", tags=["experience"])
api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(article_router, prefix="/articles", tags=["articles"])
api_router.include_router(resource_paper_router, prefix="/resource-papers", tags=["resource-papers"])
api_router.include_router(certification_router, prefix="/certifications", tags=["certifications"])
api_router.include_router(extracurricular_router, prefix="/extracurricular", tags=["extracurricular"])
