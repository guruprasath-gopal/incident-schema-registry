# Incident Schema Registry

A centralized repository for managing and validating incident-related JSON schemas used across microservices.

## Overview
This repository serves as a schema registry for incident management workflows, providing standardized JSON schemas and validation tools for inter-service communication. It ensures data consistency and contract compliance across different services in the incident response pipeline.

## Repository Structure

```
incident-schema-registry/
├── README.md                           # This file
├── .gitignore                         # Git ignore rules for Python projects
├── service-name/         # Schema definitions for Client Log Fetcher service
│   ├── README.md                      # service purpose , schema format (draft-07) , schema example
│   └── validate.py                    # Schema validation script uses schmea
```

## Services & Schemas

### Client Log Fetcher Service
**Purpose**: Handles alert processing and log fetching for incident management
**Location**: [`/client-logfetcher-service/`](./client-logfetcher-service/)  

## Getting Started

### Prerequisites
- Python 3
- `fastjsonschema` library for validation

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd incident-schema-registry
```

2. Set up Python virtual environment (optional but recommended):
```bash
python -m venv .schema-validation
source .schema-validation/bin/activate  # On macOS/Linux
# or
.schema-validation\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install fastjsonschema
```

### Usage

#### Validating Schemas

Navigate to any service directory and run the validation script:

```bash
cd client-logfetcher-service
python validate.py                    # Validates built-in sample
python validate.py your_data.json     # Validates custom JSON files
```

The validator will:
- Validate the built-in sample payload
- Validate `rich.json` if it exists in the directory
- Validate any JSON files passed as command-line arguments

## Schema Development Guidelines

### Adding New Schemas

1. Create a new directory for your service: `/your-service-name/`
2. Add a `README.md` with:
   - Schema purpose and description
   - JSON schema definition
   - Sample payload
3. Create a `validate.py` script following the existing pattern
4. Update this main README.md to include your service

### Schema Structure

Each schema should uses https://json-schema.org/draft-07/schema draft-07 format
- **Title**: Descriptive name for the schema
- **Type**: Object type definition
- **Required Fields**: List of mandatory properties
- **Properties**: Detailed field definitions with types and constraints
- **Additional Properties**: Set to `false` for strict validation

### Validation Script Template

Each service should include a `validate.py` script that:
- Defines the JSON schema
- Includes a sample payload
- Provides validation for built-in samples and external files
- Uses `fastjsonschema` for efficient validation