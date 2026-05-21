"""
Agent 基类定义

所有辩论团队的 Agent 都继承自这些基类。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class AgentMessage(BaseModel):
    """Agent 消息模型"""
    
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    role: str
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentResponse(BaseModel):
    """Agent 响应模型"""
    
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    decision: str
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    alternatives: List[str] = []
    risks: List[str] = []
    suggestions: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DebateContext(BaseModel):
    """辩论上下文"""
    
    topic: str
    description: str = ""
    constraints: List[str] = []
    requirements: List[str] = []
    background: Dict[str, Any] = {}
    history: List[AgentMessage] = []


class BaseAgent(ABC):
    """
    Agent 基类
    
    所有辩论团队的 Agent 都继承自这个基类。
    提供基本的接口定义和通用功能。
    """
    
    def __init__(
        self,
        agent_id: str,
        role: str,
        description: str = "",
        expertise: List[str] = []
    ):
        """
        初始化 Agent
        
        Args:
            agent_id: Agent 唯一标识
            role: Agent 角色名称
            description: Agent 描述
            expertise: Agent 专长领域
        """
        self.agent_id = agent_id
        self.role = role
        self.description = description
        self.expertise = expertise
        self._history: List[AgentMessage] = []
    
    @abstractmethod
    async def analyze(self, context: DebateContext) -> AgentResponse:
        """
        分析问题
        
        Args:
            context: 辩论上下文
            
        Returns:
            AgentResponse: 分析结果
        """
        pass
    
    @abstractmethod
    async def debate(
        self,
        context: DebateContext,
        messages: List[AgentMessage]
    ) -> AgentResponse:
        """
        参与辩论
        
        Args:
            context: 辩论上下文
            messages: 其他 Agent 的消息
            
        Returns:
            AgentResponse: 辩论结果
        """
        pass
    
    @abstractmethod
    async def vote(
        self,
        context: DebateContext,
        proposals: List[AgentResponse]
    ) -> AgentMessage:
        """
        投票
        
        Args:
            context: 辩论上下文
            proposals: 各 Agent 的提案
            
        Returns:
            AgentMessage: 投票结果
        """
        pass
    
    def add_to_history(self, message: AgentMessage):
        """添加到历史记录"""
        self._history.append(message)
    
    def get_history(self) -> List[AgentMessage]:
        """获取历史记录"""
        return self._history.copy()
    
    def clear_history(self):
        """清空历史记录"""
        self._history.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "description": self.description,
            "expertise": self.expertise
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.agent_id}, role={self.role})>"


class SimpleAgent(BaseAgent):
    """
    简单 Agent 实现
    
    用于测试和演示，实际使用时需要继承并实现具体逻辑。
    """
    
    async def analyze(self, context: DebateContext) -> AgentResponse:
        """简单分析实现"""
        return AgentResponse(
            agent_id=self.agent_id,
            decision="需要更多信息",
            reasoning=f"作为{self.role}，我需要更多信息来分析这个问题",
            confidence=0.5
        )
    
    async def debate(
        self,
        context: DebateContext,
        messages: List[AgentMessage]
    ) -> AgentResponse:
        """简单辩论实现"""
        # 分析其他 Agent 的观点
        other_views = [m.content for m in messages if m.agent_id != self.agent_id]
        
        return AgentResponse(
            agent_id=self.agent_id,
            decision="需要更多信息",
            reasoning=f"作为{self.role}，我考虑了其他人的观点，但仍需要更多信息",
            confidence=0.5
        )
    
    async def vote(
        self,
        context: DebateContext,
        proposals: List[AgentResponse]
    ) -> AgentMessage:
        """简单投票实现"""
        # 选择置信度最高的提案
        best_proposal = max(proposals, key=lambda p: p.confidence)
        
        return AgentMessage(
            agent_id=self.agent_id,
            role=self.role,
            content=f"我投票支持: {best_proposal.decision}",
            confidence=best_proposal.confidence
        )
