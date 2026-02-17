"""
Менеджер для работы с Mistral API моделью
"""
from typing import Dict, Any, List, Optional
from .core import AIModel, Config
from .mistral_client import MistralModel
import psutil


class ModelManager:
    """Управление AI моделями"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.current_model: Optional[AIModel] = None
        self.current_provider = "api"
        self.current_model_name = self.config.get('defaults.model', 'mistral-small-latest')
        
        # Загружаем начальную модель
        self._load_initial_model()
    
    def _load_initial_model(self):
        """Загрузка начальной модель"""
        model_name = self.current_model_name
        
        print(f"🎯 Инициализация модели: {model_name} (api)")
        
        self.current_model = MistralModel(model_name, self.config)
    
    def get_current_model(self) -> AIModel:
        """Получение текущей модели"""
        return self.current_model
    
    def switch_to_api(self, model_name: str = "mistral-small-latest") -> bool:
        """Переключение на Mistral API модель"""
        print(f"🔄 Переключение на API модель: {model_name}")
        
        new_model = MistralModel(model_name, self.config)
        
        if new_model.is_available():
            self.current_model = new_model
            self.current_provider = "api"
            self.current_model_name = model_name
            
            # Сохраняем в конфиг
            self.config.set('defaults.provider', 'api')
            self.config.set('defaults.model', model_name)
            
            print(f"✅ Переключено на {model_name}")
            return True
        else:
            print(f"❌ API модель {model_name} недоступна")
            return False
    
    def get_available_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """Получение списка доступных моделей"""
        available = {
            "api": []
        }
        
        # API модели
        api_models = self.config.get('models.api.available', [])
        for model in api_models:
            model_info = model.copy()
            model_info['provider'] = 'api'
            model_info['type'] = 'api'
            model_info['current'] = (
                self.current_provider == 'api' and 
                self.current_model_name == model['name']
            )
            
            # Проверяем доступность Mistral
            if model['name'].startswith('mistral'):
                test_model = MistralModel(model['name'], self.config)
                model_info['available'] = test_model.is_available()
            
            available['api'].append(model_info)
        
        return available
    
    def get_system_info(self) -> Dict[str, Any]:
        """Информация о системе"""
        info = {
            "system": {
                "cuda_available": False,
                "torch_version": "N/A",
                "cpu_cores": psutil.cpu_count(),
                "total_ram_gb": psutil.virtual_memory().total / 1e9,
            },
            "current_model": {
                "provider": self.current_provider,
                "name": self.current_model_name,
                "available": self.current_model.is_available() if self.current_model else False,
            }
        }
        
        return info