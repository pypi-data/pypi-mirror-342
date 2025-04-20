__version__ = "0.0.26"


import os
import logging
# import importlib.util
import importlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from cotlette.conf import settings
from cotlette import shortcuts



logger = logging.getLogger("uvicorn")


class Cotlette(FastAPI):

    def __init__(self):
        super().__init__()

        self.settings = settings
        self.shortcuts = shortcuts

        # Получить абсолютный путь к текущей диретории
        self.cotlette_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Подключение роутеров
        self.include_routers()
        self.include_templates()
        self.include_static()

    def include_routers(self):
        # Проверка и импорт установленных приложений
        logger.info(f"Loading apps and routers:")
        for app_path in self.settings.INSTALLED_APPS:
            # Динамически импортируем модуль
            module = importlib.import_module(app_path)
            logger.info(f"✅'{app_path}'")

            # Если модуль содержит роутеры, подключаем их
            if hasattr(module, "router"):
                self.include_router(module.router)
                logger.info(f"✅'{app_path}.router'")
            else:
                logger.warning(f"⚠️ '{app_path}.router'")

    def include_templates(self):
        # Подключаем шаблоны указанные пользователем в SETTINGS
        for template in self.settings.TEMPLATES:
            template_dirs = template.get("DIRS")
            template_dirs = [os.path.join(self.settings.BASE_DIR, path) for path in template_dirs]

    def include_static(self):

        # Подключаем static фреймворка
        static_dir = os.path.join(self.cotlette_directory, "static")
        self.mount("/static", StaticFiles(directory=static_dir), name="static")

        # Подключаем static указанные пользователем в SETTINGS
        if self.settings.STATIC_URL:
            static_dir = os.path.join(self.settings.BASE_DIR, self.settings.STATIC_URL)
            self.mount("/static", StaticFiles(directory=static_dir), name="static")