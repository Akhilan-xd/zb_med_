# Quick Start Guide

Get started with schemas and metadata extraction in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/Akhilan-xd/zb_med_.git
cd zb_med_

# No dependencies required for basic usage!
# (Optional) For advanced validation, install jsonschema:
pip install jsonschema
```

## Quick Test

Run the metadata extraction tool:

```bash
python scripts/extract_metadata.py
```

You should see output showing metadata extracted from all three example files.

## Understanding the Structure

```
zb_med_/
├── schemas/          # Schema definitions (the blueprints)
├── examples/         # Sample data (conforming to schemas)
├── scripts/          # Tools for metadata extraction
└── *.md             # Documentation
```

## 5-Minute Tutorial

### Step 1: Look at a Schema (30 seconds)

```bash
cat schemas/patient_schema.json
```

This defines what a valid patient record looks like.

### Step 2: Look at Example Data (30 seconds)

```bash
cat examples/patient_example.json
```

This is actual data that follows the patient schema.

### Step 3: Extract Metadata (1 minute)

```bash
python scripts/extract_metadata.py
```

This shows:
- What metadata is embedded in the data
- Whether the data is valid
- Summary information

### Step 4: Try It Yourself (3 minutes)

Create your own data file:

```bash
cat > my_patient.json << 'EOF'
{
  "patientId": "P-99999999",
  "personalInfo": {
    "firstName": "Jane",
    "lastName": "Smith",
    "dateOfBirth": "1990-05-20",
    "gender": "female",
    "bloodType": "A+"
  },
  "contactInfo": {
    "email": "jane.smith@example.com",
    "phone": "+15555551234"
  },
  "metadata": {
    "registrationDate": "2024-01-15T10:00:00Z",
    "status": "active",
    "recordSource": "manual_entry"
  }
}
EOF
```

Validate it programmatically:

```python
import json

# Load schema
with open('schemas/patient_schema.json') as f:
    schema = json.load(f)

# Load your data
with open('my_patient.json') as f:
    data = json.load(f)

# Extract metadata
metadata = data.get('metadata', {})
print("Patient ID:", data['patientId'])
print("Status:", metadata.get('status'))
print("Registered:", metadata.get('registrationDate'))
```

## Common Tasks

### Task: Validate Data Against Schema

```python
from jsonschema import validate
import json

# Load
with open('schemas/patient_schema.json') as f:
    schema = json.load(f)
with open('examples/patient_example.json') as f:
    data = json.load(f)

# Validate
try:
    validate(instance=data, schema=schema)
    print("✓ Valid!")
except Exception as e:
    print(f"✗ Invalid: {e}")
```

### Task: Extract Specific Metadata

```python
import json

with open('examples/medical_record_example.json') as f:
    record = json.load(f)

# Get metadata
metadata = record['metadata']
print(f"Created: {metadata['createdAt']}")
print(f"Version: {metadata['version']}")
print(f"Tags: {', '.join(metadata['tags'])}")
```

### Task: Check Required Fields

```python
import json

with open('schemas/patient_schema.json') as f:
    schema = json.load(f)

required_fields = schema['required']
print("Required fields:", required_fields)

# Check data has them
with open('examples/patient_example.json') as f:
    data = json.load(f)

for field in required_fields:
    if field in data:
        print(f"✓ {field}")
    else:
        print(f"✗ {field} MISSING")
```

## Next Steps

1. **Read the Full Documentation**
   - [README.md](README.md) - Overview and concepts
   - [SCHEMAS.md](SCHEMAS.md) - Detailed schema documentation
   - [WORKFLOW.md](WORKFLOW.md) - Complete workflow guide

2. **Explore the Examples**
   - Open files in `schemas/` to see schema definitions
   - Open files in `examples/` to see valid data
   - Compare them to understand the relationship

3. **Customize for Your Needs**
   - Copy a schema and modify it
   - Create your own example data
   - Update the extraction script

4. **Integrate into Your Project**
   - Use schemas to validate incoming data
   - Extract metadata for indexing/search
   - Generate documentation automatically

## Common Questions

**Q: What is a JSON Schema?**
A: A formal way to describe the structure and rules for JSON data. Like a template or contract.

**Q: Why use schemas?**
A: To ensure data quality, document structure, enable validation, and facilitate interoperability.

**Q: What is metadata?**
A: Information about the data - who created it, when, what version, etc.

**Q: How do I create my own schema?**
A: Start with an existing schema, modify it for your needs, test with examples. See [WORKFLOW.md](WORKFLOW.md).

**Q: Can I use this in production?**
A: The schemas and concepts are production-ready. You may want to add more robust validation libraries like `jsonschema` for Python.

**Q: What if my data doesn't match the schema?**
A: The validation will fail and tell you what's wrong. Fix the data or update the schema as needed.

## Troubleshooting

**Problem: Script doesn't run**
```bash
# Check Python version (need 3.6+)
python3 --version

# Run with explicit python3
python3 scripts/extract_metadata.py
```

**Problem: JSON syntax error**
```bash
# Validate JSON syntax
python3 -m json.tool your_file.json
```

**Problem: Schema validation fails**
```bash
# Install validation library
pip install jsonschema

# Use it in your code
from jsonschema import validate
```

## Resources

- JSON Schema: https://json-schema.org/
- JSON Schema Guide: https://json-schema.org/understanding-json-schema/
- Python jsonschema: https://python-jsonschema.readthedocs.io/

## Get Help

- Review the example files
- Read [WORKFLOW.md](WORKFLOW.md) for detailed steps
- Check [SCHEMAS.md](SCHEMAS.md) for field reference
- Open an issue on GitHub

---

**Ready to dive deeper?** Start with [README.md](README.md) for the full documentation!
