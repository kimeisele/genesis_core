"""
Example Agency - Workflow Definitions

Defines hiring workflows using ONLY core.process, core.validation, and core.transform.

This demonstrates how complex business logic is implemented without touching the core.
"""

from genesis_core import process, validation, entity


def setup_validation_rules():
    """
    Define validation rules for applicants.

    Returns:
        list[str]: List of rule names
    """

    # Email validation
    validation.define_rule(
        "email_valid",
        lambda e: "@" in e.data.get("email", "")
    )

    # Phone validation
    validation.define_rule(
        "phone_valid",
        lambda e: len(e.data.get("phone", "")) >= 10
    )

    # CV exists
    validation.define_rule(
        "has_cv",
        lambda e: len(e.data.get("cv_path", "")) > 0
    )

    # Status validation
    validation.define_rule(
        "valid_applicant_status",
        lambda e: e.data.get("status") in ["new", "screening", "interview", "hired", "rejected"]
    )

    return ["email_valid", "phone_valid", "has_cv", "valid_applicant_status"]


def setup_hiring_process():
    """
    Define the hiring process workflow.

    Returns:
        str: Process name
    """

    # Define step handlers
    def step_validate_applicant(e: entity.Entity) -> entity.Entity:
        """Validate applicant data."""
        print(f"   [Step] Validating applicant: {e.data['name']}")

        result = validation.validate(e, ["email_valid", "phone_valid", "has_cv"])

        if not result.is_valid:
            print(f"   ❌ Validation failed: {result.errors}")
            e.data["status"] = "rejected"
        else:
            print(f"   ✅ Validation passed")

        return e

    def step_screen_applicant(e: entity.Entity) -> entity.Entity:
        """Screen applicant CV."""
        print(f"   [Step] Screening applicant: {e.data['name']}")

        # In real system, this would check CV content
        # For demo, we just update status
        if e.data["status"] != "rejected":
            e.data["status"] = "screening"
            print(f"   ✅ Moved to screening")

        return e

    def step_schedule_interview(e: entity.Entity) -> entity.Entity:
        """Schedule interview."""
        print(f"   [Step] Scheduling interview for: {e.data['name']}")

        if e.data["status"] == "screening":
            e.data["status"] = "interview"
            print(f"   ✅ Interview scheduled")

        return e

    # Register step handlers
    process.register_step_handler("validate_applicant", step_validate_applicant)
    process.register_step_handler("screen_applicant", step_screen_applicant)
    process.register_step_handler("schedule_interview", step_schedule_interview)

    # Define the hiring process
    hiring_process = process.define_process("hiring", [
        "validate_applicant",
        "screen_applicant",
        "schedule_interview"
    ])

    return hiring_process.name


def apply_for_job(applicant_data: dict) -> str:
    """
    Main entry point: Apply for a job.

    Args:
        applicant_data: Dictionary with applicant information

    Returns:
        str: Result message
    """

    try:
        # Create applicant entity
        applicant = entity.create_entity("Applicant", applicant_data)
        print(f"\n📋 Processing applicant: {applicant.data['name']}")

        # Execute hiring process
        processed = process.execute_process("hiring", applicant)

        # Return result based on final status
        final_status = processed.data["status"]

        if final_status == "interview":
            return f"✅ Applicant {applicant.data['name']} successfully processed → Interview scheduled"
        elif final_status == "rejected":
            return f"❌ Applicant {applicant.data['name']} rejected during validation"
        else:
            return f"⏳ Applicant {applicant.data['name']} in status: {final_status}"

    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except KeyError as e:
        return f"❌ Error: {str(e)}"


# Track initialization state
_initialized = False


def initialize():
    """Initialize workflows (call this once)."""
    global _initialized

    if _initialized:
        return

    try:
        setup_validation_rules()
        setup_hiring_process()
        _initialized = True
        print("[Agency] Workflows initialized")
    except KeyError:
        # Already initialized (in case of concurrent calls)
        _initialized = True


# Auto-initialize on import
initialize()
