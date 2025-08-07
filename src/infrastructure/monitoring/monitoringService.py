# AGORA_BLOCK: start:monitoring_service
import logging
import time
from typing import Any, Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, start_http_server

logger = logging.getLogger(__name__)

class MonitoringService:
    """Сервис мониторинга и логирования"""
    
    def __init__(self, port: int = 8001):
        # Запуск Prometheus метрик
        start_http_server(port)
        
        # Основные метрики
        self.api_requests = Counter('agora_api_requests_total', 'API requests', ['endpoint', 'method', 'status'])
        self.api_errors = Counter('agora_api_errors_total', 'API errors', ['endpoint', 'status'])
        self.active_negotiations = Gauge('agora_active_negotiations', 'Active negotiations count')
        self.successful_matches = Counter('agora_successful_matches_total', 'Successful matches count')
        self.request_duration = Histogram('agora_request_duration_seconds', 'Request duration')
        
        logger.info(f"Monitoring service started on port {port}")
    
    def log_event(self, event_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Логирование события
        
        Args:
            event_name: Название события
            data: Дополнительные данные
        """
        if data:
            logger.info(f"Event: {event_name}, Data: {data}")
        else:
            logger.info(f"Event: {event_name}")
    
    def increment_api_requests(self, endpoint: str, method: str, status: int) -> None:
        """
        Увеличение счетчика API запросов
        
        Args:
            endpoint: Эндпоинт
            method: HTTP метод
            status: HTTP статус
        """
        self.api_requests.labels(endpoint=endpoint, method=method, status=status).inc()
    
    def increment_api_errors(self, endpoint: str, status: int) -> None:
        """
        Увеличение счетчика ошибок API
        
        Args:
            endpoint: Эндпоинт
            status: HTTP статус
        """
        self.api_errors.labels(endpoint=endpoint, status=status).inc()
    
    def track_negotiation_start(self) -> None:
        """Отслеживание начала переговоров"""
        self.active_negotiations.inc()
    
    def track_negotiation_end(self, success: bool = True) -> None:
        """
        Отслеживание окончания переговоров
        
        Args:
            success: Успешность переговоров
        """
        self.active_negotiations.dec()
        if success:
            self.successful_matches.inc()
    
    def track_request_duration(self, duration: float) -> None:
        """
        Отслеживание длительности запроса
        
        Args:
            duration: Длительность в секундах
        """
        self.request_duration.observe(duration)

# Создаем экземпляр сервиса
monitoring_service = MonitoringService()
# AGORA_BLOCK: end:monitoring_service