"""Deterministic, framework-neutral v2.1 reference runtime."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Agent:
    id: str
    capabilities: frozenset[str]
    permission_ceiling: frozenset[str]

@dataclass(frozen=True)
class Role:
    id: str
    responsibilities: tuple[str, ...]
    allowed_permissions: frozenset[str]

@dataclass
class WorkUnit:
    id: str
    objective: str
    owner: str
    acceptance_criteria: tuple[str, ...]
    parent_id: str | None = None
    status: str = "CREATED"
    attempts: int = 0
    retry_reason: str | None = None
    failure_evidence_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class Evidence:
    id: str
    work_unit_id: str
    source: str
    type: str
    reference: str
    method: str
    trust: str = "VERIFIED"
    digest: str | None = None

@dataclass(frozen=True)
class Handoff:
    id: str
    work_unit_id: str
    sender: str
    receiver: str
    payload_ref: str
    evidence_refs: tuple[str, ...]
    reason: str
    timestamp: str

@dataclass(frozen=True)
class Evaluation:
    id: str
    work_unit_id: str
    criteria: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    result: str
    acceptance: str
    basis: str

@dataclass(frozen=True)
class AgentContract:
    id: str
    work_unit_id: str
    agent_id: str
    role_id: str
    effective_permissions: frozenset[str]
    input: dict[str, Any]
    output: dict[str, Any]
    completion_criteria: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

class RuntimeEngine:
    """Small reference implementation used for deterministic contract tests."""
    def __init__(self) -> None:
        self.agents: dict[str, Agent] = {}
        self.roles: dict[str, Role] = {}
        self.work_units: dict[str, WorkUnit] = {}
        self.contracts: dict[str, AgentContract] = {}
        self.evidence: dict[str, Evidence] = {}
        self.handoffs: dict[str, Handoff] = {}
        self.evaluations: dict[str, Evaluation] = {}

    def register_agent(self, agent: Agent) -> None:
        if not agent.permission_ceiling <= agent.capabilities:
            raise PermissionError("agent permission ceiling exceeds capabilities")
        self.agents[agent.id] = agent

    def register_role(self, role: Role) -> None:
        self.roles[role.id] = role

    def create_work_unit(self, work_unit: WorkUnit) -> None:
        if work_unit.id in self.work_units:
            raise ValueError("work unit already exists")
        self.work_units[work_unit.id] = work_unit

    def bind(self, contract: AgentContract) -> None:
        agent = self.agents[contract.agent_id]
        role = self.roles[contract.role_id]
        wu = self.work_units[contract.work_unit_id]
        effective = agent.permission_ceiling & role.allowed_permissions
        if contract.effective_permissions != effective:
            raise PermissionError("effective permissions must equal agent/role intersection")
        if not contract.evidence_requirements:
            raise ValueError("agent contract requires evidence requirements")
        self.contracts[contract.id] = contract
        wu.status = "READY"

    def start(self, work_unit_id: str) -> None:
        wu = self.work_units[work_unit_id]
        if wu.status != "READY":
            raise RuntimeError("work unit must be READY before execution")
        wu.status = "EXECUTING"
        wu.attempts += 1

    def record_evidence(self, evidence: Evidence) -> None:
        if evidence.work_unit_id not in self.work_units:
            raise ValueError("unknown work unit")
        self.evidence[evidence.id] = evidence

    def handoff(self, handoff: Handoff) -> None:
        wu = self.work_units[handoff.work_unit_id]
        if not handoff.evidence_refs or any(ref not in self.evidence for ref in handoff.evidence_refs):
            raise ValueError("handoff requires existing evidence references")
        wu.status = "HANDOFF_PENDING"
        self.handoffs[handoff.id] = handoff

    def evaluate(self, evaluation: Evaluation) -> None:
        wu = self.work_units[evaluation.work_unit_id]
        if any(ref not in self.evidence for ref in evaluation.evidence_refs):
            raise ValueError("evaluation references missing evidence")
        if evaluation.result in {"FAIL", "UNTESTED", "BLOCKED"} and evaluation.acceptance == "ACCEPTED":
            raise ValueError("unacceptable evaluation cannot be accepted")
        wu.status = evaluation.acceptance
        self.evaluations[evaluation.id] = evaluation

    def retry(
        self,
        work_unit_id: str,
        reason: str,
        failure_evidence_refs: tuple[str, ...],
    ) -> WorkUnit:
        parent = self.work_units[work_unit_id]
        if parent.status not in {"BLOCKED", "REJECTED"}:
            raise RuntimeError("only blocked or rejected work may be retried")
        if not reason.strip():
            raise ValueError("retry requires a reason")
        if not failure_evidence_refs:
            raise ValueError("retry requires failure evidence references")
        for ref in failure_evidence_refs:
            evidence = self.evidence.get(ref)
            if evidence is None:
                raise ValueError("retry references missing failure evidence")
            if evidence.work_unit_id != parent.id:
                raise ValueError("failure evidence must belong to retried work unit")
        retry = WorkUnit(
            f"{parent.id}.retry-{parent.attempts + 1}",
            parent.objective,
            parent.owner,
            parent.acceptance_criteria,
            parent.id,
            retry_reason=reason,
            failure_evidence_refs=failure_evidence_refs,
        )
        self.create_work_unit(retry)
        return retry

    @staticmethod
    def timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()
