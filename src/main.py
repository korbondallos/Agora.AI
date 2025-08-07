# AGORA_BLOCK: start:main
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from api.auth import router as auth_router
from infrastructure.monitoring.monitoringService import monitoring_service
from infrastructure.error.errorHandler import ErrorHandler

# Создание приложения FastAPI
app = FastAPI(
    title="Agora.AI API",
    description="Интеллектуальная платформа B2B-сотрудничества",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router, prefix="/api/v1")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования запросов"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # Расчет времени выполнения
    process_time = time.time() - start_time
    
    # Логирование запроса
    monitoring_service.increment_api_requests(
        endpoint=request.url.path,
        method=request.method,
        status=response.status_code
    )
    
    # Отслеживание длительности запроса
    monitoring_service.track_request_duration(process_time)
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений"""
    error_info = ErrorHandler.handle_error(exc, "global")
    
    # Логирование ошибки
    monitoring_service.increment_api_errors(
        endpoint=request.url.path,
        status=500
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"}
    )

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API"""
    return {"message": "Agora.AI API is running"}

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# AGORA_BLOCK: end:main