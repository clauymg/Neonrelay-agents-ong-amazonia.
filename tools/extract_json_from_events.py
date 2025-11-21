
import json

from observability.observability_funct import (
    start_pipeline_trace,
    finish_pipeline_trace,
    summarize_events_by_agent,
    METRICS
)


def extract_json_from_events(events, required_keys=None, step_name=""):
    """
    Recorre TODOS los eventos y parts, intenta extraer JSON.
    - Junta todos los JSON válidos.
    - Si required_keys se pasa, elige el primero que contenga todas esas claves.
    - Si no se pasa, devuelve el primer JSON válido.
    - Si nada matchea, lanza ValueError.
    """
    candidates = []

    for e in events:
        content = getattr(e, "content", None)
        if not content:
            continue

        parts = getattr(content, "parts", [])
        for part in parts:
            text = getattr(part, "text", None)
            if not text:
                continue

            # 1) Intento directo
            try:
                data = json.loads(text)
                candidates.append(data)
                continue
            except json.JSONDecodeError:
                pass

            # 2) Intento recortando entre primera "{" y última "}"
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = text[start:end+1]
                try:
                    data = json.loads(candidate)
                    candidates.append(data)
                except json.JSONDecodeError:
                    continue

    if not candidates:
        raise ValueError(f"[{step_name}] No JSON found at all in events.")

    # Si no hay required_keys → devolvemos el primer JSON válido
    if required_keys is None:
        return candidates[0]

    # Normalizamos required_keys a set
    if not isinstance(required_keys, set):
        required_keys = set(required_keys)

    # Buscamos el primer JSON que tenga todas las claves requeridas
    for data in candidates:
        if isinstance(data, dict):
            if required_keys.issubset(set(data.keys())):
                return data

    # Debug: mostrar qué claves se encontraron realmente
    all_keys = [list(d.keys()) for d in candidates if isinstance(d, dict)]
    raise ValueError(
        f"[{step_name}] No JSON with required_keys={required_keys} found. "
        f"Candidate keys: {all_keys}"
    )
