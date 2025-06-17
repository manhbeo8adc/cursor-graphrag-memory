"""
Complete Data Models cho GraphRAG Memory System - Hỗ trợ mục tiêu tự động hóa hoàn chỉnh
Mục đích: Tự động track docs + code + features + bugs, comprehensive impact analysis, precise recommendations

Core Entities (11):
- ProjectRequirement, Feature, Bug, CodeChange, Test, TestResult, UserFeedback
- DocumentEntity, CodeFileEntity, TestCoverage, EntityRelationship

Enhanced Relationships (17):
- Original: depends_on, conflicts_with, enhances, blocks, related_to, implements, tests, fixes, caused_by
- New: documents, described_by, covers, covered_by, imports, imported_by, references, referenced_by

Capabilities: Change Detection → Doc/Code Impact Analysis → Test Recommendations → Auto Updates → Quality Assurance
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional


# =================== ENUMS ===================

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class BugSeverity(Enum):
    TRIVIAL = "trivial"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"
    BLOCKER = "blocker"

class ChangeType(Enum):
    NEW_FEATURE = "new_feature"
    ENHANCEMENT = "enhancement"
    BUG_FIX = "bug_fix"
    REFACTOR = "refactor"
    PERFORMANCE = "performance"
    SECURITY = "security"

class RelationshipType(Enum):
    DEPENDS_ON = "depends_on"
    CONFLICTS_WITH = "conflicts_with"
    ENHANCES = "enhances"
    BLOCKS = "blocks"
    RELATED_TO = "related_to"
    IMPLEMENTS = "implements"
    TESTS = "tests"
    FIXES = "fixes"
    CAUSED_BY = "caused_by"

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    REGRESSION = "regression"

class FeedbackType(Enum):
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    IMPROVEMENT = "improvement"
    QUESTION = "question"
    COMPLIMENT = "compliment"


# =================== CORE ENTITIES ===================

@dataclass
class ProjectRequirement:
    """Core project requirements entity"""
    id: str
    title: str
    description: str
    priority: Priority
    status: Status
    project_name: str
    category: str = "functional"
    business_value: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    estimated_effort: str = "medium"
    actual_effort: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    
    def get_complexity_score(self) -> int:
        """Calculate complexity based on criteria count và dependencies"""
        base_score = len(self.acceptance_criteria)
        priority_multiplier = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return base_score * priority_multiplier.get(self.priority.value, 2)


@dataclass
class Feature:
    """Software feature entity"""
    id: str
    name: str
    description: str
    status: Status
    feature_type: str = "functional"
    module: str = ""
    file_paths: List[str] = field(default_factory=list)
    api_endpoints: List[str] = field(default_factory=list)
    database_tables: List[str] = field(default_factory=list)
    external_dependencies: List[str] = field(default_factory=list)
    performance_requirements: Dict[str, Any] = field(default_factory=dict)
    security_considerations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def get_complexity_score(self) -> int:
        """Calculate feature complexity based on dependencies và scope"""
        file_score = len(self.file_paths)
        api_score = len(self.api_endpoints) * 2
        db_score = len(self.database_tables) * 3
        ext_score = len(self.external_dependencies) * 2
        return file_score + api_score + db_score + ext_score


@dataclass
class Bug:
    """Bug tracking entity"""
    id: str
    title: str
    description: str
    severity: BugSeverity
    priority: Priority
    status: Status
    bug_type: str = "functional"
    affected_features: List[str] = field(default_factory=list)
    affected_files: List[str] = field(default_factory=list)
    steps_to_reproduce: List[str] = field(default_factory=list)
    expected_behavior: str = ""
    actual_behavior: str = ""
    environment: Dict[str, str] = field(default_factory=dict)
    error_logs: List[str] = field(default_factory=list)
    root_cause: str = ""
    fix_description: str = ""
    regression_risk: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    reported_by: str = ""
    assigned_to: str = ""
    
    def get_impact_score(self) -> int:
        """Calculate bug impact based on severity và affected scope"""
        severity_scores = {"trivial": 1, "minor": 2, "major": 4, "critical": 6, "blocker": 8}
        base_score = severity_scores.get(self.severity.value, 2)
        affected_multiplier = max(1, len(self.affected_features))
        return base_score * affected_multiplier


@dataclass
class CodeChange:
    """Code change tracking entity"""
    id: str
    change_type: ChangeType
    title: str
    description: str
    file_paths: List[str] = field(default_factory=list)
    lines_added: int = 0
    lines_removed: int = 0
    complexity_delta: int = 0
    performance_impact: str = "none"
    security_impact: str = "none"
    breaking_changes: bool = False
    rollback_plan: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    author: str = ""
    reviewer: str = ""
    
    def get_risk_score(self) -> int:
        """Calculate change risk based on size và impact"""
        size_score = (self.lines_added + self.lines_removed) // 10
        complexity_score = abs(self.complexity_delta)
        breaking_score = 10 if self.breaking_changes else 0
        return min(10, size_score + complexity_score + breaking_score)


@dataclass
class Test:
    """Test case entity"""
    id: str
    name: str
    description: str
    test_type: TestType
    status: Status
    file_path: str = ""
    test_suite: str = ""
    execution_time: float = 0.0
    last_run_at: Optional[datetime] = None
    last_result: str = "unknown"
    flaky_score: float = 0.0
    coverage_percentage: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    data_requirements: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def is_critical(self) -> bool:
        """Check if test is critical based on type và coverage"""
        critical_types = [TestType.INTEGRATION, TestType.E2E, TestType.SECURITY]
        return self.test_type in critical_types or self.coverage_percentage > 80


@dataclass
class TestResult:
    """Test execution result entity"""
    id: str
    test_id: str
    execution_date: datetime
    result: str  # passed, failed, skipped, error
    execution_time: float
    error_message: str = ""
    stack_trace: str = ""
    environment: Dict[str, str] = field(default_factory=dict)
    code_version: str = ""
    data_snapshot: str = ""
    
    def is_failure(self) -> bool:
        return self.result in ["failed", "error"]


@dataclass
class UserFeedback:
    """User feedback entity"""
    id: str
    feedback_type: FeedbackType
    title: str
    description: str
    priority: Priority
    status: Status
    related_features: List[str] = field(default_factory=list)
    related_bugs: List[str] = field(default_factory=list)
    user_type: str = "end_user"  # end_user, developer, stakeholder
    business_impact: str = ""
    technical_feasibility: str = ""
    effort_estimate: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    
    def get_value_score(self) -> int:
        """Calculate feedback value based on type và business impact"""
        type_scores = {
            "bug_report": 5,
            "feature_request": 3,
            "improvement": 2,
            "question": 1,
            "compliment": 1
        }
        base_score = type_scores.get(self.feedback_type.value, 1)
        impact_multiplier = len(self.related_features) + len(self.related_bugs)
        return base_score * max(1, impact_multiplier)


# =================== DOCUMENTATION & CODE ENTITIES ===================

@dataclass
class DocumentEntity:
    """Documentation entity - crucial for auto-updates"""
    id: str
    title: str
    file_path: str
    document_type: str  # README, API_DOC, USER_GUIDE, TECHNICAL_SPEC, CHANGELOG
    content_summary: str = ""
    related_features: List[str] = field(default_factory=list)
    related_code_files: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    update_frequency: str = "on_change"  # on_change, weekly, monthly
    maintainer: str = ""
    review_required: bool = True
    template_used: str = ""
    
    def needs_update_for_feature(self, feature_id: str) -> bool:
        """Check if document needs update when feature changes"""
        return feature_id in self.related_features
    
    def get_staleness_score(self) -> float:
        """Calculate how stale the document is"""
        days_since_update = (datetime.now() - self.last_updated).days
        if self.update_frequency == "on_change":
            return min(10.0, days_since_update / 7.0)  # Stale after 1 week
        elif self.update_frequency == "weekly":
            return min(10.0, days_since_update / 7.0)
        else:  # monthly
            return min(10.0, days_since_update / 30.0)


@dataclass
class CodeFileEntity:
    """Code file entity - crucial for impact analysis"""
    id: str
    file_path: str
    file_type: str  # SOURCE, TEST, CONFIG, SCRIPT, SCHEMA
    language: str = "python"
    module_name: str = ""
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Other files this depends on
    dependents: List[str] = field(default_factory=list)   # Files that depend on this
    test_files: List[str] = field(default_factory=list)   # Tests that cover this file
    documentation_files: List[str] = field(default_factory=list)  # Docs that describe this
    complexity_score: int = 0
    lines_of_code: int = 0
    test_coverage: float = 0.0
    last_modified: datetime = field(default_factory=datetime.now)
    last_tested: Optional[datetime] = None
    
    def get_impact_score(self) -> int:
        """Calculate impact score based on dependencies"""
        dependency_score = len(self.dependents) * 2  # Files that depend on this
        complexity_factor = min(5, self.complexity_score // 10)
        return dependency_score + complexity_factor
    
    def needs_testing(self) -> bool:
        """Check if file needs testing based on changes"""
        if not self.last_tested:
            return True
        return self.last_modified > self.last_tested


@dataclass
class TestCoverage:
    """Test coverage mapping entity"""
    id: str
    test_file: str
    covered_files: List[str] = field(default_factory=list)
    covered_functions: List[str] = field(default_factory=list)
    covered_features: List[str] = field(default_factory=list)
    coverage_percentage: float = 0.0
    test_types: List[TestType] = field(default_factory=list)
    execution_time: float = 0.0
    last_run: Optional[datetime] = None
    success_rate: float = 100.0
    
    def covers_file(self, file_path: str) -> bool:
        """Check if this test covers a specific file"""
        return file_path in self.covered_files
    
    def covers_feature(self, feature_id: str) -> bool:
        """Check if this test covers a specific feature"""
        return feature_id in self.covered_features


# =================== RELATIONSHIP ENTITIES ===================

@dataclass
class EntityRelationship:
    """Generic relationship between any two entities"""
    id: str
    source_entity_type: str
    source_entity_id: str
    target_entity_type: str
    target_entity_id: str
    relationship_type: RelationshipType
    strength: float = 1.0  # 0.0 to 1.0
    confidence: float = 1.0  # 0.0 to 1.0
    bidirectional: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    
    def get_weight(self) -> float:
        """Calculate relationship weight for graph algorithms"""
        return self.strength * self.confidence


@dataclass
class ImpactAnalysis:
    """Impact analysis result entity"""
    id: str
    source_change_id: str
    source_change_type: str
    affected_entities: List[Dict[str, Any]] = field(default_factory=list)
    risk_level: str = "medium"
    recommended_tests: List[str] = field(default_factory=list)
    estimated_effort: str = ""
    confidence_score: float = 0.8
    analysis_date: datetime = field(default_factory=datetime.now)
    
    def get_total_impact_score(self) -> int:
        """Calculate total impact score"""
        return len(self.affected_entities) * len(self.recommended_tests)


# =================== ENHANCED RELATIONSHIP TYPES ===================

class ExtendedRelationshipType(Enum):
    # Original relationships
    DEPENDS_ON = "depends_on"
    CONFLICTS_WITH = "conflicts_with"
    ENHANCES = "enhances"
    BLOCKS = "blocks"
    RELATED_TO = "related_to"
    IMPLEMENTS = "implements"
    TESTS = "tests"
    FIXES = "fixes"
    CAUSED_BY = "caused_by"
    
    # New relationships for docs and code
    DOCUMENTS = "documents"           # Doc documents Feature/Code
    DESCRIBED_BY = "described_by"     # Feature described by Doc
    COVERS = "covers"                 # Test covers Code/Feature
    COVERED_BY = "covered_by"         # Code covered by Test
    IMPORTS = "imports"               # Code imports Code
    IMPORTED_BY = "imported_by"       # Code imported by Code
    REFERENCES = "references"         # Doc references Code/Feature
    REFERENCED_BY = "referenced_by"   # Code/Feature referenced by Doc


# =================== HELPER FUNCTIONS ===================

def create_relationship(source_type: str, source_id: str, 
                       target_type: str, target_id: str,
                       rel_type: RelationshipType,
                       strength: float = 1.0) -> EntityRelationship:
    """Helper function to create relationships"""
    return EntityRelationship(
        id=f"{source_type}_{source_id}_{rel_type.value}_{target_type}_{target_id}",
        source_entity_type=source_type,
        source_entity_id=source_id,
        target_entity_type=target_type,
        target_entity_id=target_id,
        relationship_type=rel_type,
        strength=strength
    )


def create_doc_code_relationship(doc_id: str, code_file_id: str, 
                               relationship_type: ExtendedRelationshipType) -> EntityRelationship:
    """Helper to create document-code relationships"""
    return EntityRelationship(
        id=f"doc_{doc_id}_{relationship_type.value}_code_{code_file_id}",
        source_entity_type="document",
        source_entity_id=doc_id,
        target_entity_type="code_file",
        target_entity_id=code_file_id,
        relationship_type=relationship_type,
        strength=1.0,
        metadata={"auto_update": True}
    )


def create_test_coverage_relationship(test_id: str, target_id: str, 
                                    target_type: str) -> EntityRelationship:
    """Helper to create test coverage relationships"""
    return EntityRelationship(
        id=f"test_{test_id}_covers_{target_type}_{target_id}",
        source_entity_type="test",
        source_entity_id=test_id,
        target_entity_type=target_type,
        target_entity_id=target_id,
        relationship_type=ExtendedRelationshipType.COVERS,
        strength=1.0,
        metadata={"coverage_type": "automated"}
    )


def calculate_comprehensive_change_impact(change: CodeChange, 
                                        related_features: List[Feature],
                                        related_tests: List[Test],
                                        related_docs: List[DocumentEntity],
                                        related_code_files: List[CodeFileEntity]) -> ImpactAnalysis:
    """Calculate comprehensive impact including docs and code files"""
    affected_entities = []
    
    # Add affected features
    for feature in related_features:
        affected_entities.append({
            "type": "feature",
            "id": feature.id,
            "name": feature.name,
            "impact_level": "high" if any(path in change.file_paths for path in feature.file_paths) else "medium",
            "action_required": "update_implementation"
        })
    
    # Add affected documents - CRUCIAL for auto-updates
    for doc in related_docs:
        if doc.needs_update_for_feature(change.id):
            affected_entities.append({
                "type": "document",
                "id": doc.id,
                "name": doc.title,
                "file_path": doc.file_path,
                "impact_level": "high" if doc.update_frequency == "on_change" else "medium",
                "action_required": "update_documentation",
                "staleness_score": doc.get_staleness_score()
            })
    
    # Add affected code files - CRUCIAL for dependency tracking
    for code_file in related_code_files:
        if code_file.needs_testing():
            affected_entities.append({
                "type": "code_file",
                "id": code_file.id,
                "name": code_file.file_path,
                "impact_level": "high" if code_file.get_impact_score() > 5 else "medium",
                "action_required": "run_tests",
                "test_files": code_file.test_files,
                "dependencies": code_file.dependencies
            })
    
    # Add recommended tests - Enhanced with coverage info
    recommended_tests = []
    for test in related_tests:
        if test.is_critical():
            recommended_tests.append({
                "test_id": test.id,
                "test_file": test.file_path,
                "priority": "high" if test.test_type in [TestType.INTEGRATION, TestType.E2E] else "medium",
                "estimated_time": test.execution_time
            })
    
    # Calculate comprehensive risk level
    base_risk = change.get_risk_score()
    doc_risk = len([e for e in affected_entities if e["type"] == "document"])
    code_risk = len([e for e in affected_entities if e["type"] == "code_file"]) * 2
    total_risk = base_risk + doc_risk + code_risk
    
    risk_level = "critical" if total_risk > 15 else "high" if total_risk > 10 else "medium" if total_risk > 5 else "low"
    
    return ImpactAnalysis(
        id=f"impact_{change.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        source_change_id=change.id,
        source_change_type=change.change_type.value,
        affected_entities=affected_entities,
        risk_level=risk_level,
        recommended_tests=[t["test_id"] for t in recommended_tests],
        estimated_effort=f"{len(affected_entities) * 1.5} hours",
        confidence_score=0.9,
        analysis_date=datetime.now()
    )


def get_documents_to_update(feature_changes: List[str], 
                          code_changes: List[str],
                          all_docs: List[DocumentEntity]) -> List[DocumentEntity]:
    """Get documents that need updating based on changes"""
    docs_to_update = []
    
    for doc in all_docs:
        # Check if any changed features are related to this doc
        if any(feature_id in doc.related_features for feature_id in feature_changes):
            docs_to_update.append(doc)
        
        # Check if any changed code files are related to this doc
        if any(code_file in doc.related_code_files for code_file in code_changes):
            docs_to_update.append(doc)
    
    return docs_to_update


def get_tests_to_run(code_changes: List[str],
                    feature_changes: List[str],
                    all_code_files: List[CodeFileEntity],
                    all_test_coverage: List[TestCoverage]) -> List[str]:
    """Get comprehensive list of tests to run based on changes"""
    tests_to_run = set()
    
    # Get tests for changed code files
    for code_file in all_code_files:
        if code_file.file_path in code_changes and code_file.needs_testing():
            tests_to_run.update(code_file.test_files)
    
    # Get tests that cover changed features
    for coverage in all_test_coverage:
        if any(feature_id in coverage.covered_features for feature_id in feature_changes):
            tests_to_run.add(coverage.test_file)
        
        if any(file_path in coverage.covered_files for file_path in code_changes):
            tests_to_run.add(coverage.test_file)
    
    return list(tests_to_run)
