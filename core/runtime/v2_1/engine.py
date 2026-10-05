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
    actor_id: str
    actor_type: str

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
        if agent.id in self.agents:
            raise ValueError("agent already exists")
        self.agents[agent.id] = agent

    def register_role(self, role: Role) -> None:
        if role.id in self.roles:
            raise ValueError("role already exists")
        self.roles[role.id] = role

    def create_work_unit(self, work_unit: WorkUnit) -> None:
        if work_unit.id in self.work_units:
            raise ValueError("work unit already exists")
        if work_unit.owner not in self.agents:
            raise ValueError("work unit owner agent is not registered")
        if work_unit.parent_id == work_unit.id:
            raise ValueError("work unit cannot be its own parent")
        if work_unit.parent_id is not None and work_unit.parent_id not in self.work_units:
            raise ValueError("work unit parent does not exist")
        self.work_units[work_unit.id] = work_unit

    def bind(self, contract: AgentContract) -> None:
        agent = self.agents[contract.agent_id]
        role = self.roles[contract.role_id]
        wu = self.work_units[contract.work_unit_id]
        effective = agent.permission_ceiling & role.allowed_permissions
        if contract.effective_permissions != effective:
            raise PermissionError("effective permissions must equal agent/role intersection")
        if wu.status != "CREATED":
            raise RuntimeError("agent contract may only bind a CREATED work unit")
        if not contract.evidence_requirements:
            raise ValueError("agent contract requires evidence requirements")
        if contract.id in self.contracts:
            raise ValueError("agent contract already exists")
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
        if evidence.id in self.evidence:
            raise ValueError("evidence already exists")
        self.evidence[evidence.id] = evidence

    def handoff(self, handoff: Handoff) -> None:
        wu = self.work_units[handoff.work_unit_id]
        if wu.status != "EXECUTING":
            raise RuntimeError("handoff requires an EXECUTING work unit")
        if handoff.sender not in self.agents:
            raise ValueError("handoff sender agent is not registered")
        if handoff.receiver not in self.agents:
            raise ValueError("handoff receiver agent is not registered")
        if wu.owner != handoff.sender:
            raise ValueError("handoff sender must own the work unit")
        contract = next(
            (item for item in self.contracts.values()
             if item.work_unit_id == handoff.work_unit_id and item.agent_id == handoff.sender),
            None,
        )
        if contract is None:
            raise ValueError("handoff sender is not the authorized work unit agent")
        if not handoff.reason.strip():
            raise ValueError("handoff requires a reason")
        if not handoff.payload_ref.strip():
            raise ValueError("handoff requires a payload reference")
        if not handoff.evidence_refs or any(ref not in self.evidence for ref in handoff.evidence_refs):
            raise ValueError("handoff requires existing evidence references")
        if any(self.evidence[ref].work_unit_id != wu.id for ref in handoff.evidence_refs):
            raise ValueError("handoff evidence must belong to the work unit")
        if handoff.id in self.handoffs:
            raise ValueError("handoff already exists")
        wu.status = "HANDOFF_PENDING"
        self.handoffs[handoff.id] = handoff

    def evaluate(self, evaluation: Evaluation) -> None:
        wu = self.work_units[evaluation.work_unit_id]
        if wu.status not in {"EXECUTING", "HANDOFF_PENDING"}:
            raise RuntimeError("evaluation requires an EXECUTING or HANDOFF_PENDING work unit")
        if evaluation.id in self.evaluations:
            raise ValueError("evaluation already exists")
        if any(ref not in self.evidence for ref in evaluation.evidence_refs):
            raise ValueError("evaluation references missing evidence")
        if evaluation.actor_type not in {"agent", "human"} or not evaluation.actor_id.strip():
            raise ValueError("evaluation requires a valid actor")
        if evaluation.actor_type == "agent" and evaluation.actor_id not in self.agents:
            raise ValueError("evaluation actor agent is not registered")
        if evaluation.actor_type == "human" and evaluation.actor_id in self.agents:
            raise ValueError("human evaluation actor must not be an agent identity")
        if evaluation.result in {"FAIL", "UNTESTED", "BLOCKED"} and evaluation.acceptance == "ACCEPTED":
            raise ValueError("unacceptable evaluation cannot be accepted")
        if evaluation.acceptance not in {"ACCEPTED", "REJECTED", "INCOMPLETE"}:
            raise ValueError("invalid acceptance status")
        if evaluation.acceptance == "ACCEPTED" and evaluation.result != "PASS":
            raise ValueError("only PASS evaluations can be accepted")
        if any(self.evidence[ref].work_unit_id != wu.id for ref in evaluation.evidence_refs):
            raise ValueError("evaluation evidence must belong to the work unit")
        if evaluation.actor_type == "human" and not any(
            self.evidence[ref].type == "human-approval" and self.evidence[ref].source == evaluation.actor_id
            for ref in evaluation.evidence_refs
        ):
            raise ValueError("human acceptance requires human-approval evidence from the actor")
        wu.status = "EVALUATING"
        self.evaluations[evaluation.id] = evaluation
        if evaluation.acceptance == "ACCEPTED":
            wu.status = "ACCEPTED"
        elif evaluation.acceptance == "REJECTED":
            wu.status = "REJECTED"
        else:
            wu.status = "BLOCKED"

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
