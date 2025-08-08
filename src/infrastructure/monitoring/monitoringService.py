# AGORA_FILE: start:src/infrastructure/monitoring/monitoringService.py
# AGORA_BLOCK: start:monitoring_service
import logging
import time
from typing import Any, Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, start_http_server

logger = logging.getLogger(__name__)

# AGORA_BLOCK: start:monitoring_service_class
class MonitoringService:
    """Сервис мониторинга и логирования"""

    # AGORA_BLOCK: start:init
    def __init__(self, port: int = 8001):
        try:
            # Запуск Prometheus метрик
            start_http_server(port)

            # Основные метрики
            self.api_requests = Counter('agora_api_requests_total', 'API requests', ['endpoint', 'method', 'status'])
            self.api_errors = Counter('agora_api_errors_total', 'API errors', ['endpoint', 'status'])
            self.active_negotiations = Gauge('agora_active_negotiations', 'Active negotiations count')
            self.successful_matches = Counter('agora_successful_matches_total', 'Successful matches count')
            self.request_duration = Histogram('agora_request_duration_seconds', 'Request duration')

            logger.info(f"Monitoring service started on port {port}")
        except Exception as e:
            logger.warning(f"Monitoring service already running or port {port} is busy: {e}")
    # AGORA_BLOCK: end:init

    # AGORA_BLOCK: start:log_event
    def log_event(self, event_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Логирование события"""
        if data:
            logger.info(f"Event: {event_name}, Data: {data}")
        else:
            logger.info(f"Event: {event_name}")
    # AGORA_BLOCK: end:log_event

    # AGORA_BLOCK: start:increment_api_requests
    def increment_api_requests(self, endpoint: str, method: str, status: int) -> None:
        """Увеличение счетчика API запросов"""
        self.api_requests.labels(endpoint=endpoint, method=method, status=status).inc()
    # AGORA_BLOCK: end:increment_api_requests

    # AGORA_BLOCK: start:increment_api_errors
    def increment_api_errors(self, endpoint: str, status: int) -> None:
        """Увеличение счетчика ошибок API"""
        self.api_errors.labels(endpoint=endpoint, status=status).inc()
    # AGORA_BLOCK: end:increment_api_errors

    # AGORA_BLOCK: start:track_negotiation_start
    def track_negotiation_start(self) -> None:
        """Отслеживание начала переговоров"""
        self.active_negotiations.inc()
    # AGORA_BLOCK: end:track_negotiation_start

    # AGORA_BLOCK: start:track_negotiation_end
    def track_negotiation_end(self, success: bool = True) -> None:
        """Отслеживание окончания переговоров"""
        self.active_negotiations.dec()
        if success:
            self.successful_matches.inc()
    # AGORA_BLOCK: end:track_negotiation_end

    # AGORA_BLOCK: start:track_request_duration
    def track_request_duration(self, duration: float) -> None:
        """Отслеживание длительности запроса"""
        self.request_duration.observe(duration)
    # AGORA_BLOCK: end:track_request_duration
# AGORA_BLOCK: end:monitoring_service_class

# Создаем экземпляр сервиса
monitoring_service = MonitoringService()
# AGORA_BLOCK: end:monitoring_service
# AGORA_FILE: end:src/infrastructure/monitoring/monitoringService.py
