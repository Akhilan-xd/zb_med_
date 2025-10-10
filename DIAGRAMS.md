# Visual Workflow Guide

This document provides visual representations of the schema and metadata extraction workflow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MEDICAL DATA SYSTEM ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐
│    DATA SOURCES         │
│  - EHR Systems          │
│  - Lab Systems          │
│  - Patient Portals      │
│  - Research DBs         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐       ┌──────────────────────┐
│   SCHEMA VALIDATION     │◄──────│  Schema Repository   │
│  - Check Structure      │       │  - patient_schema    │
│  - Validate Types       │       │  - record_schema     │
│  - Enforce Rules        │       │  - study_schema      │
└───────────┬─────────────┘       └──────────────────────┘
            │
            ▼
┌─────────────────────────┐
│  METADATA EXTRACTION    │
│  - Parse Data           │
│  - Extract Embedded     │
│  - Derive Calculated    │
│  - Generate Reports     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐       ┌──────────────────────┐
│    METADATA STORE       │◄─────►│   Search/Query       │
│  - Index Metadata       │       │   - Find Records     │
│  - Version History      │       │   - Filter Data      │
│  - Quality Metrics      │       │   - Generate Stats   │
└─────────────────────────┘       └──────────────────────┘
```

## Data Flow Diagram

```
INPUT DATA                PROCESSING                   OUTPUT
══════════════════════════════════════════════════════════════════════

┌──────────────┐
│ Patient Info │
│              │         ┌─────────────────┐
│ {            │────────►│ Load Schema     │
│   "id": "...",         │ (patient)       │
│   "name": ...,         └────────┬────────┘
│   "metadata": {...}             │
│ }            │                  ▼
└──────────────┘         ┌─────────────────┐         ┌──────────────┐
                         │ Validate Data   │────────►│ ✓ Valid      │
┌──────────────┐         │ - Required?     │         │ ✗ Invalid    │
│ Medical      │────────►│ - Type Match?   │         └──────────────┘
│ Record       │         │ - Constraints?  │
└──────────────┘         └────────┬────────┘
                                  │
┌──────────────┐                  ▼
│ Clinical     │         ┌─────────────────┐         ┌──────────────┐
│ Study        │────────►│ Extract         │────────►│ Metadata     │
└──────────────┘         │ Metadata        │         │ Report       │
                         │ - Embedded      │         │              │
                         │ - Derived       │         │ - Summary    │
                         │ - Contextual    │         │ - Stats      │
                         └─────────────────┘         │ - Quality    │
                                                      └──────────────┘
```

## Schema Validation Flow

```
START: Receive Data
      │
      ▼
┌─────────────────┐
│ Parse JSON      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Load Schema     │◄─────│ Schema Cache │
└────────┬────────┘      └──────────────┘
         │
         ▼
    ┌────────────────────────────┐
    │  Validation Checks         │
    ├────────────────────────────┤
    │  1. Required Fields        │───► Missing? → ERROR
    │  2. Data Types             │───► Wrong Type? → ERROR
    │  3. Format Patterns        │───► Invalid? → ERROR
    │  4. Value Constraints      │───► Out of Range? → ERROR
    │  5. Enum Values            │───► Not in List? → ERROR
    └────────┬───────────────────┘
             │
             ▼
        ┌─────────┐
   All  │ VALID?  │  Some
  Pass  └────┬────┘  Fail
        ┌────┴────┐
        │         │
        ▼         ▼
    ┌───────┐ ┌───────┐
    │SUCCESS│ │ ERROR │
    └───┬───┘ └───┬───┘
        │         │
        ▼         ▼
    Accept    Reject &
    Data      Report
```

## Metadata Extraction Process

```
DATA HIERARCHY                 METADATA TYPES               OUTPUT
════════════════════════════════════════════════════════════════════

