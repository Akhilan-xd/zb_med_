# Schema Overview and Metadata Fields

This document provides a detailed overview of each schema and the metadata fields they contain.

## Schema Comparison Table

| Feature | Patient Schema | Medical Record Schema | Clinical Study Schema |
|---------|---------------|----------------------|----------------------|
| Primary ID | patientId | recordId | studyId |
| ID Pattern | P-[0-9]{8} | MR-[0-9]{6} | CS-[0-9]{5} |
| Main Purpose | Patient demographics | Individual health records | Research study tracking |
| Metadata Richness | Medium | High | Very High |
| Relationships | Standalone | References patient | References multiple entities |

## Metadata Fields by Schema

### Patient Schema Metadata

Located in `metadata` object:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| registrationDate | date-time | When patient was registered | "2020-01-10T09:00:00Z" |
| lastVisit | date-time | Most recent visit | "2024-01-15T10:30:00Z" |
| status | enum | Patient status | "active", "inactive", "deceased" |
| recordSource | string | System that created record | "hospital_registration_system" |

**Additional Implicit Metadata:**
- Personal info (DOB provides age calculation)
- Contact status (presence of email/phone)
- Insurance coverage status
- Emergency contact availability

### Medical Record Schema Metadata

Located in `metadata` object:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| createdBy | string | User/system that created record | "system_user" |
| createdAt | date-time | Creation timestamp | "2024-01-15T10:30:00Z" |
| lastModified | date-time | Last modification timestamp | "2024-01-15T10:30:00Z" |
| version | string | Record version | "1.0" |
| tags | array[string] | Categorization tags | ["cardiology", "routine"] |

**Additional Implicit Metadata:**
- Provider information (who created/owns the record)
- Facility context (where record was created)
- Record type classification
- Temporal information (when event occurred)
- Patient linkage (connection to patient record)

### Clinical Study Schema Metadata

Located in `metadata` object:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| createdAt | date-time | Study record creation | "2023-12-01T08:00:00Z" |
| lastUpdated | date-time | Last update timestamp | "2024-01-15T14:30:00Z" |
| version | string | Schema/data version | "2.1" |
| dataSource | string | Origin system | "clinical_trials_registry" |
| qualityScore | number (0-100) | Data quality metric | 92.5 |

**Additional Implicit Metadata:**
- Study lifecycle (dates show progression)
- Enrollment metrics (target vs actual)
- Research team information
- Organizational affiliations
- Condition and intervention classifications
- Regulatory phase information

## Metadata Extraction Strategies

### 1. Direct Extraction
Metadata explicitly defined in a `metadata` object:
```json
{
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### 2. Derived Metadata
Calculated from other fields:
- Age from date of birth
- Duration from start/end dates
- Progress from target/actual enrollment
- Completeness from required field presence

### 3. Contextual Metadata
Inferred from relationships and structure:
- Record ownership (provider ID)
- Data lineage (record source)
- Classification (record type, study phase)
- Status (active, completed, etc.)

### 4. System Metadata
Added by processing systems:
- Extraction timestamp
- Validation results
- Quality scores
- Processing history

## Metadata Generation Workflow Details

### Phase 1: Schema Design
```
Define Requirements → Identify Entities → Design Structure
         ↓
    Add Constraints → Document Fields → Review & Validate
```

### Phase 2: Data Creation
```
Collect Data → Validate Format → Embed Metadata
      ↓
  Link Records → Set Timestamps → Apply Standards
```

### Phase 3: Metadata Extraction
```
Load Schema → Load Data → Parse Structure
     ↓
Extract Metadata → Validate Rules → Generate Report
```

### Phase 4: Usage & Maintenance
```
Query Metadata → Monitor Quality → Update Schemas
      ↓
  Version Control → Archive Old → Migrate Data
```

## Best Practices for Each Schema Type

### Patient Schema
✅ **DO:**
- Always include registration date
- Track status changes
- Maintain contact info currency
- Link to data source

❌ **DON'T:**
- Store medical details here (use medical records)
- Mix clinical and administrative data
- Forget to update last visit timestamp

### Medical Record Schema
✅ **DO:**
- Include provider and facility context
- Tag records for categorization
- Version all changes
- Maintain audit trail

❌ **DON'T:**
- Create orphaned records (always link to patient)
- Skip timestamp updates
- Omit record type classification

### Clinical Study Schema
✅ **DO:**
- Track all study lifecycle dates
- Monitor enrollment progress
- Document all team members
- Rate data quality

❌ **DON'T:**
- Leave sponsor information incomplete
- Forget to update status
- Skip version increments on changes

## Metadata Quality Checklist

Use this checklist to ensure metadata completeness:

### Completeness
- [ ] All required metadata fields present
- [ ] Timestamps follow ISO 8601 format
- [ ] IDs match defined patterns
- [ ] Enums use valid values

### Accuracy
- [ ] Dates are logical (no future dates for past events)
- [ ] Relationships are valid (referenced IDs exist)
- [ ] Status reflects actual state
- [ ] Versions increment properly

### Consistency
- [ ] Same entity represented uniformly
- [ ] Timestamps maintain chronological order
- [ ] Terminology is standardized
- [ ] Formats match across records

### Currency
- [ ] Last modified dates are recent
- [ ] Status is current
- [ ] Contact info is valid
- [ ] Links are not broken

## Common Metadata Patterns

### Temporal Metadata Pattern
```json
{
  "metadata": {
    "createdAt": "2024-01-15T10:00:00Z",
    "lastModified": "2024-01-15T10:30:00Z",
    "effectiveFrom": "2024-01-15T00:00:00Z",
    "effectiveTo": null
  }
}
```

### Ownership Metadata Pattern
```json
{
  "metadata": {
    "createdBy": "user123",
    "ownedBy": "department_cardiology",
    "organization": "hospital_001"
  }
}
```

### Versioning Metadata Pattern
```json
{
  "metadata": {
    "version": "2.1.0",
    "schemaVersion": "1.0",
    "previousVersion": "2.0.0",
    "changeLog": "Updated patient contact fields"
  }
}
```

### Quality Metadata Pattern
```json
{
  "metadata": {
    "completeness": 0.95,
    "accuracy": 0.98,
    "qualityScore": 92.5,
    "lastValidated": "2024-01-15T10:00:00Z"
  }
}
```

## Extending the Schemas

To add new metadata fields:

1. **Update the schema file** with new property definition
2. **Increment schema version** in the schema metadata
3. **Update example files** to include new fields
4. **Modify extraction script** if custom processing needed
5. **Document changes** in this file and README

Example addition:
```json
{
  "properties": {
    "metadata": {
      "properties": {
        "newField": {
          "type": "string",
          "description": "Purpose of new field"
        }
      }
    }
  }
}
```

## Related Standards

- **ISO 8601**: Date and time formats
- **HL7 FHIR**: Healthcare interoperability standards  
- **Dublin Core**: General metadata standard
- **JSON Schema**: Schema definition standard
- **OpenAPI**: API metadata standard

---

For questions about schema design or metadata extraction, refer to the main README.md or review the example files.
