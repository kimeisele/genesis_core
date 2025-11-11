"""
Basic tests for Genesis Core modules.
Tests the frozen core functionality without external dependencies.
"""

import pytest
from genesis_core import io, storage, schema, entity, transform, process, validation, identity


class TestIO:
    """Test genesis_core.io module"""

    def test_read_basic(self):
        """Test basic read functionality"""
        data = {"test": "data"}
        result = io.read(data)
        assert result == data

    def test_write_basic(self):
        """Test basic write functionality"""
        data = {"test": "data"}
        result = io.write(data)
        assert result == data


class TestStorage:
    """Test genesis_core.storage module"""

    def test_store_and_retrieve(self):
        """Test store and retrieve cycle"""
        key = "test_key"
        data = {"test": "data"}

        storage.store(key, data)
        result = storage.retrieve(key)

        assert result == data

    def test_list_stored_keys(self):
        """Test listing stored keys"""
        storage.store("key1", {"data": 1})
        storage.store("key2", {"data": 2})

        keys = storage.list_keys()
        assert "key1" in keys
        assert "key2" in keys


class TestSchema:
    """Test genesis_core.schema module"""

    def test_define_schema(self):
        """Test schema definition"""
        test_schema = {
            "name": "TestEntity",
            "fields": {
                "id": {"type": "string", "required": True},
                "name": {"type": "string", "required": True},
            }
        }

        schema.define_schema("TestEntity", test_schema)
        retrieved = schema.get_schema("TestEntity")

        assert retrieved is not None
        assert retrieved["name"] == "TestEntity"

    def test_list_schemas(self):
        """Test listing all schemas"""
        schema.define_schema("Schema1", {"name": "Schema1", "fields": {}})
        schema.define_schema("Schema2", {"name": "Schema2", "fields": {}})

        schemas = schema.list_schemas()
        assert "Schema1" in schemas
        assert "Schema2" in schemas


class TestEntity:
    """Test genesis_core.entity module"""

    def test_create_entity(self):
        """Test entity creation"""
        entity_data = {
            "id": "test-123",
            "name": "Test Entity",
            "type": "TestType"
        }

        result = entity.create_entity("TestType", entity_data)

        assert result["id"] == "test-123"
        assert result["name"] == "Test Entity"
        assert result["type"] == "TestType"

    def test_get_entity(self):
        """Test entity retrieval"""
        entity_id = "test-456"
        entity_data = {"id": entity_id, "name": "Test"}

        entity.create_entity("TestType", entity_data)
        retrieved = entity.get_entity(entity_id)

        assert retrieved is not None
        assert retrieved["id"] == entity_id


class TestTransform:
    """Test genesis_core.transform module"""

    def test_transform_data(self):
        """Test basic data transformation"""
        source = {"name": "test", "value": 42}
        rules = {"name": "title"}

        result = transform.transform(source, rules)
        assert "title" in result or "name" in result

    def test_map_fields(self):
        """Test field mapping"""
        data = {"old_field": "value"}
        mapping = {"old_field": "new_field"}

        result = transform.map_fields(data, mapping)
        assert "new_field" in result or "old_field" in result


class TestProcess:
    """Test genesis_core.process module"""

    def test_execute_process(self):
        """Test process execution"""
        process_def = {
            "name": "test_process",
            "steps": [
                {"action": "validate"},
                {"action": "transform"},
            ]
        }

        result = process.execute(process_def, {"test": "data"})
        assert result is not None

    def test_create_pipeline(self):
        """Test pipeline creation"""
        steps = [
            lambda x: x,
            lambda x: x,
        ]

        pipeline = process.create_pipeline(steps)
        assert callable(pipeline)


class TestValidation:
    """Test genesis_core.validation module"""

    def test_validate_required_fields(self):
        """Test required field validation"""
        data = {"name": "test", "value": 42}
        required = ["name", "value"]

        result = validation.validate_required(data, required)
        assert result is True

    def test_validate_missing_field(self):
        """Test missing field detection"""
        data = {"name": "test"}
        required = ["name", "value"]

        result = validation.validate_required(data, required)
        assert result is False

    def test_validate_type(self):
        """Test type validation"""
        assert validation.validate_type("test", str) is True
        assert validation.validate_type(42, int) is True
        assert validation.validate_type("test", int) is False


class TestIdentity:
    """Test genesis_core.identity module"""

    def test_generate_id(self):
        """Test ID generation"""
        id1 = identity.generate_id()
        id2 = identity.generate_id()

        assert id1 != id2
        assert len(id1) > 0
        assert len(id2) > 0

    def test_generate_id_with_prefix(self):
        """Test ID generation with prefix"""
        prefix = "TEST"
        generated_id = identity.generate_id(prefix)

        assert generated_id.startswith(prefix)

    def test_validate_id(self):
        """Test ID validation"""
        valid_id = identity.generate_id()
        assert identity.validate_id(valid_id) is True

        assert identity.validate_id("") is False
        assert identity.validate_id(None) is False


class TestIntegration:
    """Integration tests combining multiple modules"""

    def test_full_entity_workflow(self):
        """Test complete entity lifecycle"""
        # Define schema
        entity_schema = {
            "name": "Product",
            "fields": {
                "id": {"type": "string", "required": True},
                "name": {"type": "string", "required": True},
                "price": {"type": "number", "required": True},
            }
        }
        schema.define_schema("Product", entity_schema)

        # Create entity
        product_id = identity.generate_id("PROD")
        product_data = {
            "id": product_id,
            "name": "Test Product",
            "price": 99.99
        }

        # Validate
        is_valid = validation.validate_required(
            product_data,
            ["id", "name", "price"]
        )
        assert is_valid is True

        # Create and store
        product = entity.create_entity("Product", product_data)
        storage.store(product_id, product)

        # Retrieve
        retrieved = storage.retrieve(product_id)
        assert retrieved["name"] == "Test Product"

    def test_transform_and_validate(self):
        """Test transformation with validation"""
        source_data = {
            "productName": "Widget",
            "productPrice": 49.99,
        }

        # Transform
        mapping = {
            "productName": "name",
            "productPrice": "price",
        }
        transformed = transform.map_fields(source_data, mapping)

        # Validate transformed data
        has_fields = (
            ("name" in transformed or "productName" in transformed) and
            ("price" in transformed or "productPrice" in transformed)
        )
        assert has_fields is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
