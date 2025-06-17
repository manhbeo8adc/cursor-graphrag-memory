"""
Gemini AI Client Wrapper
Mục đích: Wrap Gemini API với error handling và optimizations
"""

import logging
import google.generativeai as genai
from typing import Dict, Any, Optional
import asyncio
import json
from ..utils.logger import get_logger


class GeminiClient:
    """
    Wrapper cho Gemini-2.5-Flash API
    Tối ưu hóa cho cost-effectiveness và speed
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """Initialize Gemini client với API key"""
        self.api_key = api_key
        self.model_name = model
        self.logger = get_logger(__name__)
        
        # Configure Gemini với settings tối ưu
        genai.configure(api_key=api_key)
        
        # Sử dụng Gemini-2.5-Flash cho speed và cost
        self.model = genai.GenerativeModel(
            model,
            generation_config={
                "temperature": 0.1,      # Low temperature cho consistency
                "top_p": 0.8,           # Focused responses
                "top_k": 40,            # Balanced creativity
                "max_output_tokens": 2048,  # Reasonable limit
            }
        )
        
    async def analyze_requirement(self, requirement: str, project_name: str) -> Dict[str, Any]:
        """
        Phân tích requirement và extract metadata
        Cognitive load: < 70% - single responsibility
        """
        prompt = self._build_requirement_analysis_prompt(requirement, project_name)
        
        try:
            response = await self._generate_content_async(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            self.logger.warning(f"Gemini analysis failed: {e}")
            return self._get_fallback_analysis()
    
    async def analyze_feature_dependency(self, feature_a: str, feature_b: str, 
                                       relationship_type: str) -> Dict[str, Any]:
        """
        Phân tích impact của feature dependency
        Cognitive load: < 70% - focused on dependency analysis
        """
        prompt = self._build_dependency_analysis_prompt(feature_a, feature_b, relationship_type)
        
        try:
            response = await self._generate_content_async(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            self.logger.warning(f"Dependency analysis failed: {e}")
            return self._get_fallback_dependency_analysis()
    
    async def analyze_code_change_impact(self, file_paths: list[str], 
                                       change_type: str) -> Dict[str, Any]:
        """
        Phân tích impact của code changes
        NEW: Hỗ trợ doc/code impact analysis
        """
        prompt = self._build_code_change_analysis_prompt(file_paths, change_type)
        
        try:
            response = await self._generate_content_async(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            self.logger.warning(f"Code change analysis failed: {e}")
            return self._get_fallback_code_analysis()
    
    async def analyze_document_staleness(self, doc_path: str, 
                                       related_features: list[str]) -> Dict[str, Any]:
        """
        Phân tích document staleness và update needs
        NEW: Hỗ trợ automatic doc update detection
        """
        prompt = self._build_document_staleness_prompt(doc_path, related_features)
        
        try:
            response = await self._generate_content_async(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            self.logger.warning(f"Document staleness analysis failed: {e}")
            return self._get_fallback_document_analysis()
    
    async def process_natural_language(self, message: str) -> str:
        """
        Xử lý natural language messages từ user
        Return formatted response for MCP tools
        """
        prompt = self._build_natural_language_prompt(message)
        
        try:
            response = await self._generate_content_async(prompt)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Natural language processing failed: {e}")
            return f"❌ Lỗi xử lý natural language: {str(e)}"
    
    # Private helper methods
    
    async def _generate_content_async(self, prompt: str):
        """Generate content with async support"""
        # Note: google.generativeai doesn't have native async support
        # We'll use asyncio.to_thread for now
        return await asyncio.to_thread(self.model.generate_content, prompt)
    
    def _build_requirement_analysis_prompt(self, requirement: str, project_name: str) -> str:
        """Build prompt cho requirement analysis - helper method"""
        return f"""
        Phân tích requirement và trả về JSON:
        
        Requirement: {requirement}
        Project: {project_name}
        
        Format JSON:
        {{
            "category": "functional|non-functional|business|technical",
            "complexity": "low|medium|high",
            "dependencies": ["dep1", "dep2"],
            "risk_areas": ["risk1", "risk2"],
            "testing_types": ["unit", "integration", "e2e"],
            "affected_docs": ["README.md", "API.md"],
            "affected_code_files": ["src/module.py"]
        }}
        """
    
    def _build_dependency_analysis_prompt(self, feature_a: str, feature_b: str, 
                                        relationship_type: str) -> str:
        """Build prompt cho dependency analysis - helper method"""
        return f"""
        Phân tích impact của relationship:
        
        Feature A: {feature_a}
        Feature B: {feature_b}  
        Relationship: {relationship_type}
        
        Trả về JSON:
        {{
            "impact_areas": ["area1", "area2"],
            "risk_score": 1-10,
            "mitigation_strategies": ["strategy1", "strategy2"],
            "affected_tests": ["test1.py", "test2.py"],
            "documentation_updates": ["doc1.md", "doc2.md"]
        }}
        """
    
    def _build_code_change_analysis_prompt(self, file_paths: list[str], 
                                         change_type: str) -> str:
        """Build prompt cho code change analysis"""
        files_str = ", ".join(file_paths)
        return f"""
        Phân tích impact của code changes:
        
        Changed Files: {files_str}
        Change Type: {change_type}
        
        Trả về JSON:
        {{
            "affected_features": ["feature1", "feature2"],
            "required_tests": ["test1.py", "test2.py"],
            "documentation_updates": ["README.md", "API.md"],
            "risk_level": "low|medium|high|critical",
            "breaking_changes": true/false,
            "rollback_complexity": "low|medium|high"
        }}
        """
    
    def _build_document_staleness_prompt(self, doc_path: str, 
                                       related_features: list[str]) -> str:
        """Build prompt cho document staleness analysis"""
        features_str = ", ".join(related_features)
        return f"""
        Phân tích document staleness:
        
        Document: {doc_path}
        Related Features: {features_str}
        
        Trả về JSON:
        {{
            "needs_update": true/false,
            "staleness_score": 0-10,
            "update_priority": "low|medium|high",
            "suggested_sections": ["section1", "section2"],
            "estimated_effort": "30min|1h|2h|4h"
        }}
        """
    
    def _build_natural_language_prompt(self, message: str) -> str:
        """Build prompt cho natural language processing"""
        return f"""
        Xử lý natural language message và trả về structured response:
        
        User Message: {message}
        
        Hãy phân tích message và trả về response hữu ích, bao gồm:
        - Hiểu ý đồ của user
        - Gợi ý hành động cụ thể
        - Tools nào có thể sử dụng
        - Thông tin bổ sung nếu cần
        
        Format: Friendly, helpful, và actionable
        """
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response với error handling"""
        try:
            # Clean response text (remove markdown formatting)
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            
            return json.loads(clean_text.strip())
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse JSON response: {e}")
            return {}
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Fallback analysis khi Gemini fail"""
        return {
            "category": "functional",
            "complexity": "medium", 
            "dependencies": [],
            "risk_areas": [],
            "testing_types": ["unit"],
            "affected_docs": [],
            "affected_code_files": []
        }
    
    def _get_fallback_dependency_analysis(self) -> Dict[str, Any]:
        """Fallback dependency analysis"""
        return {
            "impact_areas": ["unknown"],
            "risk_score": 5,
            "mitigation_strategies": ["thorough_testing"],
            "affected_tests": [],
            "documentation_updates": []
        }
    
    def _get_fallback_code_analysis(self) -> Dict[str, Any]:
        """Fallback code change analysis"""
        return {
            "affected_features": [],
            "required_tests": [],
            "documentation_updates": [],
            "risk_level": "medium",
            "breaking_changes": False,
            "rollback_complexity": "medium"
        }
    
    def _get_fallback_document_analysis(self) -> Dict[str, Any]:
        """Fallback document analysis"""
        return {
            "needs_update": False,
            "staleness_score": 5,
            "update_priority": "medium",
            "suggested_sections": [],
            "estimated_effort": "1h"
        }
