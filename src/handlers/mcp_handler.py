"""
MCP Protocol Handlers - Clean Architecture
Mục đích: Handle MCP protocol requests với clean separation of concerns
"""

import asyncio
from typing import Dict, Any, List, Optional
from mcp.server import Server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    CallToolRequest, CallToolResult, ListToolsRequest, ListToolsResult
)
from ..tools.tool_factory import MCPToolFactory
from ..tools.base_mcp_tool import MCPToolRegistry, MCPToolExecutor
from ..utils.logger import get_logger


class GraphitiMCPServer:
    """
    MCP Server implementation cho Graphiti Memory System
    SRP: Chỉ lo việc handle MCP protocol
    DIP: Depends on tool abstractions
    """
    
    def __init__(self, tool_registry: MCPToolRegistry, tool_executor: MCPToolExecutor):
        """Initialize MCP server với tool registry và executor"""
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor
        self.logger = get_logger(__name__)
        
        # Create MCP server instance
        self.server = Server("cursor-graphiti-memory")
        
        # Register MCP handlers
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """
        Register MCP protocol handlers
        Template method pattern
        """
        # Register tool listing handler
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return await self._handle_list_tools()
        
        # Register tool execution handler
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            return await self._handle_call_tool(name, arguments)
        
        self.logger.info("Registered MCP protocol handlers")
    
    async def _handle_list_tools(self) -> List[Tool]:
        """
        Handle list tools request
        SRP: Chỉ lo việc list tools
        """
        try:
            tools = []
            tool_schemas = self.tool_registry.get_tool_schemas()
            
            for tool_name, schema in tool_schemas.items():
                tool = Tool(
                    name=schema["name"],
                    description=schema["description"],
                    inputSchema=schema["inputSchema"]
                )
                tools.append(tool)
            
            self.logger.info(f"Listed {len(tools)} tools")
            return tools
            
        except Exception as e:
            self.logger.error(f"Error listing tools: {e}", exc_info=True)
            return []
    
    async def _handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Handle tool execution request
        SRP: Chỉ lo việc execute tools
        """
        try:
            # Execute tool through executor
            result = await self.tool_executor.execute_tool(name, arguments)
            
            # Return as TextContent
            return [TextContent(
                type="text",
                text=result
            )]
            
        except Exception as e:
            error_msg = f"❌ Error executing tool '{name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            
            return [TextContent(
                type="text",
                text=error_msg
            )]
    
    def get_server(self) -> Server:
        """Get MCP server instance"""
        return self.server
    
    async def run_stdio(self) -> None:
        """
        Run MCP server với stdio transport
        """
        from mcp.server.stdio import stdio_server
        
        self.logger.info("Starting MCP server with stdio transport")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


class MCPServerBootstrap:
    """
    Bootstrap class cho MCP server
    SRP: Chỉ lo việc bootstrap và orchestrate
    DIP: Orchestrates dependencies without tight coupling
    """
    
    def __init__(self):
        """Initialize bootstrap"""
        self.logger = get_logger(__name__)
        self.tool_registry: Optional[MCPToolRegistry] = None
        self.tool_executor: Optional[MCPToolExecutor] = None
        self.mcp_server: Optional[GraphitiMCPServer] = None
    
    async def initialize(self) -> None:
        """
        Initialize all dependencies - DIP compliant
        Template method pattern
        """
        try:
            self.logger.info("Initializing MCP Server Bootstrap...")
            
            # Create services (DIP: inject dependencies)
            gemini_client = self._create_gemini_client()
            graph_repository = self._create_graph_repository()
            
            # Import services here to avoid circular imports
            from ..services.memory_service import MemoryService
            from ..services.nlp_service import NLPService
            
            memory_service = MemoryService(
                gemini_client=gemini_client,
                graph_repository=graph_repository,
                logger=self.logger
            )
            
            nlp_service = NLPService(gemini_client, self.logger)
            
            # Create và register tools (Factory pattern)
            tool_factory = MCPToolFactory(memory_service, nlp_service)
            self.tool_registry = tool_factory.create_and_register_all_tools()
            self.tool_executor = tool_factory.get_executor()
            
            # Create MCP server
            self.mcp_server = GraphitiMCPServer(self.tool_registry, self.tool_executor)
            
            self.logger.info("✅ MCP Server initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP server: {e}", exc_info=True)
            raise
    
    def _create_gemini_client(self):
        """
        Factory method cho GeminiClient
        Factory pattern - creates with proper configuration
        """
        from ..models.gemini_client import GeminiClient
        from ..utils.config import get_config
        
        try:
            config = get_config()
            return GeminiClient(
                api_key=config.gemini.api_key,
                model=config.gemini.model
            )
        except Exception as e:
            self.logger.warning(f"Failed to create Gemini client: {e}")
            # Return mock client for development
            return self._create_mock_gemini_client()
    
    def _create_mock_gemini_client(self):
        """
        Create mock Gemini client for development/testing
        """
        class MockGeminiClient:
            async def analyze_requirement(self, requirement: str, project_name: str):
                return {"category": "functional", "complexity": "medium"}
            
            async def analyze_feature_dependency(self, feature_a: str, feature_b: str, relationship_type: str):
                return {"impact_areas": ["testing"], "risk_score": 5, "mitigation_strategies": ["thorough_testing"]}
            
            async def analyze_code_change_impact(self, file_paths: list, change_type: str):
                return {"affected_features": [], "required_tests": [], "risk_level": "medium"}
            
            async def process_natural_language(self, message: str):
                return f"Mock response for: {message}"
        
        self.logger.info("Using mock Gemini client for development")
        return MockGeminiClient()
    
    def _create_graph_repository(self):
        """
        Factory method cho GraphRepository
        Factory pattern - placeholder for future implementation
        """
        # Placeholder - sẽ implement với actual Graphiti
        class MockGraphRepository:
            async def store_requirement(self, req_obj, analysis):
                return "mock_stored"
            
            async def store_dependency(self, dependency, analysis):
                return "mock_dependency_id"
        
        self.logger.info("Using mock graph repository for development")
        return MockGraphRepository()
    
    async def run(self) -> None:
        """
        Run MCP server
        SRP: ONLY handle server execution
        """
        if not self.mcp_server:
            raise RuntimeError("MCP server not initialized. Call initialize() first.")
        
        try:
            print("🚀 Cursor Graphiti MCP Server starting...")
            print(f"🔧 Registered {len(self.tool_registry.get_all_tools())} tools")
            print("🔗 Ready for Cursor IDE connection")
            print("\n📝 Available tools:")
            
            # List available tools
            for i, tool_name in enumerate(self.tool_registry.list_tool_names(), 1):
                tool = self.tool_registry.get_tool(tool_name)
                print(f"  {i:2d}. {tool_name}: {tool.description[:60]}...")
            
            print("\n✅ Server ready! Connect from Cursor IDE using MCP protocol.\n")
            
            # Run MCP server with stdio transport
            await self.mcp_server.run_stdio()
            
        except KeyboardInterrupt:
            self.logger.info("Server stopped by user")
            print("\n🛴 Server stopped gracefully.")
        except Exception as e:
            self.logger.error(f"Server error: {e}", exc_info=True)
            print(f"\n❌ Server error: {e}")
            raise
    
    def get_tool_registry(self) -> MCPToolRegistry:
        """Get tool registry for external access"""
        if not self.tool_registry:
            raise RuntimeError("Tool registry not initialized")
        return self.tool_registry
    
    def get_tool_executor(self) -> MCPToolExecutor:
        """Get tool executor for external access"""
        if not self.tool_executor:
            raise RuntimeError("Tool executor not initialized")
        return self.tool_executor
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get server information for debugging
        """
        if not self.tool_registry:
            return {"status": "not_initialized"}
        
        tools = self.tool_registry.get_all_tools()
        return {
            "status": "initialized",
            "total_tools": len(tools),
            "tool_names": list(tools.keys()),
            "server_name": "cursor-graphiti-memory",
            "version": "1.0.0"
        }
