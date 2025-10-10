#!/usr/bin/env python3
"""
Metadata Extractor and Validator

This script demonstrates how to extract and validate metadata from JSON data
using JSON Schema definitions.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None


def extract_metadata(data: Dict[str, Any], schema_type: str) -> Dict[str, Any]:
    """
    Extract metadata from the data based on schema type.
    
    Args:
        data: The data dictionary to extract metadata from
        schema_type: Type of schema (patient, medical_record, clinical_study)
    
    Returns:
        Dictionary containing extracted metadata
    """
    metadata = {
        "extraction_timestamp": datetime.utcnow().isoformat() + "Z",
        "schema_type": schema_type,
        "data_summary": {}
    }
    
    # Extract specific metadata based on schema type
    if schema_type == "patient":
        metadata["data_summary"] = {
            "patient_id": data.get("patientId"),
            "name": f"{data.get('personalInfo', {}).get('firstName', '')} {data.get('personalInfo', {}).get('lastName', '')}",
            "status": data.get("metadata", {}).get("status"),
            "last_visit": data.get("metadata", {}).get("lastVisit")
        }
        
    elif schema_type == "medical_record":
        metadata["data_summary"] = {
            "record_id": data.get("recordId"),
            "patient_id": data.get("patientInfo", {}).get("patientId"),
            "record_type": data.get("recordType"),
            "record_date": data.get("recordDate"),
            "provider": data.get("provider", {}).get("name")
        }
        
    elif schema_type == "clinical_study":
        metadata["data_summary"] = {
            "study_id": data.get("studyId"),
            "title": data.get("title"),
            "status": data.get("status"),
            "phase": data.get("phase"),
            "enrollment_progress": f"{data.get('enrollment', {}).get('actual', 0)}/{data.get('enrollment', {}).get('target', 0)}"
        }
    
    # Extract embedded metadata if present
    if "metadata" in data:
        metadata["embedded_metadata"] = data["metadata"]
    
    return metadata


def validate_schema_structure(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic validation of data against schema structure.
    
    Note: This is a simplified validation. For production use,
    consider using jsonschema library: pip install jsonschema
    """
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check required fields
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in data:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Missing required field: {field}")
    
    # Check field types (basic check)
    properties = schema.get("properties", {})
    for field_name, field_value in data.items():
        if field_name in properties:
            expected_type = properties[field_name].get("type")
            actual_type = type(field_value).__name__
            
            # Map Python types to JSON Schema types
            type_mapping = {
                "str": "string",
                "int": "integer",
                "float": "number",
                "bool": "boolean",
                "dict": "object",
                "list": "array",
                "NoneType": "null"
            }
            
            actual_json_type = type_mapping.get(actual_type, actual_type)
            if expected_type and actual_json_type != expected_type:
                validation_result["warnings"].append(
                    f"Type mismatch for '{field_name}': expected {expected_type}, got {actual_json_type}"
                )
    
    return validation_result


def generate_metadata_report(data: Dict[str, Any], schema: Dict[str, Any], 
                             schema_type: str) -> str:
    """Generate a comprehensive metadata report."""
    
    # Extract metadata
    metadata = extract_metadata(data, schema_type)
    
    # Validate data
    validation = validate_schema_structure(data, schema)
    
    # Build report
    report = []
    report.append("=" * 70)
    report.append(f"METADATA EXTRACTION REPORT - {schema_type.upper()}")
    report.append("=" * 70)
    report.append("")
    
    report.append("Schema Information:")
    report.append(f"  Schema Title: {schema.get('title', 'N/A')}")
    report.append(f"  Schema ID: {schema.get('$id', 'N/A')}")
    report.append(f"  Description: {schema.get('description', 'N/A')}")
    report.append("")
    
    report.append("Extraction Details:")
    report.append(f"  Timestamp: {metadata['extraction_timestamp']}")
    report.append(f"  Schema Type: {metadata['schema_type']}")
    report.append("")
    
    report.append("Data Summary:")
    for key, value in metadata['data_summary'].items():
        report.append(f"  {key}: {value}")
    report.append("")
    
    if "embedded_metadata" in metadata:
        report.append("Embedded Metadata:")
        for key, value in metadata['embedded_metadata'].items():
            report.append(f"  {key}: {value}")
        report.append("")
    
    report.append("Validation Results:")
    report.append(f"  Valid: {validation['valid']}")
    if validation['errors']:
        report.append("  Errors:")
        for error in validation['errors']:
            report.append(f"    - {error}")
    if validation['warnings']:
        report.append("  Warnings:")
        for warning in validation['warnings']:
            report.append(f"    - {warning}")
    if not validation['errors'] and not validation['warnings']:
        report.append("  No issues found!")
    report.append("")
    
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    """Main function to demonstrate metadata extraction."""
    
    # Define paths
    base_path = Path(__file__).parent.parent
    schemas_path = base_path / "schemas"
    examples_path = base_path / "examples"
    
    # Process each schema type
    schema_types = [
        ("patient", "patient_schema.json", "patient_example.json"),
        ("medical_record", "medical_record_schema.json", "medical_record_example.json"),
        ("clinical_study", "clinical_study_schema.json", "clinical_study_example.json")
    ]
    
    print("\n" + "=" * 70)
    print("METADATA EXTRACTION TOOL")
    print("=" * 70)
    print("\nProcessing schemas and examples...\n")
    
    for schema_type, schema_file, example_file in schema_types:
        schema_path = schemas_path / schema_file
        example_path = examples_path / example_file
        
        # Load schema and data
        schema = load_json_file(str(schema_path))
        data = load_json_file(str(example_path))
        
        if schema and data:
            report = generate_metadata_report(data, schema, schema_type)
            print(report)
            print()
        else:
            print(f"Skipping {schema_type} due to loading errors.\n")
    
    print("Metadata extraction complete!")
    print()


if __name__ == "__main__":
    main()
