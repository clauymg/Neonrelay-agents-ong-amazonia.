
import json
from agents.orchestrator_agent import orchestrator_agent
from tools.extract_json_from_events import extract_json_from_events
from tools.dump_event_texts import dump_event_texts
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types



from observability.observability_funct import (
    start_pipeline_trace,
    finish_pipeline_trace,
    summarize_events_by_agent,
    METRICS,
)


APP_NAME = "ong_amazonia_email_pipeline"
USER_ID = "user_001"

async def run_email_pipeline_orchestrator(email_text: str, contact_data: dict):
    """
    Ejecuta el SequentialAgent (orchestrator_agent) y parsea:
      - segmentation_intent_agent
      - content_agent
      - compliance_tone_agent
      - delivery_agent

    Devuelve: (result, trace)
    """
    # ---- Session + Trace ----
    service = InMemorySessionService()
    session_id = contact_data.get("id") or contact_data.get("email") or "session_001"

    session = await service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    trace = start_pipeline_trace(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session.id,
    )

    runner = Runner(
        agent=orchestrator_agent,
        app_name=APP_NAME,
        session_service=service,
    )

    initial_prompt = f"""
USER_EMAIL:
{email_text}

CONTACT_DATA (JSON):
{json.dumps(contact_data, ensure_ascii=False)}
"""

    new_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=initial_prompt)],
    )

    # ---- Ejecutar orquestador UNA sola vez ----
    try:
        events_stream = runner.run(
            user_id=USER_ID,
            session_id=session.id,
            new_message=new_message,
        )
        # IMPORTANTÍSIMO: materializar el iterable en lista
        events = list(events_stream)
    except Exception as e:
        errors = [f"Runner error: {e}"]
        finish_pipeline_trace(trace, status="error", errors=errors)
        return {
            "segmentation": None,
            "content": None,
            "compliance": None,
            "delivery": None,
            "needs_human": True,
            "errors": errors,
        }, trace

    # Testing: ver texto crudo de los eventos (usa la MISMA lista)
    dump_event_texts(events, label="AFTER_ORCHESTRATOR")

    # Observability: resumen por agente usando la misma lista
    agents_summary = summarize_events_by_agent(events)
    trace.agents_summary = agents_summary

    # ---- Estructura resultado de negocio ----
    result = {
        "segmentation": None,
        "content": None,
        "compliance": None,
        "delivery": None,
        "needs_human": False,
        "errors": [],
    }

    # =====================
    # 1) SEGMENTATION
    # =====================
    try:
        segmentation = extract_json_from_events(
            events,
            required_keys={"segment", "language", "intent", "is_repetitive_faq"},
            step_name="segmentation",
        )
        result["segmentation"] = segmentation
    except Exception as e:
        result["errors"].append(f"Segmentation error: {e}")
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="error", errors=result["errors"])
        return result, trace

    # Regla de negocio: si no es FAQ repetitiva → escalar a humano
    if not segmentation.get("is_repetitive_faq", False):
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="needs_human", errors=result["errors"])
        return result, trace

    # =====================
    # 2) CONTENT
    # =====================
    try:
        content = extract_json_from_events(
            events,
            required_keys={"subject", "body", "suggested_cta"},
            step_name="content",
        )
        result["content"] = content
    except Exception as e:
        result["errors"].append(f"Content error: {e}")
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="error", errors=result["errors"])
        return result, trace

    # =====================
    # 3) COMPLIANCE
    # =====================
    try:
        compliance = extract_json_from_events(
            events,
            required_keys={
                "approved",
                "final_subject",
                "final_body",
                "notes_for_internal_team",
            },
            step_name="compliance",
        )
        result["compliance"] = compliance
    except Exception as e:
        result["errors"].append(f"Compliance error: {e}")
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="error", errors=result["errors"])
        return result, trace

    if not compliance.get("approved", False):
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="needs_human", errors=result["errors"])
        return result, trace

    # =====================
    # 4) DELIVERY
    # =====================
    try:
        delivery = extract_json_from_events(
            events,
            required_keys={"channel", "to", "subject", "body", "send_now"},
            step_name="delivery",
        )
        result["delivery"] = delivery
    except Exception as e:
        result["errors"].append(f"Delivery error: {e}")
        result["needs_human"] = True
        finish_pipeline_trace(trace, status="error", errors=result["errors"])
        return result, trace

    # Si llegamos aquí → todo OK
    finish_pipeline_trace(trace, status="ok", errors=result["errors"])
    return result, trace

