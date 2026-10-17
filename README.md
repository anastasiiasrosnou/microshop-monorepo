# Microshop Monorepo

Учебный проект: три Flask-микросервиса, FastAPI Gateway, Flask веб-интерфейс и GitHub Actions CI.

## Локальная проверка

```bash
pip install -r requirements.txt
python -m pytest
```

## Запуск (пять отдельных терминалов из корня проекта)

```bash
python products_service/app.py
python orders_service/app.py
python customers_service/app.py
python -m uvicorn api_gateway.main:app --port 8000
python web_app/app.py
```

Интерфейс: http://localhost:5004; Swagger: http://localhost:8000/docs.

## GitHub Actions

Workflow `.github/workflows/ci_pipeline.yml` запускает Flake8 и pytest при push и pull request в main/master.

Для демонстрации ошибки по заданию временно удалите двоеточие после `def get_products()` в `products_service/app.py`, отправьте коммит и убедитесь, что Actions завершился ошибкой. Затем восстановите двоеточие и отправьте новый коммит.
