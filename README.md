# Personal Assistant Lite

Личный веб‑помощник с AI-ассистентом для ежедневного трекинга задач, финансов, тренировок и не только.

Занимаясь своим бытом в Obsidian, я столкнулся с проблемой. Я заполняю много своих данных в md файл, а после чего отдаю это в ручную в LLM. А что если всё будет в удобном интерфейсе и мои данные будут сами подтягиваться для встроенного чата с персональным AI помощником. Так и появился мой проект. Использую его сам каждый день.


## Возможности

- **Задачи**: список, статусы, приоритеты, дедлайны, теги, поиск
- **Деньги**: доход/расход, категории, суммы за месяц, топ категорий расходов
- **Тренировки**: дневник сессий, упражнения, подходы (reps/weight), простые PR (оценка 1RM)
- **AI Ассистент**: умный помощник на базе Mistral API с доступом к контексту вашего дня
- **Дневник**: записи о настроении и событиях
- **Календарь**: планирование событий
- **Заметки**: быстрые заметки с тегами

Все данные сохраняются локально в браузере (**localStorage**). Есть **Экспорт/Импорт JSON** для бэкапа.

## Требования

- **Frontend**: Node.js 18+, npm
- **Backend**: Python 3.8+, Mistral API ключ

---

## Быстрый старт

### 1. Установка и запуск Frontend

```bash
# Перейдите в корневую директорию проекта
cd PersonalAssistantLite

# Установите зависимости
npm install

# Запустите dev-сервер
npm run dev
```

Откройте адрес, который покажет Vite (обычно `http://localhost:5173`).

### 2. Настройка и запуск Backend (опционально)

Для работы AI-ассистента требуется настроить бэкенд:

```bash
# Перейдите в директорию backend
cd backend
```

#### 2.1 Настройка конфигурации

Скопируйте примеры конфигурации:

```bash
# Frontend
cp env.example .env

# Backend
cp backend/env.example backend/.env
cp backend/config.example.yaml backend/config.yaml
```

Отредактируйте `backend/.env` и вставьте ваш Mistral API ключ:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

> **Где получить API ключ?** Зарегистрируйтесь на [platform.mistral.ai](https://platform.mistral.ai) и создайте API ключ в разделе API Keys.

#### 2.2 Установка Python зависимостей

```bash
# Установите зависимости
pip install -r requirements.txt
```

#### 2.3 Запуск Backend

**Windows:**
```bash
# Запуск через скрипт (установит зависимости автоматически)
start.bat

# Или напрямую
python main.py
```

**Linux/macOS:**
```bash
# Сделайте скрипт исполняемым
chmod +x start.sh

# Запустите
./start.sh

# Или напрямую
python3 main.py
```

Сервер будет доступен по адресу: `http://localhost:8000`

---

## Структура проекта

```
PersonalAssistantLite/
├── src/                      # Frontend (React + TypeScript)
│   ├── App.tsx              # Главный компонент приложения
│   ├── features/            # Фичи приложения
│   │   ├── ai-assistant/   # AI ассистент
│   │   ├── calendar/       # Календарь
│   │   ├── diary/          # Дневник
│   │   ├── money/          # Финансы
│   │   ├── notes/          # Заметки
│   │   ├── tasks/          # Задачи
│   │   └── workouts/       # Тренировки
│   └── lib/                 # Утилиты и API клиент
├── backend/                 # Backend (FastAPI)
│   ├── main.py             # Главный файл сервера
│   ├── config.yaml         # Конфигурация
│   ├── .env                # Переменные окружения
│   ├── requirements.txt    # Python зависимости
│   ├── start.bat           # Скрипт запуска (Windows)
│   ├── start.sh            # Скрипт запуска (Linux/macOS)
│   └── ai/                 # AI модули
│       ├── core.py         # Базовые интерфейсы
│       ├── mistral_client.py  # Mistral API клиент
│       └── model_manager.py   # Менеджер моделей
├── package.json            # Frontend зависимости
└── vite.config.ts          # Vite конфигурация
```

---

## API Endpoints Backend

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/` | GET | Основная информация API |
| `/health` | GET | Проверка здоровья сервиса |
| `/api/models/available` | GET | Список доступных моделей |
| `/api/models/current` | GET | Информация о текущей модели |
| `/api/models/switch` | POST | Переключение модели |
| `/api/chat` | POST | Чат с AI ассистентом |
| `/api/system/info` | GET | Информация о системе |

---

## Доступные модели AI

В файле `backend/config.yaml` настроены следующие модели:

| Модель | Описание |
|--------|----------|
| `mistral-small-latest` | Быстрая и недорогая (рекомендуется) |
| `mistral-medium-latest` | Хороший баланс скорости и качества |
| `mistral-large-latest` | Максимальное качество |

---

## Сборка Frontend

### Development сборка

```bash
npm run dev
```

### Production сборка

```bash
npm run build
npm run preview
```

После сборки приложение будет доступно по адресу, который покажет `vite preview` (обычно `http://localhost:4173`).

---

## Переменные окружения

### Frontend

Создайте `.env` файл в корне проекта (опционально):

```env
VITE_API_URL=http://localhost:8000
```

### Backend

```env
# Mistral API ключ (обязательно для работы AI)
MISTRAL_API_KEY=your_mistral_api_key_here

# Настройки локальных моделей (опционально)
LOCAL_MODEL_DEVICE=auto
LOCAL_MODEL_QUANTIZATION=4bit
```

---

## Устранение проблем

### Frontend

**Ошибка `npm install`:**
- Убедитесь, что Node.js 18+ установлен: `node --version`
- Удалите `node_modules` и `package-lock.json` и повторите установку

**Ошибка при запуске:**
- Проверьте, что порт 5173 свободен
- Используйте `npm run dev -- --host` для запуска на всех интерфейсах

### Backend

**Mistral API недоступен:**
- Проверьте, что API ключ корректно настроен в `.env` или `config.yaml`
- Проверьте лимиты API на [platform.mistral.ai](https://platform.mistral.ai)

**Ошибка `ModuleNotFoundError`:**
- Установите зависимости: `pip install -r requirements.txt`

**Порт 8000 занят:**
- Измените порт в `backend/main.py` (параметр `port` в `uvicorn.run`)
- Или освободите порт 8000

---

## Лицензия

MIT License
