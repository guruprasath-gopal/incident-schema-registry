#!/usr/bin/env python3
# Validate schema-defined samples, rich.json (if present), and any JSON files passed on CLI.
# Usage:
#   pip install fastjsonschema
#   python x.py                # validates SAMPLE + rich.json if exists
#   python x.py foo.json bar.json

import json
import pathlib
import sys
from typing import Any

import fastjsonschema
from fastjsonschema import JsonSchemaException

HERE = pathlib.Path(__file__).resolve().parent
RICH = HERE / "rich.json"

# ----------------------------
# SCHEMA DEFINITION
# ----------------------------
SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ALERT_CREATED",
    "type": "object",
    "additionalProperties": False,
    "required": ["messageType", "incident"],
    "properties": {
        "messageType": {"const": "ALERT_CREATED"},
        "incident": {
            "type": "object",
            "additionalProperties": False,
            "required": ["incident_id", "session"],
            "properties": {
                "incident_id": {"type": "string", "minLength": 1},
                "session": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "session_id",
                        "incident_id",
                        "company_id",
                        "metadata",
                        "alerts",
                    ],
                    "properties": {
                        "session_id": {"type": "string", "minLength": 1},
                        "incident_id": {"type": "string", "minLength": 1},
                        "company_id": {"type": "string", "minLength": 1},
                        "metadata": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "title",
                                "service",
                                "severity",
                                "timestamp",
                                "source",
                                "environment",
                            ],
                            "properties": {
                                "title": {"type": "string", "minLength": 1},
                                "service": {"type": "string", "minLength": 1},
                                "severity": {
                                    "type": "string",
                                    "enum": ["low", "medium", "high", "critical"],
                                },
                                "timestamp": {"type": "string", "format": "date-time"},
                                "source": {"type": "string", "minLength": 1},
                                "environment": {
                                    "type": "string",
                                    "enum": ["development", "staging", "production"],
                                },
                            },
                        },
                        "alerts": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["service", "title", "severity"],
                                "properties": {
                                    "service": {"type": "string", "minLength": 1},
                                    "title": {"type": "string", "minLength": 1},
                                    "severity": {
                                        "type": "string",
                                        "enum": ["low", "medium", "high", "critical"],
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

# ----------------------------
# SAMPLE PAYLOAD
# ----------------------------
SAMPLE = {
    "messageType": "ALERT_CREATED",
    "incident": {
        "incident_id": "bugraid-INC-804",
        "session": {
            "session_id": "0958989a-a7e5-48dd-9365-92efb6e32f95",
            "incident_id": "bugraid-INC-804",
            "company_id": "acme-co",
            "metadata": {
                "title": "Spike in 5xx for payments",
                "service": "payments",
                "severity": "high",
                "timestamp": "2025-09-11T04:55:00Z",
                "source": "grafana-alerting",
                "environment": "development",
            },
            "alerts": [
                {
                    "service": "payments",
                    "title": "HTTP 500 surge",
                    "severity": "critical",
                }
            ],
        },
    },
}


def load_json_file(path: pathlib.Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[x] Failed to load JSON from {path}: {e}")
        sys.exit(1)


def validate(validator, obj: Any, name: str) -> int:
    try:
        validator(obj)
        print(f"[ok] {name} ✓")
        return 0
    except JsonSchemaException as e:
        print(f"[!] {name} ✗")
        print(f"    {e.message}")
        return 1


def main() -> None:
    try:
        validator = fastjsonschema.compile(SCHEMA)
    except Exception as e:
        print(f"[x] Schema compilation failed: {e}")
        sys.exit(1)

    rc = 0
    rc += validate(validator, SAMPLE, "builtin SAMPLE")

    if RICH.exists():
        rc += validate(validator, load_json_file(RICH), "rich.json")

    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        if p.suffix.lower() == ".json" and p.exists():
            rc += validate(validator, load_json_file(p), str(p))
        else:
            print(f"[i] Skipping non-JSON or missing file: {arg}")

    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
