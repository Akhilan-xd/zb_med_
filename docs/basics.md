## Basics and Terminologies

### **Schema**
A **schema** defines the structure, organization, and rules for how data is stored and represented.  
It provides a common set of variables and formats across different domains, allowing both humans and machines to understand and extract information easily.

**Key Points:**
- Controlled vocabularies  
- Discipline-specific  
- Founded by Google, Yahoo, Microsoft, Yandex, and GitHub contributors<sup>[1]</sup>

---

### **Schema Vocabulary Overview**
The schemas are a set of *types*, each associated with a set of *properties*.  
The current vocabulary consists of:

| Category | Count |
|-----------|-------:|
| **Types** | 817 |
| **Properties** | 1,518 |
| **Datatypes** | 14 |
| **Enumerations** | 94 |
| **Enumeration Members** | 521 |

---

## Project API vs. REST API Comparison

| Feature / Metadata | Project API | REST API | Notes |
|--------------------|--------------|-----------|--------|
| Project Name | Usually available | Available via `/projects` endpoint | Both provide project name |
| Description | Often included | Typically included | Short text about the project |
| README / Documentation | Can fetch full README content | Sometimes only metadata; README may need a separate endpoint (`/repos/{owner}/{repo}/readme`) | Project API may aggregate info |
| Owner / Creator | Included | Included | Username or organization |
| Tags / Topics | Often available | Sometimes via `/topics` endpoint | Useful for categorization |
| Version / Branch Info | Often included | Available via `/branches` or `/tags` | Might need separate call in REST API |
| License Info | Often included | Available via `/license` endpoint | REST may need a specific request |
| Contributors | Often included | Available via `/contributors` | Shows who worked on project |
| Languages / Tech Stack | Sometimes included | Available via `/languages` endpoint | Can differ based on API |
| Issues / Tickets | Often included | Available via `/issues` endpoint | REST may require pagination |
| Pull Requests / Merge Requests | Often included | Available via `/pulls` endpoint | REST API usually paginated |
| Project Stats (stars, forks) | Available | Available via `/repos` endpoint | Metrics about popularity |
| Activity / Events | Sometimes included | Available via `/events` endpoint | Can include commits, pushes, etc. |

---

### Key Differences
- **Project API**: Higher-level and often aggregates multiple data points (e.g., README, metadata, and tags in one call).  
- **REST API**: More granular and modular — multiple endpoints are usually needed to gather equivalent data.  
- **Project API** is ideal for summaries, while **REST API** gives more flexibility and fine control.
