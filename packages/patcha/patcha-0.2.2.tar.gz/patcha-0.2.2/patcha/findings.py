import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger("patcha")

class SecurityFinding:
    """Class representing a security finding"""
    
    def __init__(
        self,
        title: str,
        message: str,
        rule_id: Optional[str] = None,
        severity: str = "medium",
        confidence: str = "medium",
        file_path: Optional[str] = None,
        line_number: Optional[int] = None,
        code_snippet: Optional[str] = None,
        scanner: Optional[str] = None,
        type: Optional[str] = None,
        cwe: Optional[str] = None,
        remediation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        tool: Optional[str] = None,
    ):
        self.title = title
        self.message = message
        self.rule_id = rule_id
        self.severity = severity.lower() if severity else "medium"
        self.confidence = confidence.lower() if confidence else "medium"
        self.file_path = file_path
        self.line_number = line_number
        self.code_snippet = code_snippet
        self.scanner = scanner or tool or "unknown"
        self.type = type
        self.cwe = cwe
        self.remediation = remediation
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
        self.source = source or self.scanner
        self.fingerprint = self._generate_fingerprint()
    
    def _generate_fingerprint(self) -> str:
        """Generate a unique fingerprint for deduplication."""
        data = (
            f"{self.rule_id or self.title or ''}-"
            f"{self.file_path or ''}-"
            f"{self.line_number or 0}-"
            f"{hashlib.md5((self.code_snippet or self.message or '')[:100].encode()).hexdigest()}"
        )
        return hashlib.md5(data.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary for serialization"""
        return {
            "title": self.title,
            "message": self.message,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "scanner": self.scanner,
            "type": self.type,
            "cwe": self.cwe,
            "remediation": self.remediation,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "fingerprint": self.fingerprint,
            "source": self.source,
        }

    def __eq__(self, other):
        if not isinstance(other, SecurityFinding):
            return NotImplemented
        return self.fingerprint == other.fingerprint

    def __hash__(self):
        return hash(self.fingerprint)

    def __repr__(self) -> str:
        return (f"SecurityFinding(rule='{self.rule_id or self.title}', "
                f"file='{self.file_path}:{self.line_number}', "
                f"severity='{self.severity}')")


class FindingsManager:
    """Class for managing security findings"""
    
    def __init__(self):
        self.findings = []
    
    def add_finding(self, finding: SecurityFinding) -> None:
        """Add a finding to the list"""
        self.findings.append(finding)
        logger.debug(f"Added finding: {finding.title}")
    
    def get_findings(self) -> List[SecurityFinding]:
        """Get all findings"""
        return self.findings
    
    def get_findings_by_severity(self, severity: str) -> List[SecurityFinding]:
        """Get findings by severity"""
        return [f for f in self.findings if f.severity.lower() == severity.lower()]
    
    def get_findings_by_file(self, file_path: str) -> List[SecurityFinding]:
        """Get findings by file path"""
        return [f for f in self.findings if f.file_path == file_path]
    
    def get_findings_by_scanner(self, scanner: str) -> List[SecurityFinding]:
        """Get findings by scanner"""
        return [f for f in self.findings if f.scanner == scanner]
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all findings to a list of dictionaries"""
        return [finding.to_dict() for finding in self.findings] 