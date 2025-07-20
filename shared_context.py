from iointel import AsyncMemory
from typing import Dict, Any, List
import json
import asyncio

class SharedContextManager:
    def __init__(self):
        self.memory = AsyncMemory()
        self.context_store: Dict[str, Any] = {}
    
    async def store_context(self, context_id: str, data: Dict[str, Any]):
        """Store context data"""
        self.context_store[context_id] = data
        await self.memory.store_run_history(context_id, data)
    
    async def get_context(self, context_id: str) -> Dict[str, Any]:
        """Retrieve context data"""
        if context_id in self.context_store:
            return self.context_store[context_id]
        
        # Try to load from memory
        try:
            history = await self.memory.get_message_history(context_id, 100)
            return history[-1] if history else {}
        except:
            return {}
    
    async def share_between_agents(self, from_agent: str, to_agent: str, data: Dict[str, Any]):
        """Share data between agents"""
        context_id = f"{from_agent}_to_{to_agent}"
        await self.store_context(context_id, {
            "from": from_agent,
            "to": to_agent,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        })