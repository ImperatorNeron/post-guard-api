import os

DC = "docker compose"
DL = "docker logs"

APP_FILE = "docker_compose/app.yaml"
APP_CONTAINER = "main-app"

STORAGES_FILE = "docker_compose/storages.yaml"
STORAGES_CONTAINER = "postgresql-container"

ENV = "--env-file .env"


def app(target, source, env):
    command = f"{DC} -f {APP_FILE} -f {STORAGES_FILE} {ENV} up --build -d"
    return os.system(command)


def app_logs(target, source, env):
    command = f"{DL} {APP_CONTAINER} -f"
    return os.system(command)


def app_down(target, source, env):
    command = f"{DC} -f {APP_FILE} -f {STORAGES_FILE} {ENV} down"
    return os.system(command)


Command("up", [], app)
Command("down", [], app_down)
Command("logs", [], app_logs)
