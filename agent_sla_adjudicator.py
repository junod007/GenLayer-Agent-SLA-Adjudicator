# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class AgentSLAAdjudicator(gl.Contract):

    clients: TreeMap[u256, Address]
    agents: TreeMap[u256, Address]
    services: TreeMap[u256, str]
    evidence_urls: TreeMap[u256, str]
    deadlines: TreeMap[u256, str]
    criteria: TreeMap[u256, str]

    statuses: TreeMap[u256, str]
    decisions: TreeMap[u256, str]
    reasons: TreeMap[u256, str]

    next_sla_id: u256

    def __init__(self):
        self.next_sla_id = u256(0)

    @gl.public.write
    def create_sla(
        self,
        agent: str,
        service: str,
        evidence_url: str,
        deadline: str,
        criteria: str
    ) -> u256:

        if not service:
            raise gl.UserError("Service description required")

        if not evidence_url:
            raise gl.UserError("Evidence URL required")

        if not criteria:
            raise gl.UserError("Evaluation criteria required")

        agent_address = Address(agent)

        if agent_address == Address(
            "0x0000000000000000000000000000000000000000"
        ):
            raise gl.UserError("Invalid agent address")

        sla_id = self.next_sla_id

        self.clients[sla_id] = gl.message.sender_address
        self.agents[sla_id] = agent_address
        self.services[sla_id] = service
        self.evidence_urls[sla_id] = evidence_url
        self.deadlines[sla_id] = deadline
        self.criteria[sla_id] = criteria

        self.statuses[sla_id] = "PENDING"
        self.decisions[sla_id] = "UNDETERMINED"
        self.reasons[sla_id] = ""

        self.next_sla_id = self.next_sla_id + u256(1)

        return sla_id

    @gl.public.write
    def evaluate_sla(self, sla_id: u256) -> typing.Any:

        if sla_id not in self.statuses:
            raise gl.UserError("SLA not found")

        if self.statuses[sla_id] != "PENDING":
            raise gl.UserError("SLA already evaluated")

        service = self.services[sla_id]
        evidence_url = self.evidence_urls[sla_id]
        deadline = self.deadlines[sla_id]
        criteria = self.criteria[sla_id]

        def evaluate_evidence():

            response = gl.nondet.web.get(evidence_url)

            evidence = response.body.decode("utf-8")

            if not evidence.strip():
                return {
                    "decision": "UNDETERMINED",
                    "reason": "Evidence source unavailable or empty"
                }

            prompt = f"""
You are an impartial SLA adjudicator.

Determine whether an AI agent fulfilled this service agreement.

SERVICE:
{service}

DEADLINE:
{deadline}

EVALUATION CRITERIA:
{criteria}

EVIDENCE URL:
{evidence_url}

EVIDENCE:
{evidence}

Rules:

ACCEPTED:
The evidence clearly demonstrates that the requirements
and evaluation criteria were fulfilled.

REJECTED:
The evidence clearly demonstrates that the requirements
were not fulfilled.

UNDETERMINED:
The evidence is missing, insufficient, contradictory,
or does not allow a reliable determination.

Do not invent facts.
Use only information supported by the evidence.

Return JSON with exactly:

{{
    "decision": "ACCEPTED",
    "reason": "short factual explanation"
}}
"""

            result = gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

            return result

        result = gl.eq_principle.prompt_comparative(
            evaluate_evidence,
            principle=(
                "The decision field must be exactly the same. "
                "Allowed values are ACCEPTED, REJECTED, or UNDETERMINED. "
                "The reason must be factually consistent with the decision."
            )
        )

        decision = result.get("decision", "UNDETERMINED")
        reason = result.get("reason", "")

        if decision not in [
            "ACCEPTED",
            "REJECTED",
            "UNDETERMINED"
        ]:
            decision = "UNDETERMINED"

        self.decisions[sla_id] = decision
        self.reasons[sla_id] = reason
        self.statuses[sla_id] = "EVALUATED"

        return {
            "sla_id": sla_id,
            "decision": decision,
            "reason": reason
        }

    @gl.public.view
    def get_sla(self, sla_id: u256) -> typing.Any:

        if sla_id not in self.statuses:
            raise gl.UserError("SLA not found")

        return {
            "client": str(self.clients[sla_id]),
            "agent": str(self.agents[sla_id]),
            "service": self.services[sla_id],
            "evidence_url": self.evidence_urls[sla_id],
            "deadline": self.deadlines[sla_id],
            "criteria": self.criteria[sla_id],
            "status": self.statuses[sla_id],
            "decision": self.decisions[sla_id],
            "reason": self.reasons[sla_id]
        }

    @gl.public.view
    def get_sla_count(self) -> u256:
        return self.next_sla_id
