
from google.adk.agents import SequentialAgent

from agents.segmentation_intent_agent import segmentation_intent_agent
from agents.content_agent import content_agent
from agents.compliance_tone_agent import compliance_tone_agent
from agents.delivery_agent import delivery_agent

orchestrator_agent = SequentialAgent(
    name="orchestrator_agent",
    sub_agents=[
        segmentation_intent_agent,
        content_agent,
        compliance_tone_agent,
        delivery_agent,
    ],
)
