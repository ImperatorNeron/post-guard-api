import os

DC = "docker compose"
DL = "docker logs"

APP_FILE = "docker_compose/app.yaml"
APP_CONTAINER = "main-app"


def app(target, source, env):
    command = f"{DC} -f {APP_FILE} up --build -d"
    return os.system(command)


def app_logs(target, source, env):
    command = f"{DL} {APP_CONTAINER} -f"
    return os.system(command)


def app_down(target, source, env):
    command = f"{DC} -f {APP_FILE} down"
    return os.system(command)


Command("up", [], app)
Command("down", [], app_down)
Command("logs", [], app_logs)
