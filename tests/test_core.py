"""Tests for Audit Provenance Tracer."""
import unittest
from mcp_audit_provenance_tracer.core import AuditProvenanceTracer

class TestAuditProvenanceTracer(unittest.TestCase):
    def test_chain_integrity_and_tampering(self):
        tracer = AuditProvenanceTracer()
        tracer.record_event("action1", {"param": 1})
        tracer.record_event("action2", {"param": 2})
        self.assertTrue(tracer.verify_integrity())

        # Tamper with block
        tracer.chain[1].payload["param"] = 999
        self.assertFalse(tracer.verify_integrity())
