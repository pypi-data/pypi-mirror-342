# vebboard

**vebboard** — Python-библиотека для создания дашбордов из файлов и баз данных (CSV, Excel, JSON, SQLite, Google Sheets и др.).

## Возможности

- Простое создание дашбордов с графиками.
- Импорт данных из CSV, Excel, JSON, Parquet, SQLite, Google Sheets.
- Экспорт дашборда в HTML.
- Сохранение/загрузка конфигурации в JSON.
- Поддержка тем и кастомного оформления.

## Установка

```
pip install vebboard
```

## Пример использования

```python
from vebboard.core.dashboard import Dashboard
import pandas as pd

df = pd.DataFrame({
    'day': ['Mon', 'Tue', 'Wed'],
    'revenue': [100, 200, 150]
})

dashboard = Dashboard(\"Мой дашборд\")
dashboard.add_chart(df, chart_type='bar', x='day', y='revenue')
dashboard.show()
```