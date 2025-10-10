# Metadata Generation Workflow Guide

This document provides a detailed, step-by-step guide for implementing metadata generation in your projects.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    METADATA GENERATION WORKFLOW                  │
└─────────────────────────────────────────────────────────────────┘

Phase 1: DESIGN                Phase 2: IMPLEMENT
┌──────────────┐              ┌──────────────┐
│ Define       │              │ Create       │
│ Requirements │──────────────▶ Schemas      │
└──────────────┘              └──────────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Generate     │
                              │ Examples     │
                              └──────────────┘

Phase 3: EXTRACT               Phase 4: USE
┌──────────────┐              ┌──────────────┐
│ Load Data    │              │ Query        │
│ & Schema     │              │ Metadata     │
└──────────────┘              └──────────────┘
       │                             ▲
       ▼                             │
┌──────────────┐              ┌──────────────┐
│ Extract &    │              │ Store &      │
│ Validate     │──────────────▶ Index        │
└──────────────┘              └──────────────┘
```

## Phase 1: Schema Design

### Step 1.1: Identify Data Entities

Ask yourself:
- What types of data do I need to manage?
- What are the core entities in my domain?
- How do these entities relate to each other?

**Example for Medical Domain:**
- Patients (demographics, contact)
- Medical Records (diagnoses, treatments)
- Clinical Studies (research data)

### Step 1.2: Define Entity Structure

For each entity, identify:
- **Required fields**: Must be present
- **Optional fields**: May be present
- **Field types**: String, number, date, etc.
- **Validation rules**: Patterns, ranges, enums

**Example Structure:**
```
Patient
├── Identifiers (ID, medical record number)
├── Personal Info (name, DOB, gender)
├── Contact Info (phone, email, address)
├── Medical Info (blood type, allergies)
└── Metadata (registration date, status)
```

### Step 1.3: Add Metadata Fields

Decide what metadata to track:

**Temporal Metadata:**
- When was it created?
- When was it last modified?
- When is it effective?

**Provenance Metadata:**
- Who created it?
- What system generated it?
- Where did it come from?

**Administrative Metadata:**
- What version is this?
- What is its current status?
- How is it categorized?

### Step 1.4: Create JSON Schema

```bash
# Create schema file
touch schemas/my_entity_schema.json
```

Basic schema template:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/my-entity.schema.json",
  "title": "My Entity Schema",
  "description": "Schema for my entity",
  "type": "object",
  "required": ["id", "name"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier"
    },
    "name": {
      "type": "string",
      "description": "Entity name"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "createdAt": {
          "type": "string",
          "format": "date-time"
        }
      }
    }
  }
}
```

## Phase 2: Implementation

### Step 2.1: Create Example Data

Create valid example data that matches your schema:

```bash
# Create example file
touch examples/my_entity_example.json
```

Example data:
```json
{
  "id": "ENT-001",
  "name": "Example Entity",
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "createdBy": "user123",
    "version": "1.0"
  }
}
```

### Step 2.2: Validate Schema

Test your schema with examples:

```bash
# Using Python and jsonschema library
pip install jsonschema

# Validate
python -c "
import json
from jsonschema import validate

with open('schemas/my_entity_schema.json') as f:
    schema = json.load(f)
    
with open('examples/my_entity_example.json') as f:
    data = json.load(f)
    
validate(instance=data, schema=schema)
print('Validation successful!')
"
```

### Step 2.3: Set Up Data Ingestion

Create a process to:
1. Receive new data
2. Validate against schema
3. Add system metadata
4. Store in database/filesystem

```python
def ingest_data(data, schema):
    # Validate
    validate(instance=data, schema=schema)
    
    # Add system metadata
    if 'metadata' not in data:
        data['metadata'] = {}
    
    data['metadata']['ingestedAt'] = datetime.utcnow().isoformat()
    data['metadata']['ingestedBy'] = 'system'
    
    # Store
    save_to_database(data)
```

