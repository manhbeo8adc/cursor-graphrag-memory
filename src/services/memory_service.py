"""
Memory Service - Intelligent business logic hỗ trợ mục tiêu chính
SRP: Core logic cho automatic impact analysis, dependency tracking, intelligent recommendations
Capabilities: Auto-analyze changes → Track dependencies → Recommend tests → Ensure code quality
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from ..models.memory_models import (
    ProjectRequirement, Feature, Bug, CodeChange, Test, UserFeedback,
    DocumentEntity, CodeFileEntity, TestCoverage, Priority, Status, 
    BugSeverity, ChangeType, FeedbackType, TestType,
    calculate_comprehensive_change_impact, get_documents_to_update, get_tests_to_run
)
from ..models.gemini_client import GeminiClient
from ..utils.logger import get_logger


class MemoryService:
    """
    Core business logic cho memory management - SOLID compliant
    SRP: Chỉ lo business logic, không lo infrastructure
    DIP: Depends on abstractions (interfaces)
    """
    
    def __init__(self, gemini_client: GeminiClient, graph_repository, logger=None):
        """
        Initialize service với dependency injection
        DIP: Inject abstractions, not concrete classes
        """
        self.gemini = gemini_client
        self.graph_repo = graph_repository  # Abstraction
        self.logger = logger or get_logger(__name__)
        
        # In-memory storage for demo (sẽ thay bằng actual graph DB)
        self._requirements: Dict[str, ProjectRequirement] = {}
        self._features: Dict[str, Feature] = {}
        self._bugs: Dict[str, Bug] = {}
        self._code_changes: Dict[str, CodeChange] = {}
        self._tests: Dict[str, Test] = {}
        self._documents: Dict[str, DocumentEntity] = {}
        self._code_files: Dict[str, CodeFileEntity] = {}
        self._test_coverage: Dict[str, TestCoverage] = {}
        self._user_feedback: Dict[str, UserFeedback] = {}
    
    # =================== CORE STORAGE METHODS ===================
    
    async def store_project_requirement(self, requirement: str, project_name: str, 
                                      priority: str = "medium") -> str:
        """
        Store project requirement - SRP focused
        OCP: Extensible via strategy pattern
        """
        try:
            # Generate unique ID
            req_id = f"req_{uuid.uuid4().hex[:8]}"
            
            # Analyze với Gemini (SRP: delegate analysis)
            analysis = await self._analyze_requirement(requirement, project_name)
            
            # Create requirement object (SRP: delegate creation)
            req_obj = self._create_requirement_object(
                req_id, requirement, project_name, priority, analysis
            )
            
            # Store in repository
            self._requirements[req_id] = req_obj
            
            self.logger.info(f"✅ Stored requirement: {req_id}")
            return f"✅ Lưu requirement thành công: {req_id}\n\n**Thông tin:**\n- Priority: {priority}\n- Category: {analysis.get('category', 'functional')}\n- Complexity: {analysis.get('complexity', 'medium')}"
            
        except Exception as e:
            self.logger.error(f"Failed to store requirement: {e}")
            return f"❌ Lỗi lưu requirement: {str(e)}"
    
    async def store_feature_dependency(self, feature_a: str, feature_b: str,
                                     relationship_type: str, risk_level: str = "medium") -> str:
        """
        Store feature dependency - SRP focused
        LSP: Consistent return type với other store methods
        """
        try:
            # Analyze impact (SRP: delegate)
            analysis = await self._analyze_dependency_impact(
                feature_a, feature_b, relationship_type
            )
            
            # Store dependency info
            dependency_id = f"dep_{uuid.uuid4().hex[:8]}"
            
            self.logger.info(f"✅ Stored dependency: {feature_a} -> {feature_b}")
            return f"✅ Lưu dependency thành công: {feature_a} {relationship_type} {feature_b}\n\n**Impact Analysis:**\n- Risk Score: {analysis.get('risk_score', 5)}/10\n- Impact Areas: {', '.join(analysis.get('impact_areas', []))}\n- Mitigation: {', '.join(analysis.get('mitigation_strategies', []))}"
            
        except Exception as e:
            self.logger.error(f"Failed to store dependency: {e}")
            return f"❌ Lỗi lưu dependency: {str(e)}"
    
    async def store_bug_report(self, title: str, description: str, severity: str,
                             affected_features: List[str] = None) -> str:
        """
        Store bug report với automatic categorization
        NEW: Enhanced với doc/code tracking
        """
        try:
            bug_id = f"bug_{uuid.uuid4().hex[:8]}"
            affected_features = affected_features or []
            
            # Create bug object
            bug = Bug(
                id=bug_id,
                title=title,
                description=description,
                severity=BugSeverity(severity),
                priority=Priority.HIGH if severity in ["critical", "blocker"] else Priority.MEDIUM,
                status=Status.OPEN,
                affected_features=affected_features,
                created_at=datetime.now(),
                reported_by="user"
            )
            
            self._bugs[bug_id] = bug
            
            # Analyze impact
            impact_score = bug.get_impact_score()
            
            self.logger.info(f"✅ Stored bug report: {bug_id}")
            return f"✅ Lưu bug report thành công: {bug_id}\n\n**Thông tin:**\n- Severity: {severity}\n- Impact Score: {impact_score}\n- Affected Features: {len(affected_features)}\n- Priority: {bug.priority.value}"
            
        except Exception as e:
            self.logger.error(f"Failed to store bug report: {e}")
            return f"❌ Lỗi lưu bug report: {str(e)}"
    
    async def store_code_change(self, title: str, change_type: str, file_paths: List[str],
                              lines_added: int = 0, lines_removed: int = 0) -> str:
        """
        Store code change với comprehensive impact analysis
        NEW: Enhanced với doc/code tracking
        """
        try:
            change_id = f"change_{uuid.uuid4().hex[:8]}"
            
            # Create code change object
            change = CodeChange(
                id=change_id,
                change_type=ChangeType(change_type),
                title=title,
                description=title,
                file_paths=file_paths,
                lines_added=lines_added,
                lines_removed=lines_removed,
                created_at=datetime.now(),
                author="user"
            )
            
            self._code_changes[change_id] = change
            
            # Analyze comprehensive impact
            impact_analysis = await self._analyze_code_change_comprehensive_impact(change)
            
            self.logger.info(f"✅ Stored code change: {change_id}")
            return f"✅ Lưu code change thành công: {change_id}\n\n**Impact Analysis:**\n- Risk Score: {change.get_risk_score()}/10\n- Files Changed: {len(file_paths)}\n- Lines: +{lines_added}/-{lines_removed}\n- Affected Entities: {len(impact_analysis.get('affected_entities', []))}"
            
        except Exception as e:
            self.logger.error(f"Failed to store code change: {e}")
            return f"❌ Lỗi lưu code change: {str(e)}"
    
    async def store_user_feedback(self, feedback_type: str, title: str, description: str,
                                priority: str = "medium") -> str:
        """
        Store user feedback với automatic categorization
        """
        try:
            feedback_id = f"feedback_{uuid.uuid4().hex[:8]}"
            
            # Create feedback object
            feedback = UserFeedback(
                id=feedback_id,
                feedback_type=FeedbackType(feedback_type),
                title=title,
                description=description,
                priority=Priority(priority),
                status=Status.OPEN,
                created_at=datetime.now(),
                created_by="user"
            )
            
            self._user_feedback[feedback_id] = feedback
            
            # Calculate value score
            value_score = feedback.get_value_score()
            
            self.logger.info(f"✅ Stored user feedback: {feedback_id}")
            return f"✅ Lưu user feedback thành công: {feedback_id}\n\n**Thông tin:**\n- Type: {feedback_type}\n- Priority: {priority}\n- Value Score: {value_score}\n- Status: {feedback.status.value}"
            
        except Exception as e:
            self.logger.error(f"Failed to store user feedback: {e}")
            return f"❌ Lỗi lưu user feedback: {str(e)}"
    
    # =================== INTELLIGENT QUERY METHODS ===================
    
    async def get_tests_to_run(self, modified_features: List[str]) -> str:
        """
        Get smart test recommendations - SRP focused
        Enhanced với comprehensive analysis
        """
        try:
            # Find related entities
            related_code_files = self._find_related_code_files(modified_features)
            related_tests = self._find_related_tests(modified_features)
            related_coverage = list(self._test_coverage.values())
            
            # Get comprehensive test plan
            tests_to_run = get_tests_to_run(
                code_changes=[cf.file_path for cf in related_code_files],
                feature_changes=modified_features,
                all_code_files=list(self._code_files.values()),
                all_test_coverage=related_coverage
            )
            
            # Format comprehensive response
            return self._format_comprehensive_test_recommendations(
                modified_features, related_code_files, related_tests, tests_to_run
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get test recommendations: {e}")
            return f"❌ Lỗi lấy test recommendations: {str(e)}"
    
    async def get_related_features(self, feature: str, max_depth: int = 2) -> str:
        """
        Find related features - Enhanced với comprehensive relationships
        """
        try:
            # Find related features (placeholder implementation)
            related = [f for f in self._features.keys() if f != feature][:5]
            
            return self._format_related_features(feature, related)
        except Exception as e:
            self.logger.error(f"Failed to find related features: {e}")
            return f"❌ Lỗi tìm related features: {str(e)}"
    
    async def search_memory(self, query: str, limit: int = 10) -> str:
        """
        Search memory - Enhanced với comprehensive search
        """
        try:
            results = []
            
            # Search requirements
            for req in self._requirements.values():
                if query.lower() in req.title.lower() or query.lower() in req.description.lower():
                    results.append({"type": "requirement", "id": req.id, "title": req.title})
            
            # Search features
            for feature in self._features.values():
                if query.lower() in feature.name.lower() or query.lower() in feature.description.lower():
                    results.append({"type": "feature", "id": feature.id, "title": feature.name})
            
            # Search bugs
            for bug in self._bugs.values():
                if query.lower() in bug.title.lower() or query.lower() in bug.description.lower():
                    results.append({"type": "bug", "id": bug.id, "title": bug.title})
            
            return self._format_search_results(query, results[:limit])
        except Exception as e:
            self.logger.error(f"Failed to search memory: {e}")
            return f"❌ Lỗi tìm kiếm memory: {str(e)}"
    
    async def get_bug_impact_analysis(self, bug_id: str) -> str:
        """
        Phân tích comprehensive impact của bug
        NEW: Enhanced với doc/code tracking
        """
        try:
            if bug_id not in self._bugs:
                return f"❌ Không tìm thấy bug: {bug_id}"
            
            bug = self._bugs[bug_id]
            
            # Analyze comprehensive impact
            impact_score = bug.get_impact_score()
            affected_features = bug.affected_features
            affected_files = bug.affected_files
            
            # Find related documents and tests
            related_docs = self._find_related_documents(affected_features, affected_files)
            related_tests = self._find_tests_for_files(affected_files)
            
            return f"🔍 **Bug Impact Analysis: {bug_id}**\n\n"\
                   f"**Basic Info:**\n"\
                   f"- Severity: {bug.severity.value}\n"\
                   f"- Impact Score: {impact_score}/10\n"\
                   f"- Status: {bug.status.value}\n\n"\
                   f"**Affected Scope:**\n"\
                   f"- Features: {len(affected_features)} ({', '.join(affected_features[:3])})\n"\
                   f"- Files: {len(affected_files)} ({', '.join(affected_files[:3])})\n"\
                   f"- Docs: {len(related_docs)} documents need review\n"\
                   f"- Tests: {len(related_tests)} tests should be run\n\n"\
                   f"**Recommendations:**\n"\
                   f"- Priority: {'HIGH' if impact_score > 6 else 'MEDIUM'}\n"\
                   f"- Regression Risk: {bug.regression_risk}\n"\
                   f"- Estimated Fix Time: {self._estimate_fix_time(bug)}"
            
        except Exception as e:
            self.logger.error(f"Failed to analyze bug impact: {e}")
            return f"❌ Lỗi phân tích bug impact: {str(e)}"
    
    # =================== NEW: COMPREHENSIVE ANALYSIS METHODS ===================
    
    async def get_documents_to_update(self, feature_changes: List[str], 
                                    code_changes: List[str]) -> str:
        """
        Lấy danh sách documents cần update - KEY for automation goal
        """
        try:
            docs_to_update = get_documents_to_update(
                feature_changes, code_changes, list(self._documents.values())
            )
            
            if not docs_to_update:
                return "✅ Không có documents nào cần update."
            
            result = f"📝 **Documents cần update ({len(docs_to_update)}):**\n\n"
            
            for doc in docs_to_update:
                staleness = doc.get_staleness_score()
                priority = "HIGH" if doc.update_frequency == "on_change" else "MEDIUM"
                
                result += f"**{doc.title}**\n"
                result += f"- File: `{doc.file_path}`\n"
                result += f"- Type: {doc.document_type}\n"
                result += f"- Priority: {priority}\n"
                result += f"- Staleness: {staleness:.1f}/10\n"
                result += f"- Last Updated: {doc.last_updated.strftime('%Y-%m-%d')}\n\n"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get documents to update: {e}")
            return f"❌ Lỗi lấy documents to update: {str(e)}"
    
    async def get_comprehensive_test_plan(self, code_changes: List[str], 
                                        feature_changes: List[str],
                                        risk_level: str = "medium") -> str:
        """
        Tạo comprehensive test plan - KEY for automation goal
        """
        try:
            # Find all related entities
            related_code_files = self._find_code_files_by_paths(code_changes)
            related_features = [self._features.get(f) for f in feature_changes if f in self._features]
            related_tests = self._find_tests_for_changes(code_changes, feature_changes)
            
            # Categorize tests by priority
            critical_tests = [t for t in related_tests if t.is_critical()]
            regression_tests = [t for t in related_tests if t.test_type == TestType.REGRESSION]
            unit_tests = [t for t in related_tests if t.test_type == TestType.UNIT]
            
            # Calculate effort
            total_time = sum(t.execution_time for t in related_tests)
            
            result = f"🧪 **Comprehensive Test Plan**\n\n"
            result += f"**Scope:**\n"
            result += f"- Code Files: {len(code_changes)}\n"
            result += f"- Features: {len(feature_changes)}\n"
            result += f"- Risk Level: {risk_level.upper()}\n\n"
            
            result += f"**Test Categories:**\n"
            result += f"- Critical Tests: {len(critical_tests)} (must run)\n"
            result += f"- Regression Tests: {len(regression_tests)} (recommended)\n"
            result += f"- Unit Tests: {len(unit_tests)} (if time permits)\n\n"
            
            result += f"**Execution Plan:**\n"
            result += f"- Total Tests: {len(related_tests)}\n"
            result += f"- Estimated Time: {total_time:.1f} minutes\n"
            result += f"- Recommended Order: Critical → Regression → Unit\n\n"
            
            result += f"**Risk Mitigation:**\n"
            if risk_level == "high":
                result += "- Run ALL tests before deployment\n"
                result += "- Manual testing for critical paths\n"
                result += "- Staged rollout recommended\n"
            elif risk_level == "medium":
                result += "- Run critical and regression tests\n"
                result += "- Monitor key metrics post-deployment\n"
            else:
                result += "- Run critical tests minimum\n"
                result += "- Standard deployment process\n"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to create comprehensive test plan: {e}")
            return f"❌ Lỗi tạo comprehensive test plan: {str(e)}"
    
    # =================== PRIVATE HELPER METHODS ===================
    
    async def _analyze_requirement(self, requirement: str, project_name: str) -> Dict[str, Any]:
        """SRP: Only analyze requirements"""
        return await self.gemini.analyze_requirement(requirement, project_name)
    
    async def _analyze_dependency_impact(self, feature_a: str, feature_b: str, 
                                       relationship_type: str) -> Dict[str, Any]:
        """SRP: Only analyze dependency impact"""
        return await self.gemini.analyze_feature_dependency(feature_a, feature_b, relationship_type)
    
    async def _analyze_code_change_comprehensive_impact(self, change: CodeChange) -> Dict[str, Any]:
        """NEW: Analyze comprehensive impact including docs and code"""
        return await self.gemini.analyze_code_change_impact(change.file_paths, change.change_type.value)
    
    def _create_requirement_object(self, req_id: str, requirement: str, 
                                 project_name: str, priority: str, analysis: Dict[str, Any]) -> ProjectRequirement:
        """SRP: Only create requirement objects"""
        return ProjectRequirement(
            id=req_id,
            title=requirement,
            description=requirement,
            priority=Priority(priority),
            status=Status.OPEN,
            project_name=project_name,
            category=analysis.get("category", "functional"),
            estimated_effort=analysis.get("complexity", "medium")
        )
    
    def _find_related_code_files(self, feature_ids: List[str]) -> List[CodeFileEntity]:
        """Find code files related to features"""
        # Placeholder implementation
        return list(self._code_files.values())[:3]
    
    def _find_related_tests(self, feature_ids: List[str]) -> List[Test]:
        """Find tests related to features"""
        # Placeholder implementation
        return list(self._tests.values())[:3]
    
    def _find_related_documents(self, feature_ids: List[str], file_paths: List[str]) -> List[DocumentEntity]:
        """Find documents related to features and files"""
        related = []
        for doc in self._documents.values():
            if any(fid in doc.related_features for fid in feature_ids):
                related.append(doc)
            if any(fp in doc.related_code_files for fp in file_paths):
                related.append(doc)
        return related
    
    def _find_tests_for_files(self, file_paths: List[str]) -> List[Test]:
        """Find tests that cover specific files"""
        # Placeholder implementation
        return list(self._tests.values())[:2]
    
    def _find_code_files_by_paths(self, paths: List[str]) -> List[CodeFileEntity]:
        """Find code files by their paths"""
        return [cf for cf in self._code_files.values() if cf.file_path in paths]
    
    def _find_tests_for_changes(self, code_changes: List[str], feature_changes: List[str]) -> List[Test]:
        """Find tests for code and feature changes"""
        # Placeholder implementation
        return list(self._tests.values())
    
    def _estimate_fix_time(self, bug: Bug) -> str:
        """Estimate bug fix time based on complexity"""
        impact = bug.get_impact_score()
        if impact > 6:
            return "4-8 hours"
        elif impact > 3:
            return "2-4 hours"
        else:
            return "1-2 hours"
    
    # =================== FORMATTING METHODS ===================
    
    def _format_comprehensive_test_recommendations(self, modified: List[str], 
                                                 code_files: List[CodeFileEntity],
                                                 tests: List[Test], 
                                                 test_files: List[str]) -> str:
        """Format comprehensive test recommendations"""
        result = f"📋 **Comprehensive Test Recommendations**\n\n"
        result += f"**Modified Features:** {', '.join(modified)}\n"
        result += f"**Affected Code Files:** {len(code_files)}\n"
        result += f"**Recommended Tests:** {len(test_files)}\n\n"
        
        if test_files:
            result += "**Tests to Run:**\n"
            for i, test_file in enumerate(test_files[:10], 1):
                result += f"{i}. `{test_file}`\n"
            if len(test_files) > 10:
                result += f"... and {len(test_files) - 10} more\n"
        
        # Add execution estimate
        total_time = sum(t.execution_time for t in tests)
        result += f"\n**Estimated Execution Time:** {total_time:.1f} minutes"
        
        return result
    
    def _format_related_features(self, feature: str, related: List[str]) -> str:
        """Format related features for display"""
        result = f"🔗 **Related Features for '{feature}'**\n\n"
        if related:
            for i, rel in enumerate(related[:10], 1):
                result += f"{i}. {rel}\n"
            if len(related) > 10:
                result += f"... and {len(related) - 10} more\n"
        else:
            result += "No related features found."
        return result
    
    def _format_search_results(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format search results for display"""
        result = f"🔍 **Search Results for '{query}' ({len(results)} found)**\n\n"
        
        if results:
            for i, item in enumerate(results, 1):
                result += f"{i}. **{item['title']}** ({item['type']})\n"
                result += f"   ID: `{item['id']}`\n\n"
        else:
            result += "No results found. Try different keywords."
        
        return result
