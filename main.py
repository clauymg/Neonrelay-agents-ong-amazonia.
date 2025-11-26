
import os
import sys
import vertexai

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

if PROJECT_ID:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print(f"✅ Vertex AI initialized: project={PROJECT_ID}, location={LOCATION}")

from agents.orchestrator_agent import orchestrator_agent

agent = orchestrator_agent

if __name__ == "__main__":
    print(f"✅ Agent ready: {agent.name}")
    print(f"   Sub-agents: {len(agent.sub_agents)}")
