# ALERT_CREATED (Client logs → Client Log Fetcher)

**Input data description:** Client logs  
**Used by:** Client Log Fetcher service  
**Purpose:** Triggers log fetch & processing for a newly observed alert.

## Schema
```json schema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ALERT_CREATED",
  "type": "object",
  "additionalProperties": false,
  "required": ["messageType", "incident"],
  "properties": {
    "messageType": { "const": "ALERT_CREATED" },
    "incident": {
      "type": "object",
      "additionalProperties": false,
      "required": ["incident_id", "session"],
      "properties": {
        "incident_id": { "type": "string", "minLength": 1 },
        "session": {
          "type": "object",
          "additionalProperties": false,
          "required": ["session_id", "incident_id", "company_id", "metadata", "alerts"],
          "properties": {
            "session_id": {
              "type": "string",
              "minLength": 1,
            },
            "incident_id": { "type": "string", "minLength": 1 },
            "company_id": { "type": "string", "minLength": 1 },
            "metadata": {
              "type": "object",
              "additionalProperties": false,
              "required": ["title", "service", "severity", "timestamp", "source", "environment"],
              "properties": {
                "title": { "type": "string", "minLength": 1 },
                "service": { "type": "string", "minLength": 1 },
                "severity": { "type": "string" },
                "timestamp": { "type": "string", "format": "date-time" },
                "source": { "type": "string", "minLength": 1 },
                "environment": { "type": "string" }
              }
            },
            "alerts": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["service", "title", "severity"],
                "properties": {
                  "service": { "type": "string", "minLength": 1 },
                  "title": { "type": "string", "minLength": 1 },
                  "severity": { "type": "string" }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
## Sample 
{
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
        "environment": "development"
      },
      "alerts": [
        { "service": "payments", "title": "HTTP 500 surge", "severity": "critical" }
      ]
    }
  }
}
