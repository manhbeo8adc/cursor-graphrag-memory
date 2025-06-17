"""
NLP Service - Natural Language Processing
Mục đích: Xử lý natural language messages từ user
"""

import logging
from typing import Dict, Any, Optional
from ..models.gemini_client import GeminiClient
from ..utils.logger import get_logger


class NLPService:
    """
    Natural Language Processing Service
    SRP: Chỉ lo việc xử lý natural language
    """
    
    def __init__(self, gemini_client: GeminiClient, logger=None):
        """Initialize NLP service với Gemini client"""
        self.gemini = gemini_client
        self.logger = logger or get_logger(__name__)
    
    async def process_natural_language(self, message: str) -> str:
        """
        Xử lý natural language message và trả về helpful response
        SRP: Chỉ lo việc process natural language
        """
        try:
            # Analyze message intent
            intent = self._analyze_message_intent(message)
            
            # Process with Gemini
            response = await self.gemini.process_natural_language(message)
            
            # Format response with intent-based suggestions
            formatted_response = self._format_response_with_suggestions(message, response, intent)
            
            self.logger.info(f"Processed natural language message: {message[:50]}...")
            return formatted_response
            
        except Exception as e:
            self.logger.error(f"Failed to process natural language: {e}")
            return f"❌ Lỗi xử lý natural language: {str(e)}"
    
    def _analyze_message_intent(self, message: str) -> str:
        """
        Phân tích intent của message
        Simple keyword-based analysis (có thể enhance với ML)
        """
        message_lower = message.lower()
        
        # Intent keywords mapping
        intent_keywords = {
            "store_requirement": ["requirement", "yêu cầu", "tính năng", "feature", "lưu", "thêm"],
            "store_bug": ["bug", "lỗi", "error", "sự cố", "problem", "issue"],
            "get_tests": ["test", "kiểm tra", "chạy", "run", "testing"],
            "search": ["tìm", "search", "find", "lookup", "query"],
            "analyze": ["phân tích", "analyze", "impact", "tác động"],
            "help": ["help", "giúp", "hướng dẫn", "cách", "how"]
        }
        
        # Find matching intent
        for intent, keywords in intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "general"
    
    def _format_response_with_suggestions(self, original_message: str, 
                                        gemini_response: str, intent: str) -> str:
        """
        Format response với intent-based suggestions
        """
        # Base response from Gemini
        formatted = f"🤖 **AI Assistant Response:**\n\n{gemini_response}\n\n"
        
        # Add intent-specific suggestions
        suggestions = self._get_intent_suggestions(intent)
        if suggestions:
            formatted += f"💡 **Gợi ý các tools hữu ích:**\n{suggestions}"
        
        return formatted
    
    def _get_intent_suggestions(self, intent: str) -> str:
        """
        Lấy suggestions dựa trên intent
        """
        suggestions_map = {
            "store_requirement": """
- `store_project_requirement`: Lưu requirement mới
- `store_feature_dependency`: Lưu dependency giữa features
- `store_user_feedback`: Lưu feedback từ user""",
            
            "store_bug": """
- `store_bug_report`: Lưu bug report chi tiết
- `get_bug_impact_analysis`: Phân tích tác động của bug
- `store_code_change`: Lưu code changes liên quan""",
            
            "get_tests": """
- `get_tests_to_run`: Lấy danh sách tests cần chạy
- `get_comprehensive_test_plan`: Tạo test plan chi tiết
- `get_regression_risk`: Đánh giá rủi ro regression""",
            
            "search": """
- `search_memory`: Tìm kiếm trong memory system
- `get_related_features`: Tìm features liên quan
- `get_documents_to_update`: Tìm docs cần update""",
            
            "analyze": """
- `get_change_impact_analysis`: Phân tích tác động thay đổi
- `get_bug_impact_analysis`: Phân tích tác động bug
- `get_regression_risk`: Đánh giá rủi ro regression""",
            
            "help": """
- `natural_language_handler`: Chat với AI assistant
- `search_memory`: Tìm kiếm thông tin
- Kiểm tra các tools khác trong MCP server"""
        }
        
        return suggestions_map.get(intent, "")
    
    async def analyze_user_intent_advanced(self, message: str) -> Dict[str, Any]:
        """
        Advanced intent analysis using Gemini
        Có thể sử dụng cho future enhancements
        """
        try:
            prompt = f"""
            Phân tích intent của user message và trả về JSON:
            
            Message: "{message}"
            
            Trả về JSON format:
            {{
                "intent": "store_requirement|store_bug|get_tests|search|analyze|help|general",
                "confidence": 0.0-1.0,
                "entities": ["entity1", "entity2"],
                "suggested_action": "specific action to take",
                "required_params": ["param1", "param2"]
            }}
            """
            
            response = await self.gemini._generate_content_async(prompt)
            return self.gemini._parse_json_response(response.text)
            
        except Exception as e:
            self.logger.warning(f"Advanced intent analysis failed: {e}")
            return {
                "intent": "general",
                "confidence": 0.5,
                "entities": [],
                "suggested_action": "Use natural_language_handler tool",
                "required_params": []
            }
