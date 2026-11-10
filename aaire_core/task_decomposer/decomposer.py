import re
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class DynamicAgentSpec:
    agent_id: str
    role_name: str
    system_prompt: str
    capabilities: List[str] = field(default_factory=list)
    ephemeral: bool = True


@dataclass
class SubTask:
    task_id: str
    title: str
    description: str
    assigned_role: str
    agent_spec: DynamicAgentSpec
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1
    status: str = "PENDING"
    retries: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DynamicAgentForge:
    """
    टास्क की ज़रूरत के हिसाब से तुरंत नया स्पेशलिस्ट AI एजेंट बनाता है।
    इसमें एजेंट्स की संख्या या कैटेगरी की कोई सीमा नहीं है।
    """

    BASE_ROLES = {
        "scraper": ["scrape", "fetch", "crawl", "html", "spider", "portal", "url", "extract"],
        "security_auditor": ["security", "crypto", "vault", "auth", "guard", "ssl", "tls", "audit"],
        "coder": ["code", "build", "create", "script", "python", "function", "api", "implement"],
        "binary_reverser": ["apk", "binary", "decompile", "dotnet", "inspect", "hex", "reverse"],
        "architect": ["design", "plan", "architecture", "dag", "structure", "schema", "pipeline"],
        "validator": ["test", "verify", "validate", "check", "quality", "assert", "benchmark"]
    }

    @classmethod
    def spawn_agent_for_task(cls, task_description: str) -> DynamicAgentSpec:
        text_lower = task_description.lower()

        for role, keywords in cls.BASE_ROLES.items():
            if any(kw in text_lower for kw in keywords):
                return DynamicAgentSpec(
                    agent_id=f"agent_{role}_{uuid.uuid4().hex[:6]}",
                    role_name=role,
                    system_prompt=f"You are an elite {role.upper()} specialist in AAIRE. Execute: {task_description}",
                    capabilities=keywords
                )

        # अगर काम बिल्कुल नया है, तो टास्क के शब्दों से तुरंत नया स्पेशलिस्ट एजेंट बनाएं
        words = [w for w in re.findall(r'[a-zA-Z0-9_]+', text_lower) if len(w) > 3]
        custom_domain = "_".join(words[:2]) if words else "universal_solver"
        dynamic_role = f"specialist_{custom_domain}_agent"

        return DynamicAgentSpec(
            agent_id=f"dyn_{uuid.uuid4().hex[:8]}",
            role_name=dynamic_role,
            system_prompt=(
                f"You are a dynamically spawned AAIRE Specialist Agent ({dynamic_role}). "
                f"Your sole mission is to master and execute this specific task: {task_description}"
            ),
            capabilities=words[:5] if words else ["general_problem_solving"]
        )


class TaskDecomposer:
    """
    बड़े मिशन को अनलिमिटेड सब-टास्क्स में तोड़ता है और हर काम के लिए अलग एजेंट तैनात करता है।
    """

    def __init__(self, allow_unlimited: bool = True):
        self.allow_unlimited = allow_unlimited

    def decompose(self, objective: str, context: Optional[Dict[str, Any]] = None) -> List[SubTask]:
        if not objective or not objective.strip():
            return []

        raw_parts = re.split(
            r'(?:\n+|;\s*|\.\s+|\s+and\s+|\s+then\s+|\s+उसके बाद\s+|\s+और\s+|\s+फिर\s+)',
            objective.strip()
        )
        cleaned_parts = [p.strip() for p in raw_parts if len(p.strip()) > 3]

        if not cleaned_parts:
            cleaned_parts = [objective.strip()]

        subtasks: List[SubTask] = []

        for idx, part in enumerate(cleaned_parts, start=1):
            t_id = f"subtask_{idx}_{uuid.uuid4().hex[:6]}"
            spawned_agent = DynamicAgentForge.spawn_agent_for_task(part)

            subtask = SubTask(
                task_id=t_id,
                title=f"Dynamic Execution [{spawned_agent.role_name.upper()}]",
                description=part,
                assigned_role=spawned_agent.role_name,
                agent_spec=spawned_agent,
                dependencies=[],
                priority=idx
            )
            subtasks.append(subtask)

        val_agent = DynamicAgentForge.spawn_agent_for_task("validate and verify all swarm outputs")
        subtasks.append(
            SubTask(
                task_id=f"subtask_{len(subtasks)+1}_gate",
                title="Final Swarm Quality Gate Verification",
                description=f"Validate all {len(subtasks)} parallel agent outputs.",
                assigned_role="validator",
                agent_spec=val_agent,
                dependencies=[t.task_id for t in subtasks],
                priority=len(subtasks) + 1
            )
        )

        return subtasks
                      
