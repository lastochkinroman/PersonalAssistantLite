"""
Основной FastAPI сервер с поддержкой Mistral API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime

from ai.core import Config
from ai.model_manager import ModelManager

app = FastAPI(
    title="Personal Assistant AI API",
    description="AI ассистент с Mistral API",
    version="4.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class DailyContext(BaseModel):
    date: str
    tasks: List[Dict[str, Any]] = []
    finances: Optional[List[Dict[str, Any]]] = []
    money: Optional[List[Dict[str, Any]]] = []
    workouts: List[Dict[str, Any]] = []
    diary: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []
    notes: List[Dict[str, Any]] = []

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context: DailyContext

class ModelSwitchRequest(BaseModel):
    model_name: str

# Глобальные объекты
config = Config()
model_manager = ModelManager(config)

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🚀 Запуск AI бэкенда с Mistral API")
    print("=" * 60)
    
    # Показываем информацию о системе
    system_info = model_manager.get_system_info()
    
    print(f"\n📊 Информация о системе:")
    print(f"  CPU: {system_info['system']['cpu_cores']} ядер")
    print(f"  Оперативная память: {system_info['system']['total_ram_gb']:.1f} GB")
    
    print(f"\n🤖 Текущая модель:")
    print(f"  Провайдер: {system_info['current_model']['provider']}")
    print(f"  Модель: {system_info['current_model']['name']}")
    print(f"  Доступна: {system_info['current_model']['available']}")
    
    print("\n" + "=" * 60)

@app.get("/")
async def root():
    current_model = model_manager.get_current_model()
    model_info = current_model.get_info() if current_model else {}
    
    return {
        "message": "Personal Assistant AI API",
        "version": "4.0.0",
        "model": model_info
    }

@app.get("/health")
async def health():
    current_model = model_manager.get_current_model()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "current_model": {
            "provider": model_manager.current_provider,
            "name": model_manager.current_model_name,
            "available": current_model.is_available() if current_model else False
        },
        "system": model_manager.get_system_info()['system']
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Основной эндпоинт для чата"""
    current_model = model_manager.get_current_model()
    
    if not current_model or not current_model.is_available():
        raise HTTPException(
            status_code=503,
            detail="Текущая модель недоступна. Проверьте подключение к Mistral API."
        )
    
    try:
        # Преобразуем сообщения в формат для модели
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Преобразуем контекст
        context = request.context.dict()
        
        # Генерация ответа
        response_text = current_model.generate(messages, context)
        
        return {
            "success": True,
            "response": response_text,
            "model": {
                "provider": model_manager.current_provider,
                "name": model_manager.current_model_name
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка генерации: {str(e)}"
        )

@app.get("/api/models/available")
async def get_available_models():
    """Получение списка доступных моделей"""
    available = model_manager.get_available_models()
    system_info = model_manager.get_system_info()
    
    return {
        "api": available['api'],
        "current": {
            "provider": model_manager.current_provider,
            "name": model_manager.current_model_name
        },
        "system": system_info['system']
    }

@app.post("/api/models/switch")
async def switch_model(request: ModelSwitchRequest):
    """Переключение модели"""
    try:
        success = model_manager.switch_to_api(request.model_name)
        
        if success:
            current_model = model_manager.get_current_model()
            
            return {
                "success": True,
                "message": f"Модель переключена на {request.model_name}",
                "current_model": {
                    "provider": model_manager.current_provider,
                    "name": model_manager.current_model_name,
                    "info": current_model.get_info() if current_model else {}
                }
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Не удалось переключиться на модель {request.model_name}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models/current")
async def get_current_model():
    """Получение информации о текущей модели"""
    current_model = model_manager.get_current_model()
    
    if not current_model:
        raise HTTPException(status_code=404, detail="Модель не загружена")
    
    return {
        "provider": model_manager.current_provider,
        "name": model_manager.current_model_name,
        "info": current_model.get_info(),
        "available": current_model.is_available()
    }

@app.get("/api/model/status")
async def get_model_status():
    """Получение статуса текущей модели"""
    current_model = model_manager.get_current_model()
    
    if not current_model:
        raise HTTPException(status_code=404, detail="Модель не загружена")
    
    return {
        "loaded": current_model.is_available(),
        "model_name": model_manager.current_model_name,
        "device": "api",
        "estimated_memory": "N/A",
        "cuda_available": False
    }

@app.get("/api/system/info")
async def get_system_info():
    """Получение информации о системе"""
    return model_manager.get_system_info()

if __name__ == "__main__":
    print("\n🌐 Сервер запускается...")
    print("📍 http://localhost:8000")
    print("📊 Проверка: http://localhost:8000/health")
    print("🤖 Модели: http://localhost:8000/api/models/available")
    print("\nНажмите Ctrl+C для остановки\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )