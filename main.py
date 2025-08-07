# AGORA_BLOCK: start:main_app
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from src.api.auth import router as auth_router
from src.infrastructure.monitoring.monitoringService import monitoring_service
from src.infrastructure.error.errorHandler import ErrorHandler

# AGORA_BLOCK: start:app_initialization
# Создание приложения FastAPI
app = FastAPI(
   title="Agora.AI API",
   description="Интеллектуальная платформа B2B-сотрудничества",
   version="1.0.0"
)
# AGORA_BLOCK: end:app_initialization

# AGORA_BLOCK: start:cors_setup
# Настройка CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # В проде нужно указать конкретные домены
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
# AGORA_BLOCK: end:cors_setup

# AGORA_BLOCK: start:routers_registration
# Подключение роутеров
app.include_router(auth_router, prefix="/api/v1")
# TODO: Добавить другие роутеры по мере создания
# app.include_router(profile_router, prefix="/api/v1")
# app.include_router(match_router, prefix="/api/v1")
# app.include_router(logistics_router, prefix="/api/v1")
# app.include_router(contract_router, prefix="/api/v1")
# app.include_router(ai_router, prefix="/api/v1")
# app.include_router(reputation_router, prefix="/api/v1")
# app.include_router(blockchain_router, prefix="/api/v1")
# AGORA_BLOCK: end:routers_registration

# AGORA_BLOCK: start:middleware_logging
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
   
   # Добавление заголовков с метриками
   response.headers["X-Process-Time"] = str(process_time)
   
   return response
# AGORA_BLOCK: end:middleware_logging

# AGORA_BLOCK: start:exception_handlers
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

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
   """Обработчик для 404 ошибок"""
   return JSONResponse(
       status_code=404,
       content={"detail": "Ресурс не найден"}
   )

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
   """Обработчик ошибок валидации"""
   return JSONResponse(
       status_code=422,
       content={"detail": "Ошибка валидации данных", "errors": str(exc)}
   )
# AGORA_BLOCK: end:exception_handlers

# AGORA_BLOCK: start:startup_shutdown_events
@app.on_event("startup")
async def startup_event():
   """События при запуске приложения"""
   monitoring_service.log_event("app.startup", {"message": "Agora.AI API starting..."})
   # TODO: Инициализация подключений к БД
   # TODO: Инициализация кэша
   # TODO: Проверка переменных окружения

@app.on_event("shutdown")
async def shutdown_event():
   """События при остановке приложения"""
   monitoring_service.log_event("app.shutdown", {"message": "Agora.AI API shutting down..."})
   # TODO: Закрытие подключений к БД
   # TODO: Очистка кэша
   # TODO: Сохранение состояния
# AGORA_BLOCK: end:startup_shutdown_events

# AGORA_BLOCK: start:health_endpoints
@app.get("/")
async def root():
   """Корневой эндпоинт для проверки работы API"""
   return {
       "message": "Agora.AI API is running",
       "version": "1.0.0",
       "docs": "/docs",
       "health": "/health"
   }

@app.get("/health")
async def health_check():
   """Эндпоинт для проверки здоровья сервиса"""
   return {
       "status": "healthy",
       "timestamp": time.time(),
       "uptime": getattr(app, 'start_time', None)
   }

@app.get("/health/ready")
async def readiness_check():
   """Проверка готовности сервиса к работе"""
   # TODO: Проверить подключение к БД
   # TODO: Проверить доступность внешних сервисов
   return {
       "status": "ready",
       "checks": {
           "database": "ok",
           "cache": "ok",
           "external_apis": "ok"
       }
   }

@app.get("/health/live")
async def liveness_check():
   """Проверка что сервис живой"""
   return {"status": "alive"}
# AGORA_BLOCK: end:health_endpoints

# AGORA_BLOCK: start:api_info_endpoints
@app.get("/api/v1/info")
async def api_info():
   """Информация об API"""
   return {
       "name": "Agora.AI API",
       "version": "1.0.0",
       "description": "Интеллектуальная платформа B2B-сотрудничества",
       "endpoints": {
           "auth": "/api/v1/auth",
           "profile": "/api/v1/profile",
           "match": "/api/v1/match",
           "logistics": "/api/v1/logistics",
           "contract": "/api/v1/contract",
           "ai": "/api/v1/ai",
           "reputation": "/api/v1/reputation",
           "blockchain": "/api/v1/blockchain"
       }
   }

@app.get("/api/v1/metrics")
async def metrics_endpoint():
   """Базовые метрики приложения"""
   # TODO: Вернуть актуальные метрики
   return {
       "requests_total": 0,
       "errors_total": 0,
       "active_users": 0,
       "active_negotiations": 0,
       "successful_matches": 0
   }
# AGORA_BLOCK: end:api_info_endpoints

# AGORA_BLOCK: start:main_entry_point
if __name__ == "__main__":
   import uvicorn
   
   # Устанавливаем время запуска
   app.start_time = time.time()
   
   # Запуск сервера
   uvicorn.run(
       app, 
       host="0.0.0.0", 
       port=8000,
       reload=True,  # Автоперезагрузка при изменениях (только для разработки)
       log_level="info"
   )
# AGORA_BLOCK: end:main_entry_point

# AGORA_BLOCK: end:main_app