# Medical Data Schemas and Metadata Extraction

A comprehensive repository demonstrating the use of **JSON Schemas** for defining medical data structures and **automated metadata extraction** workflows.

## 📋 Table of Contents

- [Overview](#overview)
- [What are Schemas?](#what-are-schemas)
- [What is Metadata?](#what-is-metadata)
- [Repository Structure](#repository-structure)
- [Available Schemas](#available-schemas)
- [Metadata Generation Workflow](#metadata-generation-workflow)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)

## 🎯 Overview

This repository provides:
- **JSON Schema definitions** for common medical data types
- **Example data files** that conform to the schemas
- **Python scripts** for automated metadata extraction and validation
- **Documentation** on metadata generation workflows

## 🔍 What are Schemas?

**Schemas** are formal definitions that describe the structure, format, and constraints of data. Think of them as blueprints or contracts for your data.

### Benefits of Using Schemas:
- ✅ **Data Validation**: Ensure data meets required standards
- ✅ **Documentation**: Self-documenting data structures
- ✅ **Consistency**: Maintain uniform data across systems
- ✅ **Interoperability**: Enable data exchange between systems
- ✅ **Error Prevention**: Catch issues early in development

### JSON Schema Format:
We use [JSON Schema](https://json-schema.org/) (Draft 7), which provides:
- Type definitions (string, number, object, array, etc.)
- Validation rules (required fields, patterns, ranges)
- Documentation (descriptions, examples)
- Composition (reusable schema components)

## 📊 What is Metadata?

**Metadata** is "data about data" - information that describes and provides context about other data.

### Types of Metadata:
1. **Descriptive Metadata**: What the data is about (title, description, keywords)
2. **Structural Metadata**: How the data is organized (format, relationships)
3. **Administrative Metadata**: Who created it, when, version, access rights

### Why Metadata Matters:
- 🔎 **Discoverability**: Find relevant data quickly
- 📝 **Context**: Understand data origin and meaning
- 🔒 **Governance**: Track ownership and compliance
- 🔄 **Lifecycle Management**: Monitor data from creation to archive

## 📁 Repository Structure

```
zb_med_/
├── schemas/                      # JSON Schema definitions
│   ├── patient_schema.json       # Patient information schema
│   ├── medical_record_schema.json # Medical record schema
│   └── clinical_study_schema.json # Clinical study schema
├── examples/                     # Example data files
│   ├── patient_example.json
│   ├── medical_record_example.json
│   └── clinical_study_example.json
├── scripts/                      # Metadata extraction tools
│   └── extract_metadata.py       # Python metadata extractor
└── README.md                     # This file
```

## 📚 Available Schemas

### 1. Patient Schema (`patient_schema.json`)
Defines the structure for patient information including:
- Personal information (name, DOB, gender, blood type)
- Contact details (email, phone, address)
- Emergency contacts
- Insurance information
- Registration and visit metadata

### 2. Medical Record Schema (`medical_record_schema.json`)
Defines the structure for medical records including:
- Record identification
- Patient information reference
- Healthcare provider details
- Facility information
- Record type and timestamps
- Administrative metadata

### 3. Clinical Study Schema (`clinical_study_schema.json`)
Defines the structure for clinical research studies including:
- Study identification and title
- Study status and phase
- Enrollment information
- Sponsors and investigators
- Conditions and interventions
- Quality and version metadata

## 🔄 Metadata Generation Workflow

### Step 1: Define Schema
Create a JSON Schema that describes your data structure with validation rules.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Your Data Type",
  "type": "object",
  "required": ["id", "name"],
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string"},
    "metadata": {
      "type": "object",
      "properties": {
        "createdAt": {"type": "string", "format": "date-time"},
        "version": {"type": "string"}
      }
    }
  }
}
```

### Step 2: Create Data Instance
Create data that conforms to your schema.

```json
{
  "id": "12345",
  "name": "Sample Record",
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### Step 3: Extract Metadata
Use automated tools to extract and validate metadata:

```bash
python scripts/extract_metadata.py
```

### Step 4: Validate and Use
The extraction process:
1. Loads the schema and data
2. Validates data against schema rules
3. Extracts embedded metadata
4. Generates summary information
5. Produces a metadata report

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Basic understanding of JSON

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Akhilan-xd/zb_med_.git
cd zb_med_
```

2. (Optional) For advanced validation, install jsonschema:
```bash
pip install jsonschema
```

### Quick Start

Run the metadata extraction tool:
```bash
python scripts/extract_metadata.py
```

This will process all example files and generate metadata reports.

## 💡 Usage Examples

### Example 1: Validate Patient Data

```python
import json

# Load schema
with open('schemas/patient_schema.json') as f:
    schema = json.load(f)

# Load data
with open('examples/patient_example.json') as f:
    patient = json.load(f)

# Extract metadata
print(f"Patient ID: {patient['patientId']}")
print(f"Status: {patient['metadata']['status']}")
print(f"Last Visit: {patient['metadata']['lastVisit']}")
```

### Example 2: Extract Medical Record Metadata

```python
import json

with open('examples/medical_record_example.json') as f:
    record = json.load(f)

metadata = {
    "record_id": record['recordId'],
    "patient": record['patientInfo']['patientId'],
    "type": record['recordType'],
    "date": record['recordDate'],
    "provider": record['provider']['name']
}

print(f"Record Metadata: {json.dumps(metadata, indent=2)}")
```

### Example 3: Programmatic Validation

```bash
# Run the extraction script
python scripts/extract_metadata.py

# Output will show:
# - Schema information
# - Data summary
# - Embedded metadata
# - Validation results
```

## 🎯 Use Cases

### Healthcare Systems
- **Patient Management**: Validate patient registration data
- **EHR Integration**: Ensure consistent medical record formats
- **Data Exchange**: Facilitate interoperability between systems

### Research
- **Clinical Trials**: Standardize study metadata
- **Data Collection**: Ensure research data quality
- **Publication**: Generate metadata for datasets

### Compliance
- **HIPAA**: Track data access and modifications
- **Audit Trails**: Maintain comprehensive metadata logs
- **Quality Assurance**: Validate data meets regulatory standards

### Data Management
- **ETL Pipelines**: Validate data during ingestion
- **Data Catalogs**: Auto-generate data documentation
- **Version Control**: Track data schema evolution

## ✨ Best Practices

### Schema Design
1. **Be Specific**: Define precise validation rules (patterns, ranges, enums)
2. **Document Everything**: Add descriptions to all properties
3. **Use Standards**: Follow established formats (ISO dates, email, URIs)
4. **Plan for Change**: Design schemas that can evolve
5. **Reuse Components**: Use `$ref` for common patterns

### Metadata Management
1. **Automate Generation**: Use tools to extract metadata automatically
2. **Standardize Formats**: Use ISO standards (8601 for dates)
3. **Version Everything**: Track schema and data versions
4. **Include Context**: Record who, when, where, why
5. **Validate Regularly**: Check metadata completeness and accuracy

### Implementation
1. **Start Simple**: Begin with basic schemas and expand
2. **Test Thoroughly**: Validate with real-world data
3. **Document Workflows**: Explain how to use schemas and tools
4. **Monitor Quality**: Track validation errors and warnings
5. **Iterate**: Refine schemas based on feedback and usage

## 🔗 Additional Resources

- [JSON Schema Specification](https://json-schema.org/)
- [Understanding JSON Schema Guide](https://json-schema.org/understanding-json-schema/)
- [Schema Validation Tools](https://json-schema.org/implementations.html)
- [FHIR Healthcare Standards](https://www.hl7.org/fhir/)
- [Dublin Core Metadata Initiative](https://www.dublincore.org/)

## 📄 License

This project is provided as-is for educational and reference purposes.

## 🤝 Contributing

Feel free to suggest improvements or additional schemas that would be valuable for the medical informatics community.

---

**Questions or Issues?** Open an issue on GitHub or refer to the examples and scripts provided.