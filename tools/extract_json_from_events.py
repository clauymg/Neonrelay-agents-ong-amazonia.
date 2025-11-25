
import json 
from google.genai import types
import time

def extract_json_from_events(events, required_keys=None, step_name: str = ""):
    """
    Recorre TODOS los eventos y parts, intenta extraer JSON.
    - Junta todos los JSON válidos.
    - Si required_keys se pasa, elige el primero que contenga todas esas claves.
    - Si no se pasa, devuelve el primer JSON válido.
    - Si nada matchea, lanza ValueError con info de debug.
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

            # Intento 1: JSON directo
            try:
                data = json.loads(text)
                candidates.append(data)
                continue
            except json.JSONDecodeError:
                pass

            # Intento 2: recorte entre primera y última llave
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                sub = text[start:end+1]
                try:
                    data = json.loads(sub)
                    candidates.append(data)
                except json.JSONDecodeError:
                    pass

    if not candidates:
        raise ValueError(
            f"[{step_name}] No JSON found in ANY event or part. "
            f"Revisa el dump de eventos para ver el texto crudo."
        )

    # Sin required_keys → devolvemos el primero
    if not required_keys:
        return candidates[0]

    required_keys = set(required_keys)

    # Buscar el primer dict que tenga todas las claves
    for data in candidates:
        if isinstance(data, dict) and required_keys.issubset(data.keys()):
            return data

    all_keys = [list(d.keys()) for d in candidates if isinstance(d, dict)]
    raise ValueError(
        f"[{step_name}] JSON found, pero NINGUNO tiene todas las claves {required_keys}. "
        f"Keys encontradas: {all_keys}"
    )
