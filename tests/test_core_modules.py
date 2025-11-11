"""
Comprehensive tests for Genesis Core modules.

Tests the ACTUAL API of all core modules, ensuring they work correctly.
"""

import pytest
import tempfile
from pathlib import Path
from genesis_core import io, storage, schema, entity, transform, process, validation, identity


class TestIO:
    """Test genesis_core.io module - File I/O operations"""

    def test_read_write_text(self):
        """Test text file read/write cycle"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "Hello, World!"

            io.write_text(file_path, content)
            result = io.read_text(file_path)

            assert result == content

    def test_read_write_json(self):
        """Test JSON file read/write cycle"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            data = {"key": "value", "number": 42}

            io.write_json(file_path, data)
            result = io.read_json(file_path)

            assert result == data

    def test_exists(self):
        """Test path existence check"""
        with tempfile.TemporaryDirectory() as tmpdir:
            existing = Path(tmpdir) / "exists.txt"
            non_existing = Path(tmpdir) / "nope.txt"

            io.write_text(existing, "content")

            assert io.exists(existing) is True
            assert io.exists(non_existing) is False

    def test_list_files(self):
        """Test file listing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            (tmpdir_path / "file1.txt").write_text("content1")
            (tmpdir_path / "file2.txt").write_text("content2")
            (tmpdir_path / "file3.log").write_text("content3")

            all_files = io.list_files(tmpdir_path)
            txt_files = io.list_files(tmpdir_path, "*.txt")

            assert len(all_files) == 3
            assert len(txt_files) == 2


class TestStorage:
    """Test genesis_core.storage module - Key-value storage"""

    def test_store_and_retrieve(self):
        """Test store and retrieve cycle"""
        key = "test_key_123"
        data = {"test": "data", "value": 42}

        storage.store(key, data)
        result = storage.retrieve(key)

        assert result == data

    def test_exists(self):
        """Test key existence check"""
        storage.store("exists_key", {"data": "value"})

        assert storage.exists("exists_key") is True
        assert storage.exists("nonexistent_key") is False

    def test_delete(self):
        """Test deletion"""
        key = "delete_me"
        storage.store(key, {"data": "value"})

        assert storage.exists(key) is True
        storage.delete(key)
        assert storage.exists(key) is False

    def test_list_keys(self):
        """Test listing stored keys"""
        storage.store("key1", {"data": 1})
        storage.store("key2", {"data": 2})

        keys = storage.list_keys()
        assert "key1" in keys
        assert "key2" in keys

    def test_list_keys_with_prefix(self):
        """Test listing keys with prefix filter"""
        storage.store("test_prefix:1", {"data": 1})
        storage.store("test_prefix:2", {"data": 2})

        keys = storage.list_keys("test_prefix:")
        assert len([k for k in keys if k.startswith("test_prefix:")]) >= 2


class TestSchema:
    """Test genesis_core.schema module - Schema definitions"""

    def test_define_and_get_schema(self):
        """Test schema definition and retrieval"""
        schema_def = schema.define_schema("TestEntity", {"name": str, "age": int, "email": str})

        retrieved = schema.get_schema("TestEntity")

        assert retrieved.name == "TestEntity"
        assert "name" in retrieved.fields

    def test_validate_data_success(self):
        """Test successful data validation"""
        schema.define_schema("ValidTest", {"field1": str, "field2": int})

        result = schema.validate_data("ValidTest", {"field1": "value", "field2": 42})

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_data_failure(self):
        """Test failed data validation"""
        schema.define_schema("InvalidTest", {"required_field": str})

        result = schema.validate_data("InvalidTest", {"wrong_field": "value"})

        assert result.is_valid is False
        assert len(result.errors) > 0

    def test_list_schemas(self):
        """Test listing all schemas"""
        schema.define_schema("Schema1", {"field": str})
        schema.define_schema("Schema2", {"field": int})

        schemas = schema.list_schemas()

        assert "Schema1" in schemas
        assert "Schema2" in schemas


class TestEntity:
    """Test genesis_core.entity module - Entity CRUD"""

    def test_create_entity(self):
        """Test entity creation"""
        # Define schema first
        schema.define_schema("Person", {"name": str, "age": int})

        entity_obj = entity.create_entity("Person", {"name": "Alice", "age": 30})

        assert entity_obj.schema_name == "Person"
        assert entity_obj.data["name"] == "Alice"
        assert entity_obj.data["age"] == 30
        assert entity_obj.id is not None

    def test_get_entity(self):
        """Test entity retrieval"""
        schema.define_schema("Product", {"name": str, "price": int})

        created = entity.create_entity("Product", {"name": "Widget", "price": 999})

        retrieved = entity.get_entity(created.id)

        assert retrieved.id == created.id
        assert retrieved.data == created.data

    def test_update_entity(self):
        """Test entity update"""
        schema.define_schema("UpdateTest", {"value": int})

        created = entity.create_entity("UpdateTest", {"value": 10})
        updated = entity.update_entity(created.id, {"value": 20})

        assert updated.data["value"] == 20

    def test_delete_entity(self):
        """Test entity deletion"""
        schema.define_schema("DeleteTest", {"field": str})

        created = entity.create_entity("DeleteTest", {"field": "value"})
        entity.delete_entity(created.id)

        with pytest.raises(KeyError):
            entity.get_entity(created.id)

    def test_list_entities(self):
        """Test listing entities by schema"""
        schema.define_schema("ListTest", {"name": str})

        entity.create_entity("ListTest", {"name": "Entity1"})
        entity.create_entity("ListTest", {"name": "Entity2"})

        entities = entity.list_entities("ListTest")

        assert len(entities) >= 2


class TestTransform:
    """Test genesis_core.transform module - Data transformation"""

    def test_define_and_apply_transform(self):
        """Test transformation definition and application"""
        schema.define_schema("Source", {"value": int})
        schema.define_schema("Target", {"doubled": int})

        # Define transformation
        transform.define_transform(
            "double_value", "Source", "Target", lambda e: {"doubled": e.data["value"] * 2}
        )

        # Create source entity
        source = entity.create_entity("Source", {"value": 10})

        # Apply transformation
        result = transform.apply_transform(source, "double_value")

        assert result.data["doubled"] == 20

    def test_list_transforms(self):
        """Test listing all transforms"""
        transforms = transform.list_transforms()
        assert isinstance(transforms, list)


class TestProcess:
    """Test genesis_core.process module - Workflow/process management"""

    def test_define_and_execute_process(self):
        """Test process definition and execution"""
        schema.define_schema("ProcessTest", {"value": int})

        # Define step handlers
        def step1(e):
            e.data["value"] += 10
            return e

        def step2(e):
            e.data["value"] *= 2
            return e

        # Register handlers
        process.register_step_handler("add_ten", step1)
        process.register_step_handler("double", step2)

        # Define process
        process.define_process("math_process", ["add_ten", "double"])

        # Create entity and execute
        test_entity = entity.create_entity("ProcessTest", {"value": 5})
        result = process.execute_process("math_process", test_entity)

        # (5 + 10) * 2 = 30
        assert result.data["value"] == 30

    def test_list_processes(self):
        """Test listing all processes"""
        processes = process.list_processes()
        assert isinstance(processes, list)


class TestValidation:
    """Test genesis_core.validation module - Validation rules"""

    def test_define_and_validate_rule(self):
        """Test rule definition and validation"""
        schema.define_schema("ValidationTest", {"age": int})

        # Define rule
        validation.define_rule(
            "is_adult",
            lambda e: e.data.get("age", 0) >= 18,
        )

        # Test with valid entity
        adult = entity.create_entity("ValidationTest", {"age": 25})
        result_valid = validation.validate(adult, ["is_adult"])

        assert result_valid.is_valid is True

        # Test with invalid entity
        child = entity.create_entity("ValidationTest", {"age": 10})
        result_invalid = validation.validate(child, ["is_adult"])

        assert result_invalid.is_valid is False
        assert len(result_invalid.errors) > 0

    def test_list_rules(self):
        """Test listing all rules"""
        rules = validation.list_rules()
        assert isinstance(rules, list)


class TestIdentity:
    """Test genesis_core.identity module - Auth/permissions"""

    def test_create_and_get_subject(self):
        """Test subject creation and retrieval"""
        subject = identity.create_subject(
            "user123", {"name": "Alice", "email": "alice@example.com"}
        )

        retrieved = identity.get_subject("user123")

        assert retrieved.id == "user123"
        assert retrieved.attributes["name"] == "Alice"

    def test_grant_and_check_permission(self):
        """Test permission granting and checking"""
        identity.create_subject("admin", {"name": "Admin"})

        # Grant permissions
        identity.grant_permission("admin", "read", "doc:*")
        identity.grant_permission("admin", "write", "doc:*")

        # Check permissions
        assert identity.check_permission("admin", "read", "doc:123") is True
        assert identity.check_permission("admin", "write", "doc:456") is True
        assert identity.check_permission("admin", "delete", "doc:789") is False

    def test_list_permissions(self):
        """Test listing subject permissions"""
        identity.create_subject("test_user", {"name": "Test"})
        identity.grant_permission("test_user", "read", "file:*")

        permissions = identity.list_permissions("test_user")

        assert len(permissions) >= 1
        assert permissions[0].action == "read"


class TestIntegration:
    """Integration tests combining multiple modules"""

    def test_full_entity_workflow(self):
        """Test complete workflow: schema, entity, validation, transform"""
        # Define schemas
        schema.define_schema("Order", {"product_id": str, "quantity": int, "price": int})
        schema.define_schema("OrderSummary", {"total": int})

        # Define validation rule
        validation.define_rule(
            "positive_quantity",
            lambda e: e.data.get("quantity", 0) > 0,
        )

        # Define transform
        transform.define_transform(
            "calculate_total",
            "Order",
            "OrderSummary",
            lambda e: {"total": e.data["quantity"] * e.data["price"]},
        )

        # Create and validate order
        order = entity.create_entity(
            "Order", {"product_id": "PROD123", "quantity": 3, "price": 100}
        )

        validation_result = validation.validate(order, ["positive_quantity"])
        assert validation_result.is_valid is True

        # Transform to summary
        summary = transform.apply_transform(order, "calculate_total")
        assert summary.data["total"] == 300

    def test_process_with_validation(self):
        """Test process that includes validation steps"""
        # Define schema
        schema.define_schema("Application", {"status": str, "score": int})

        # Define validation
        validation.define_rule(
            "passing_score",
            lambda e: e.data.get("score", 0) >= 70,
        )

        # Define process steps
        def validate_step(e):
            result = validation.validate(e, ["passing_score"])
            if not result.is_valid:
                raise ValueError(f"Validation failed: {result.errors}")
            return e

        def approve_step(e):
            e.data["status"] = "approved"
            return e

        # Register and define process
        process.register_step_handler("validate_app", validate_step)
        process.register_step_handler("approve_app", approve_step)
        process.define_process("approval_process", ["validate_app", "approve_app"])

        # Test with passing application
        passing_app = entity.create_entity("Application", {"status": "pending", "score": 85})

        result = process.execute_process("approval_process", passing_app)
        assert result.data["status"] == "approved"

        # Test with failing application
        failing_app = entity.create_entity("Application", {"status": "pending", "score": 50})

        with pytest.raises(ValueError):
            process.execute_process("approval_process", failing_app)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
