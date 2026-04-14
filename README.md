SiteRpg — минимальная Flask-игра

Быстрый старт:

1. Создать виртуальное окружение и активировать его.

Windows (PowerShell):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Запустить приложение:

```powershell
python main.py
```

Замечания:
- Секретный ключ можно задать через переменную окружения `SITE_RPG_SECRET`.
- База данных создаётся автоматически (`sqlite:///game.db`).
- `.gitignore` уже настроен для исключения `.venv` и `instance/`.
