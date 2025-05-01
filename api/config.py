class ProjectSettings:
    database_url: str = "postgresql+asyncpg://user:password@127.0.0.1:5433/getcar"
    server_reload: bool = True
    server_host: str = "localhost"
    server_port: str = 8000
    media_root: str = "static/media"


settings = ProjectSettings()
