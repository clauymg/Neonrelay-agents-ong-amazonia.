
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, asdict



# Métricas globales simples (in-memory)
METRICS = {
    "pipelines_total": 0,
    "pipelines_ok": 0,
    "pipelines_needs_human": 0,
    "pipelines_error": 0,
}


@dataclass
class PipelineTrace:
    trace_id: str
    app_name: str
    user_id: str
    session_id: str
    start_time: float
    end_time: float | None = None
    latency_sec: float | None = None
    status: str | None = None   # "ok" | "needs_human" | "error"
    errors: list | None = None
    agents_summary: dict | None = None


def start_pipeline_trace(app_name: str, user_id: str, session_id: str) -> PipelineTrace:
    trace = PipelineTrace(
        trace_id=str(uuid.uuid4()),
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        start_time=time.time(),
        errors=[],
        agents_summary={},
    )
    METRICS["pipelines_total"] += 1
    print(f"[OBS] Start pipeline trace_id={trace.trace_id} session_id={session_id}")
    return trace


def finish_pipeline_trace(trace: PipelineTrace, status: str, errors: list | None = None):
    trace.end_time = time.time()
    trace.latency_sec = trace.end_time - trace.start_time
    trace.status = status
    if errors:
        trace.errors = errors

    # actualizar métricas agregadas
    if status == "ok":
        METRICS["pipelines_ok"] += 1
    elif status == "needs_human":
        METRICS["pipelines_needs_human"] += 1
    else:
        METRICS["pipelines_error"] += 1

    print(f"[OBS] End pipeline trace_id={trace.trace_id} "
          f"status={status} latency={trace.latency_sec:.3f}s")

    # También podemos imprimir el trace como JSON-friendly dict
    print("[OBS] Trace summary:", asdict(trace))
    return trace


def summarize_events_by_agent(events):
    """
    Saca un resumen liviano:
    - cuántos eventos por agent_name
    - tipos de eventos
    """
    summary = defaultdict(lambda: {"events": 0, "event_types": defaultdict(int)})

    for e in events:
        event_type = getattr(e, "event_type", "unknown")
        # Algunos eventos traen agent_name directo, otros se pueden leer via agent.name
        agent_name = getattr(e, "agent_name", None)
        if not agent_name:
            agent_obj = getattr(e, "agent", None)
            agent_name = getattr(agent_obj, "name", "unknown_agent")

        summary[agent_name]["events"] += 1
        summary[agent_name]["event_types"][event_type] += 1

    # Convertir defaultdicts anidados a dicts normales
    clean_summary = {}
    for agent_name, data in summary.items():
        clean_summary[agent_name] = {
            "events": data["events"],
            "event_types": dict(data["event_types"]),
        }

    print("[OBS] Events by agent:")
    for agent_name, data in clean_summary.items():
        print(f"  - {agent_name}: {data['events']} events, types={data['event_types']}")

    return clean_summary