## Phase 3: Metadata Extraction

### Step 3.1: Load Schema and Data

```python
import json

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

schema = load_json_file('schemas/my_entity_schema.json')
data = load_json_file('examples/my_entity_example.json')
```

### Step 3.2: Extract Embedded Metadata

```python
def extract_embedded_metadata(data):
    """Extract metadata object from data."""
    return data.get('metadata', {})

metadata = extract_embedded_metadata(data)
print(f"Created: {metadata.get('createdAt')}")
print(f"Version: {metadata.get('version')}")
```

### Step 3.3: Derive Additional Metadata

```python
def derive_metadata(data, schema):
    """Calculate derived metadata."""
    derived = {
        'field_count': len(data.keys()),
        'has_metadata': 'metadata' in data,
        'schema_version': schema.get('version', 'unknown'),
        'completeness': calculate_completeness(data, schema)
    }
    return derived

def calculate_completeness(data, schema):
    """Calculate percentage of optional fields present."""
    required = set(schema.get('required', []))
    all_props = set(schema.get('properties', {}).keys())
    optional = all_props - required
    
    optional_present = sum(1 for field in optional if field in data)
    return (optional_present / len(optional)) * 100 if optional else 100
```

### Step 3.4: Validate Against Schema

```python
def validate_data(data, schema):
    """Validate and report issues."""
    errors = []
    warnings = []
    
    # Check required fields
    for field in schema.get('required', []):
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check data types
    properties = schema.get('properties', {})
    for field, value in data.items():
        if field in properties:
            expected_type = properties[field].get('type')
            actual_type = type(value).__name__
            # Type checking logic here
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

### Step 3.5: Generate Metadata Report

```python
def generate_report(data, schema, metadata):
    """Create comprehensive metadata report."""
    report = {
        'schema_info': {
            'title': schema.get('title'),
            'version': schema.get('version')
        },
        'data_summary': {
            'id': data.get('id'),
            'type': schema.get('title')
        },
        'metadata': metadata,
        'validation': validate_data(data, schema),
        'timestamp': datetime.utcnow().isoformat()
    }
    return report
```

## Phase 4: Using Metadata

### Step 4.1: Query by Metadata

```python
def find_by_metadata(records, criteria):
    """Find records matching metadata criteria."""
    results = []
    for record in records:
        metadata = record.get('metadata', {})
        
        # Check if all criteria match
        matches = all(
            metadata.get(key) == value 
            for key, value in criteria.items()
        )
        
        if matches:
            results.append(record)
    
    return results

# Example usage
recent_records = find_by_metadata(
    all_records,
    {'status': 'active', 'version': '2.0'}
)
```

### Step 4.2: Generate Statistics

```python
def metadata_statistics(records):
    """Generate metadata statistics."""
    stats = {
        'total_records': len(records),
        'by_status': {},
        'by_version': {},
        'date_range': {
            'earliest': None,
            'latest': None
        }
    }
    
    for record in records:
        metadata = record.get('metadata', {})
        
        # Count by status
        status = metadata.get('status', 'unknown')
        stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        
        # Count by version
        version = metadata.get('version', 'unknown')
        stats['by_version'][version] = stats['by_version'].get(version, 0) + 1
        
        # Track date range
        created = metadata.get('createdAt')
        if created:
            if not stats['date_range']['earliest'] or created < stats['date_range']['earliest']:
                stats['date_range']['earliest'] = created
            if not stats['date_range']['latest'] or created > stats['date_range']['latest']:
                stats['date_range']['latest'] = created
    
    return stats
```

### Step 4.3: Export Metadata Catalog

```python
def export_metadata_catalog(records, output_file):
    """Export all metadata to a catalog file."""
    catalog = []
    
    for record in records:
        entry = {
            'id': record.get('id'),
            'type': record.get('type'),
            'metadata': record.get('metadata', {}),
            'extracted_at': datetime.utcnow().isoformat()
        }
        catalog.append(entry)
    
    with open(output_file, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"Catalog exported: {len(catalog)} entries")
