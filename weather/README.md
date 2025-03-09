# Weather App

## 功能說明
- 獲取即時天氣警報
- 獲取特定位置的天氣預報
- 支援多城市查詢
- 提供詳細的天氣資訊，包括溫度、風速和預報描述

## 安裝需求
### 環境需求
- Python 3.12+
- uv 套件管理工具

### 安裝步驟
1. 複製專案到本地
   ```bash
   git clone [repository-url]
   cd weather
   ```

2. 使用 uv 安裝 pyproject.toml 中定義的依賴項
   ```bash
   uv pip sync pyproject.toml
   ```

3. 執行應用程式
   ```bash
   python -m weather
   ```

4. Add into Cursor
   - Cursor settings
   - Add MCP
   - Type `command`
   ```bash
   uv --directory /Users/louisfghbvc/Desktop/mcp-servers/weather run weather.py
   ```

## 使用說明
### 獲取天氣警報
使用 `get_alerts` 函數來獲取特定州的天氣警報：
```python
# 獲取加州的天氣警報
alerts = get_alerts("CA")
print(alerts)
```

### 獲取天氣預報
使用 `get_forecast` 函數來獲取特定位置的天氣預報：
```python
# 獲取舊金山的天氣預報 (37.7749, -122.4194)
forecast = get_forecast(37.7749, -122.4194)
print(forecast)
```

## 專案結構
- `weather.py`: 主要應用程式代碼
- `pyproject.toml`: 專案配置和相依套件

## Demo
請參考 [Spec Story](./SpecStory.md)

## 授權
MIT License