Document Level
├── id: "12345"            ┌──────────────────┐
├── title: "..."     ─────►│ Descriptive      │─────► Catalog Entry
├── type: "patient"        │ - What it is     │       Summary Info
│                          └──────────────────┘
├── content: {...}         ┌──────────────────┐
│   ├── field1      ─────►│ Structural       │─────► Schema Map
│   ├── field2            │ - How organized  │       Data Model
│   └── field3            └──────────────────┘
│
└── metadata: {            ┌──────────────────┐
    ├── created     ─────►│ Administrative   │─────► Audit Log
    ├── modified          │ - Who/When/Where │       History
    ├── version           └──────────────────┘
    ├── status            ┌──────────────────┐
    └── quality     ─────►│ Quality          │─────► QA Report
                          │ - Completeness   │       Metrics
                          │ - Accuracy       │
                          └──────────────────┘

                          ┌──────────────────┐
  [Calculations]    ─────►│ Derived          │─────► Analytics
  - Age from DOB          │ - Computed       │       Insights
  - Duration              │ - Aggregated     │
  - Progress %            └──────────────────┘
```

## Complete Workflow Timeline

```
TIME    PHASE           ACTIVITY                    ARTIFACTS
═══════════════════════════════════════════════════════════════════════

T-0     DESIGN          Design Schema               schema.json
  │                     Define Fields               ├── properties
  │                     Set Constraints             ├── required
  │                     Document Purpose            └── descriptions
  ▼
T+1     IMPLEMENT       Create Examples             example.json
  │                     Write Validation            validate.py
  │                     Build Tools                 extract.py
  ▼
T+2     DEPLOY          Integrate System            production
  │                     Configure Pipeline          
  │                     Train Users                 
  ▼
T+3     OPERATE         Ingest Data                 data/
  │                     Validate Incoming           ├── validated/
  │                     Extract Metadata            └── metadata/
  │                     Index for Search
  ▼
T+4     MAINTAIN        Monitor Quality             reports/
  │                     Update Schemas              ├── quality.json
  │                     Fix Issues                  └── errors.log
  │                     Optimize Performance
  ▼
T+5     EVOLVE          Add Features                v2.0/
                        Migrate Data                migration/
                        Deprecate Old               archive/
```

## Schema Relationship Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    SCHEMA ECOSYSTEM                         │
└────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  Base Metadata   │
                    │   Schema         │
                    │ ┌──────────────┐ │
                    │ │ - createdAt  │ │
                    │ │ - modifiedAt │ │
                    │ │ - version    │ │
                    │ └──────────────┘ │
                    └────────┬─────────┘
                             │ (inherited by)
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  Patient     │  │  Medical     │  │  Clinical    │
    │  Schema      │  │  Record      │  │  Study       │
    ├──────────────┤  │  Schema      │  │  Schema      │
    │ + personalID │  ├──────────────┤  ├──────────────┤
    │ + name       │  │ + recordID   │  │ + studyID    │
    │ + DOB        │  │ + patientRef │──┼──┤ + subjects   │
    │ + contact    │  │ + provider   │  │ + phase      │
    │ + insurance  │  │ + facility   │  │ + enrollment │
    └──────────────┘  │ + type       │  └──────────────┘
                      └──────────────┘
                             │
                             │ (references)
                             ▼
                      ┌──────────────┐
                      │  Patient     │
                      │  Instance    │
                      └──────────────┘
```

## Metadata Quality Framework

```
QUALITY DIMENSIONS           MEASUREMENT              THRESHOLDS
══════════════════════════════════════════════════════════════════════

Completeness                 Required Fields          Target: 100%
├── Required Present     ─► Present / Total      ─►  Minimum: 95%
├── Optional Present     ─► Optional / Total     ─►  Good: 80%
└── Metadata Present     ─► Meta Fields / All    ─►  Excellent: 90%

Accuracy                     Validation Results       Target: 98%
├── Format Correct       ─► Valid Format / Total ─►  Minimum: 95%
├── Type Correct         ─► Correct Type / Total ─►  Critical: 100%
└── Range Valid          ─► In Range / Total     ─►  Good: 98%

Consistency                  Cross-Field Checks       Target: 100%
├── Dates Logical        ─► Valid Sequence       ─►  Required: 100%
├── IDs Match            ─► References Valid     ─►  Required: 100%
└── Status Coherent      ─► State Valid          ─►  Good: 98%

Timeliness                   Update Frequency         Target: Daily
├── Last Modified        ─► Days Since Update    ─►  Warning: >30d
├── Creation Date        ─► Delay from Event     ─►  Good: <1d
└── Version Current      ─► Versions Behind      ─►  Warning: >2

Overall Quality Score = Weighted Average of Dimensions
                       (Completeness × 0.3 + Accuracy × 0.4 + 
                        Consistency × 0.2 + Timeliness × 0.1)
```

## Usage Patterns

```
COMMON OPERATIONS               API CALLS                RESPONSE
═════════════════════════════════════════════════════════════════════

1. Validate New Data
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │ POST /data  │────────►│ Validate    │────────►│ 200 OK      │
   │ {data}      │         │ Extract     │         │ + metadata  │
   └─────────────┘         └─────────────┘         └─────────────┘

2. Query by Metadata
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │ GET /search │────────►│ Query Index │────────►│ Results[]   │
   │ ?status=... │         │ Filter      │         │ + metadata  │
   └─────────────┘         └─────────────┘         └─────────────┘

3. Generate Report
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │ GET /report │────────►│ Aggregate   │────────►│ Statistics  │
   │ ?type=...   │         │ Analyze     │         │ + charts    │
   └─────────────┘         └─────────────┘         └─────────────┘

4. Update Schema
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │ PUT /schema │────────►│ Validate    │────────►│ 200 Updated │
   │ {schema}    │         │ Migrate     │         │ + version   │
   └─────────────┘         └─────────────┘         └─────────────┘
```

## Error Handling Flow

```
                    ┌──────────────┐
                    │  Input Data  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Validate    │
                    └──────┬───────┘
                           │
               ┌───────────┴────────────┐
               │                        │
               ▼                        ▼
        ┌─────────────┐          ┌─────────────┐
        │   VALID     │          │  INVALID    │
        └──────┬──────┘          └──────┬──────┘
               │                        │
               ▼                        ▼
        ┌─────────────┐          ┌─────────────┐
        │  Extract    │          │  Categorize │
        │  Metadata   │          │  Error      │
        └──────┬──────┘          └──────┬──────┘
               │                        │
               ▼                  ┌─────┴──────┐
        ┌─────────────┐          │            │
        │  Store &    │          ▼            ▼
        │  Index      │    ┌──────────┐ ┌──────────┐
        └──────┬──────┘    │ Fixable  │ │ Critical │
               │           └────┬─────┘ └────┬─────┘
               ▼                │            │
        ┌─────────────┐         ▼            ▼
        │  Success    │    ┌──────────┐ ┌──────────┐
        │  Response   │    │  Queue   │ │  Reject  │
        └─────────────┘    │  Retry   │ │  Notify  │
                           └──────────┘ └──────────┘
```

## Implementation Checklist

```
☐ SETUP
  ☐ Clone repository
  ☐ Review schemas
  ☐ Test examples
  ☐ Run extraction tool

☐ CUSTOMIZATION
  ☐ Identify your entities
  ☐ Design custom schemas
  ☐ Create example data
  ☐ Validate examples

☐ INTEGRATION
  ☐ Add to data pipeline
  ☐ Configure validation
  ☐ Set up metadata store
  ☐ Enable search/query

☐ TESTING
  ☐ Test with real data
  ☐ Measure quality
  ☐ Fix issues
  ☐ Optimize performance

☐ DEPLOYMENT
  ☐ Document process
  ☐ Train team
  ☐ Monitor usage
  ☐ Iterate improvements
```

---

For detailed implementation steps, see [WORKFLOW.md](WORKFLOW.md)
For schema specifics, see [SCHEMAS.md](SCHEMAS.md)
For quick start, see [QUICKSTART.md](QUICKSTART.md)
