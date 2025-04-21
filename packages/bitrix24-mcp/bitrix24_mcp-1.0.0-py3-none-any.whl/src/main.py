from src.config import SettingsManager
from src.infrastructure.logging.logger import configure_log_level, logger
from src.presentation.mcp import create_mcp_server

server = create_mcp_server()


def run() -> None:
    """Точка входа для запуска MCP сервера.

    Эта функция инициализирует настройки и запускает MCP сервер
    для обработки входящих запросов.
    """
    settings = SettingsManager.init()
    configure_log_level(settings.LOG_LEVEL)

    logger.info("Запуск MCP сервера")

    server.run()


if __name__ == "__main__":
    run()
