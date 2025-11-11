"""
Example Agency - Recruiting Application

A complete recruiting agency application built ONLY using Genesis Core.

This demonstrates that complex domain logic can be built entirely through
extensions without EVER modifying the core.

Architecture:
- schemas.py: Defines domain schemas (Applicant, Job, Interview)
- workflows.py: Defines hiring processes using core.process
- main.py: Entry point that ties everything together
"""

__version__ = "1.0.0"
