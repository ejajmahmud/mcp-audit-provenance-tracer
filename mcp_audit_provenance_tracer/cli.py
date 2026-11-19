"""CLI for Audit Provenance Tracer."""
import argparse
from .core import AuditProvenanceTracer

def main():
    parser = argparse.ArgumentParser(description="MCP Audit Provenance Tracer CLI")
    parser.add_argument("--demo", action="store_true", help="Run audit tracer demo")
    args = parser.parse_args()

    tracer = AuditProvenanceTracer()
    tracer.record_event("db_write", {"table": "users", "action": "insert"})
    tracer.record_event("send_email", {"to": "ops@example.com"})
    print(f"Chain length: {len(tracer.chain)}, Integrity Valid: {tracer.verify_integrity()}")

if __name__ == "__main__":
    main()
