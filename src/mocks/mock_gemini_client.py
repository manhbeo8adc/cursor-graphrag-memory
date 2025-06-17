"""
Mock Gemini Client cho Development Mode
Trả về responses giả để test mà không cần API key thật
"""
import time
import json
import random
from typing import Dict, Any, List


class MockGeminiClient:
    """Mock implementation của Gemini Client cho development"""
    
    def __init__(self, api_key: str = "mock_key"):
        """Khởi tạo mock client"""
        self.api_key = api_key
        self.request_count = 0
        
        # Pre-defined responses cho different use cases
        self.mock_responses = {
            "priority_analysis": ["low", "medium", "high", "critical"],
            "severity_analysis": ["minor", "major", "critical", "blocker"],
            "keywords": [
                "authentication, login, security, oauth",
                "database, storage, persistence, sql",
                "frontend, ui, user interface, react",
                "backend, api, server, endpoint",
                "testing, quality assurance, automation"
            ],
            "test_suggestions": [
                "1. Test valid input scenarios\n2. Test invalid input handling\n3. Test edge cases\n4. Test error conditions",
                "1. Unit tests for core functionality\n2. Integration tests for API endpoints\n3. E2E tests for user workflows",
                "1. Performance testing under load\n2. Security testing for vulnerabilities\n3. Compatibility testing across browsers"
            ],
            "impact_analysis": [
                {
                    "affected_modules": ["auth", "user", "session"],
                    "risk_level": "medium",
                    "recommended_tests": ["test_auth", "test_user_session", "test_login_flow"]
                },
                {
                    "affected_modules": ["database", "storage"],
                    "risk_level": "high", 
                    "recommended_tests": ["test_db_migration", "test_data_integrity"]
                },
                {
                    "affected_modules": ["frontend", "ui"],
                    "risk_level": "low",
                    "recommended_tests": ["test_ui_components", "test_responsive_design"]
                }
            ]
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Tạo mock response dựa trên prompt
        Mô phỏng việc call Gemini API
        """
        self.request_count += 1
        
        # Simulate API delay
        time.sleep(0.1)
        
        # Analyze prompt để trả về appropriate response
        prompt_lower = prompt.lower()
        
        if "priority" in prompt_lower or "urgent" in prompt_lower:
            return random.choice(self.mock_responses["priority_analysis"])
        
        elif "severity" in prompt_lower or "bug" in prompt_lower:
            return random.choice(self.mock_responses["severity_analysis"])
        
        elif "keyword" in prompt_lower or "extract" in prompt_lower:
            return random.choice(self.mock_responses["keywords"])
        
        elif "test" in prompt_lower and "suggest" in prompt_lower:
            return random.choice(self.mock_responses["test_suggestions"])
        
        elif "impact" in prompt_lower or "analysis" in prompt_lower:
            impact_data = random.choice(self.mock_responses["impact_analysis"])
            return json.dumps(impact_data, indent=2)
        
        elif "natural language" in prompt_lower or "chat" in prompt_lower:
            return self._generate_chat_response(prompt)
        
        else:
            # Default response
            return f"Mock response for prompt: {prompt[:50]}..."
    
    def _generate_chat_response(self, prompt: str) -> str:
        """Tạo chat response cho natural language queries"""
        responses = [
            "Dựa trên phân tích, tôi khuyên bạn nên chạy các tests liên quan đến authentication và user management.",
            "Thay đổi này có thể ảnh hưởng đến module database và storage. Hãy kiểm tra data integrity tests.",
            "Tôi thấy đây là một bug có mức độ nghiêm trọng medium. Nên ưu tiên fix trong sprint hiện tại.",
            "Feature này có dependency với authentication system. Hãy đảm bảo test integration giữa các modules.",
            "Dựa trên code changes, bạn nên update documentation cho API endpoints và user guide."
        ]
        
        return random.choice(responses)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Trả về thống kê sử dụng mock API"""
        return {
            "total_requests": self.request_count,
            "status": "mock_mode",
            "api_key": "mock_key_active",
            "cost_saved": f"${self.request_count * 0.01:.2f}"  # Giả định cost
        }
    
    def test_connection(self) -> bool:
        """Test connection - luôn return True cho mock"""
        return True
    
    def reset_stats(self):
        """Reset usage statistics"""
        self.request_count = 0


# Factory function để tạo mock client
def create_mock_gemini_client(api_key: str = "mock_key") -> MockGeminiClient:
    """Tạo mock Gemini client instance"""
    return MockGeminiClient(api_key)


# Example usage
if __name__ == "__main__":
    # Test mock client
    client = create_mock_gemini_client()
    
    print("🧪 Testing Mock Gemini Client")
    print("=" * 40)
    
    # Test different types of prompts
    test_prompts = [
        "Analyze the priority of this requirement: Critical security fix needed",
        "What is the severity of this bug: App crashes on login",
        "Extract keywords from: Implement OAuth2 authentication system",
        "Suggest test cases for user authentication feature",
        "Analyze impact of changes to auth module",
        "What tests should I run after fixing the login bug?"
    ]
    
    for prompt in test_prompts:
        response = client.generate_response(prompt)
        print(f"Prompt: {prompt[:50]}...")
        print(f"Response: {response}")
        print("-" * 40)
    
    print(f"Usage Stats: {client.get_usage_stats()}") 