from fabric.api import run
from fabric.context_managers import settings


def reset_database(host: str):
    """Обнулить базу данных"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"stas@{host}"):
        command = f"{manage_dot_py} flush --noinput"
        print(f"execute: {command}")
        run(command)


def create_session_on_server(host: str, email: str):
    """Создать сеанс на сервере"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"stas@{host}"):
        command = f"{manage_dot_py} create_session {email}"
        print(f"execute: {command}")
        session_key = run(command)
        return session_key.strip()


def _get_manage_dot_py(host: str) -> str:
    """Получить начало команды с файлом manage.py"""
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/superlists/manage.py"
