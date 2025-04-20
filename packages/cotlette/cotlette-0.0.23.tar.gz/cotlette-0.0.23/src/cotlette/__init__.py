__version__ = "0.0.23"


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
        
        # Подключение роутеров
        self.include_routers()
        
        # Получить абсолютный путь к текущей диретории
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        static_directory = os.path.join(current_directory, "static")
        self.mount("/static", StaticFiles(directory=static_directory), name="static")

    def include_routers(self):

        # # Подключаем роутеры к приложению
        # from cotlette.urls import urls_router, api_router
        # self.include_router(urls_router)
        # self.include_router(api_router, prefix="/api", tags=["common"],)

        for template in self.settings.TEMPLATES:
            template_dirs = template.get("DIRS")
            template_dirs = [os.path.join(self.settings.BASE_DIR, path) for path in template_dirs]
        # print('template_dirs', template_dirs)

        # Проверка и импорт установленных приложений
        logger.info(f"Loading apps and routers:")
        for app_path in self.settings.INSTALLED_APPS:
            # try:
            # Динамически импортируем модуль
            module = importlib.import_module(app_path)
            logger.info(f"✅'{app_path}'")

            # Если модуль содержит роутеры, подключаем их
            if hasattr(module, "router"):
                self.include_router(module.router)
                logger.info(f"✅'{app_path}.router'")
            else:
                logger.warning(f"⚠️ '{app_path}.router'")
            # except Exception as e:
            #     logger.error(f"❌'{app_path}': {str(e)}")
