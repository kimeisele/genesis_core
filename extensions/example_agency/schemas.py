"""
Example Agency - Schema Definitions

Defines all domain schemas using ONLY core.schema.

This file shows how domain-specific logic is built as an extension layer.
"""

from genesis_core import schema


def setup_schemas():
    """
    Define all agency domain schemas.

    Returns:
        dict: Schema definitions
    """

    # Applicant schema
    applicant_schema = schema.define_schema("Applicant", {
        "name": str,
        "email": str,
        "phone": str,
        "cv_path": str,
        "status": str  # "new", "screening", "interview", "hired", "rejected"
    })

    # Job schema
    job_schema = schema.define_schema("Job", {
        "title": str,
        "description": str,
        "department": str,
        "status": str  # "open", "closed"
    })

    # Interview schema
    interview_schema = schema.define_schema("Interview", {
        "applicant_id": str,
        "job_id": str,
        "scheduled_date": str,
        "interviewer": str,
        "notes": str,
        "result": str  # "pending", "pass", "fail"
    })

    # Application schema (links applicant to job)
    application_schema = schema.define_schema("Application", {
        "applicant_id": str,
        "job_id": str,
        "applied_date": str,
        "status": str  # "pending", "under_review", "accepted", "rejected"
    })

    return {
        "Applicant": applicant_schema,
        "Job": job_schema,
        "Interview": interview_schema,
        "Application": application_schema
    }


# Auto-setup on import
try:
    SCHEMAS = setup_schemas()
except KeyError:
    # Schemas already defined (e.g., in tests)
    pass
