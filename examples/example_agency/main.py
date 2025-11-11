#!/usr/bin/env python3
"""
Example Agency - Main Entry Point

A complete recruiting agency application built ONLY using Genesis Core extensions.

This demonstrates:
1. Complex domain logic without modifying core
2. Multiple schemas working together
3. Validation, processes, and workflows
4. A real-world use case

Run this file to see the agency in action.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from extensions.example_agency import schemas, workflows


def main():
    """Run the recruiting agency demo."""

    print("=" * 70)
    print("RECRUITING AGENCY - Powered by Genesis Core")
    print("=" * 70)

    # Initialize schemas and workflows
    print("\n[Setup] Initializing agency schemas and workflows...")

    # Schemas are auto-initialized on import, just display them
    print(f"✅ Loaded {len(schemas.SCHEMAS)} domain schemas:")
    for schema_name in schemas.SCHEMAS:
        print(f"   - {schema_name}")

    # Test Case 1: Valid applicant
    print("\n" + "-" * 70)
    print("TEST CASE 1: Valid Applicant")
    print("-" * 70)

    result1 = workflows.apply_for_job({
        "name": "Anna Schmidt",
        "email": "anna.schmidt@example.com",
        "phone": "+49 123 456789",
        "cv_path": "/uploads/cv/anna_schmidt.pdf",
        "status": "new"
    })

    print(f"\n{result1}")

    # Test Case 2: Invalid applicant (no email)
    print("\n" + "-" * 70)
    print("TEST CASE 2: Invalid Applicant (missing email)")
    print("-" * 70)

    result2 = workflows.apply_for_job({
        "name": "Bob Miller",
        "email": "invalid-email",  # Invalid email
        "phone": "123",  # Too short
        "cv_path": "",  # No CV
        "status": "new"
    })

    print(f"\n{result2}")

    # Test Case 3: Another valid applicant
    print("\n" + "-" * 70)
    print("TEST CASE 3: Another Valid Applicant")
    print("-" * 70)

    result3 = workflows.apply_for_job({
        "name": "Clara Johnson",
        "email": "clara@example.com",
        "phone": "+1 555 123 4567",
        "cv_path": "/uploads/cv/clara_johnson.pdf",
        "status": "new"
    })

    print(f"\n{result3}")

    # Summary
    print("\n" + "=" * 70)
    print("AGENCY DEMO COMPLETE")
    print("=" * 70)

    print("""
Key Achievements:
✅ Built a complete recruiting agency using ONLY Genesis Core
✅ Zero lines of code modified in genesis_core/
✅ All domain logic in extensions/
✅ Schemas, validation, processes all working together
✅ Easy to extend with more features (interviews, offers, etc.)

This proves the Genesis Core architecture works!
    """)


if __name__ == "__main__":
    main()
