import logging

import structlog

logger = structlog.get_logger()


def configure_logging(*, debug_mode: bool) -> None:
    min_level = logging.DEBUG if debug_mode else logging.INFO
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer(
                exception_formatter=structlog.dev.plain_traceback
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(min_level=min_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
