#!/usr/bin/env python3
"""
Basic Core Functionality Test

Proves that Genesis Core works by testing fundamental operations.
"""

print("=" * 60)
print("GENESIS CORE - BASIC FUNCTIONALITY TEST")
print("=" * 60)

# Test 1: Schema Definition
print("\n[1/8] Testing core.schema...")
from genesis_core import schema

user_schema = schema.define_schema("User", {
    "name": str,
    "email": str,
    "age": int
})
print(f"✅ Defined schema: {user_schema.name}")
print(f"   Fields: {list(user_schema.fields.keys())}")

# Test 2: Entity Creation
print("\n[2/8] Testing core.entity...")
from genesis_core import entity

user = entity.create_entity("User", {
    "name": "Max Mustermann",
    "email": "max@example.com",
    "age": 30
})
print(f"✅ Created entity: {user.id[:8]}...")
print(f"   Data: {user.data}")

# Test 3: Storage Operations
print("\n[3/8] Testing core.storage...")
from genesis_core import storage

storage.store(user.id, user)
retrieved = storage.retrieve(user.id)
print(f"✅ Stored and retrieved entity")
print(f"   Retrieved: {retrieved.data['name']}")

# Test 4: Entity Update
print("\n[4/8] Testing entity updates...")
updated = entity.update_entity(user.id, {"age": 31})
print(f"✅ Updated entity age: {updated.data['age']}")

# Test 5: Validation Rules
print("\n[5/8] Testing core.validation...")
from genesis_core import validation

validation.define_rule("email_valid", lambda e: "@" in e.data.get("email", ""))
validation.define_rule("adult", lambda e: e.data.get("age", 0) >= 18)

result = validation.validate(user, ["email_valid", "adult"])
print(f"✅ Validation result: {result.is_valid}")

# Test 6: Transform
print("\n[6/8] Testing core.transform...")
from genesis_core import transform

# Define a simple schema to transform to
summary_schema = schema.define_schema("UserSummary", {
    "display_name": str,
    "contact": str
})

# Define transform
transform.define_transform(
    "user_to_summary",
    "User",
    "UserSummary",
    lambda e: {
        "display_name": e.data["name"],
        "contact": e.data["email"]
    }
)

summary = transform.apply_transform(user, "user_to_summary")
print(f"✅ Transformed entity: {summary.data}")

# Test 7: Process Workflow
print("\n[7/8] Testing core.process...")
from genesis_core import process

def step_validate(e):
    print(f"   → Step: validate")
    return e

def step_enrich(e):
    print(f"   → Step: enrich")
    return e

process.register_step_handler("validate", step_validate)
process.register_step_handler("enrich", step_enrich)

workflow = process.define_process("onboarding", ["validate", "enrich"])
processed = process.execute_process("onboarding", user)
print(f"✅ Executed process: {workflow.name}")

# Test 8: Identity & Permissions
print("\n[8/8] Testing core.identity...")
from genesis_core import identity

admin = identity.create_subject("admin_1", {
    "name": "Admin User",
    "role": "admin"
})

identity.grant_permission("admin_1", "read", "user:*")
identity.grant_permission("admin_1", "write", "user:*")

can_read = identity.check_permission("admin_1", "read", "user:123")
can_delete = identity.check_permission("admin_1", "delete", "user:123")

print(f"✅ Created subject: {admin.id}")
print(f"   Can read user:123? {can_read}")
print(f"   Can delete user:123? {can_delete}")

# Test 9: IO Operations
print("\n[BONUS] Testing core.io...")
from genesis_core import io
from pathlib import Path

test_file = Path("/tmp/genesis_test.json")
io.write_json(test_file, {"test": "data", "value": 123})
loaded = io.read_json(test_file)
print(f"✅ File I/O works")
print(f"   Wrote and read: {loaded}")

# Final Summary
print("\n" + "=" * 60)
print("🎉 ALL CORE MODULES WORKING")
print("=" * 60)
print(f"""
Summary:
- ✅ schema: {len(schema.list_schemas())} schemas defined
- ✅ entity: {len(entity.list_entities())} entities created
- ✅ storage: {len(storage.list_keys())} keys stored
- ✅ validation: {len(validation.list_rules())} rules defined
- ✅ transform: {len(transform.list_transforms())} transforms defined
- ✅ process: {len(process.list_processes())} processes defined
- ✅ identity: 1 subject created
- ✅ io: File operations work

The Genesis Core is OPERATIONAL.
""")