```

## Complete Example Workflow

Here's a complete example combining all phases:

```python
#!/usr/bin/env python3
"""Complete metadata workflow example."""

import json
from datetime import datetime
from pathlib import Path

def complete_workflow(schema_path, data_path):
    """Execute complete metadata workflow."""
    
    print("=" * 60)
    print("METADATA WORKFLOW EXECUTION")
    print("=" * 60)
    
    # Phase 1 & 2: Load schema and data (already created)
    print("\n1. Loading schema and data...")
    with open(schema_path) as f:
        schema = json.load(f)
    with open(data_path) as f:
        data = json.load(f)
    print(f"   Schema: {schema.get('title')}")
    print(f"   Data ID: {data.get('id')}")
    
    # Phase 3: Extract metadata
    print("\n2. Extracting metadata...")
    metadata = data.get('metadata', {})
    print(f"   Found {len(metadata)} metadata fields")
    
    # Validate
    print("\n3. Validating...")
    validation = validate_data(data, schema)
    print(f"   Valid: {validation['valid']}")
    if validation['errors']:
        print(f"   Errors: {validation['errors']}")
    
    # Generate report
    print("\n4. Generating report...")
    report = {
        'schema': schema.get('title'),
        'data_id': data.get('id'),
        'metadata': metadata,
        'validation': validation,
        'generated_at': datetime.utcnow().isoformat()
    }
    
    # Phase 4: Save report
    output_file = 'metadata_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n5. Report saved to: {output_file}")
    print("\nWorkflow complete!")
    print("=" * 60)

if __name__ == "__main__":
    complete_workflow(
        'schemas/patient_schema.json',
        'examples/patient_example.json'
    )
```

## Running the Workflow

### Using the Provided Script

```bash
# Run the extraction tool
python scripts/extract_metadata.py

# This will:
# 1. Load all schemas from schemas/
# 2. Load all examples from examples/
# 3. Extract and validate metadata
# 4. Generate reports for each
```

### Custom Implementation

```bash
# Create your own script
cp scripts/extract_metadata.py scripts/my_workflow.py

# Modify for your needs
# - Add custom extraction logic
# - Change output format
# - Add database integration

# Run your version
python scripts/my_workflow.py
```

## Troubleshooting

### Schema Validation Fails

**Problem**: Data doesn't validate against schema

**Solutions**:
1. Check required fields are present
2. Verify data types match schema
3. Test date formats (use ISO 8601)
4. Validate enum values
5. Check pattern constraints (regex)

### Metadata Missing

**Problem**: Metadata fields not found

**Solutions**:
1. Check if `metadata` object exists in data
2. Verify field names match schema
3. Ensure data ingestion adds metadata
4. Check for typos in field names

### Performance Issues

**Problem**: Extraction is slow

**Solutions**:
1. Process files in batches
2. Use streaming for large files
3. Cache schema objects
4. Parallelize processing
5. Index metadata for faster queries

## Best Practices Summary

✅ **DO**:
- Design schemas before creating data
- Validate all incoming data
- Add metadata automatically during ingestion
- Version everything (schemas and data)
- Document all metadata fields
- Use standard formats (ISO dates, etc.)

❌ **DON'T**:
- Skip validation steps
- Mix different data versions
- Use inconsistent date formats
- Forget to update metadata on changes
- Store sensitive data in metadata
- Ignore schema validation errors

## Next Steps

1. **Review Examples**: Examine schemas and examples in this repository
2. **Customize**: Adapt schemas to your domain
3. **Test**: Validate with real data
4. **Automate**: Integrate into your pipelines
5. **Monitor**: Track metadata quality over time
6. **Iterate**: Refine based on usage patterns

---

For more information, see [README.md](README.md) and [SCHEMAS.md](SCHEMAS.md).
