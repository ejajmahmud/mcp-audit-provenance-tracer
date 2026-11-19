"""Core Audit Provenance Tracer."""
from typing import Dict, List, Any, Optional
import hashlib
import json
import time

class AuditBlock:
    def __init__(self, index: int, prev_hash: str, tool_name: str, payload: Dict[str, Any], timestamp: Optional[float] = None):
        self.index = index
        self.prev_hash = prev_hash
        self.tool_name = tool_name
        self.payload = payload
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        data = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "tool": self.tool_name,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
        raw = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

class AuditProvenanceTracer:
    def __init__(self):
        self.chain: List[AuditBlock] = []
        # Genesis block
        genesis = AuditBlock(0, "0" * 64, "GENESIS", {"status": "initialized"}, timestamp=0.0)
        self.chain.append(genesis)

    def record_event(self, tool_name: str, payload: Dict[str, Any]) -> AuditBlock:
        prev = self.chain[-1]
        block = AuditBlock(index=prev.index + 1, prev_hash=prev.hash, tool_name=tool_name, payload=payload)
        self.chain.append(block)
        return block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.prev_hash != prev.hash:
                return False
            if curr.hash != curr.compute_hash():
                return False
        return True
