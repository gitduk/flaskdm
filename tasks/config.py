class Config:
    enable_utc = True
    timezone = 'Asia/Shanghai'
    broker_url = "amqp://flask:Zmxhc2s@localhost:5672/flask"
    result_backend = "redis://localhost:6379/1"

    # worker
    worker_concurrency = 10

    # task
    task_soft_time_limit = 6000  # 单个任务的运行时间不超过此值(秒)，否则会抛出(SoftTimeLimitExceeded)异常停止任务。
    task_serializer = "json"

    result_serializer = "json"
    accept_content = ["json"]
    worker_prefetch_multiplier = 1  # 禁用任务预取
    worker_max_tasks_per_child = 100  # worker执行100个任务自动销毁，防止内存泄露
    worker_disable_rate_limits = True  # 即使任务设置了明确的速率限制，也禁用所有速率限制。


class ProductionConfig(Config):
    """
    Production Config
    """


class DevelopmentConfig(Config):
    """
    Development Config
    """


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
