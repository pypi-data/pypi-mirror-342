class env_manager:
    """
    环境管理器，prod：生产（默认）debug：调试
    """
    _instance = None
    _mode = "prod"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_mode(cls, mode="prod"):
        cls._mode = mode

    @classmethod
    def is_debug(cls):
        return cls._mode == "debug"

    @classmethod
    def is_prod(cls):
        return cls._mode == "prod"
