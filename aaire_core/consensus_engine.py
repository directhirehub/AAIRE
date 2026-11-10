# File: aaire_core/consensus_engine.py

from typing import Dict, Any, List

class AAIREConsensusEngine:
    """
    AAIRE के लिए 100% ओरिजिनल मल्टी-एजेंट डिबेट और कंसेंसस इंजन।
    यह विभिन्न वर्चुअल एजेंट्स के प्रपोजल्स की समीक्षा करके सर्वसम्मति (Consensus) बनाता है।
    """
    def __init__(self):
        self.proposals: List[Dict[str, Any]] = []

    def submit_proposal(self, agent_name: str, proposal_text: str, confidence_score: float) -> None:
        """
        विभिन्न एजेंट्स से प्रपोजल या समाधान स्वीकार करता है।
        """
        proposal = {
            "agent": agent_name,
            "proposal": proposal_text,
            "confidence": max(0.0, min(1.0, confidence_score)),
            "votes": 0
        }
        self.proposals.append(proposal)

    def reach_consensus(self, task_objective: str) -> Dict[str, Any]:
        """
        सभी प्रपोजल्स का विश्लेषण करता है और सबसे अधिक स्कोर वाले सर्वमान्य समाधान को चुनता है।
        """
        if not self.proposals:
            return {
                "objective": task_objective,
                "status": "failed",
                "consensus_reached": False,
                "winning_proposal": None,
                "reason": "No proposals submitted for consensus."
            }

        # कॉन्फिडेंस स्कोर के आधार पर सर्वश्रेष्ठ प्रपोजल का चयन (कंसेंसस लूप)
        best_proposal = max(self.proposals, key=lambda x: x["confidence"])

        return {
            "objective": task_objective,
            "status": "success",
            "consensus_reached": True,
            "total_participants": len(self.proposals),
            "winning_agent": best_proposal["agent"],
            "winning_proposal": best_proposal["proposal"],
            "confidence_score": best_proposal["confidence"],
            "all_proposals": self.proposals
        }
      
