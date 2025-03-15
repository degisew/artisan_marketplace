import pytest
from django.db.utils import IntegrityError


pytestmark = pytest.mark.django_db


class TestDataLookupModel:
    def test_unique_value_constraint(self, data_lookup_factory):
        data_lookup_factory(value="unique-value")
        with pytest.raises(IntegrityError):
            data_lookup_factory(value="unique-value")

    def test_unique_is_default_per_type(self, data_lookup_factory):
        data_lookup_factory(type="attribute_field_type", is_default=True)
        with pytest.raises(IntegrityError):
            data_lookup_factory(type="attribute_field_type", is_default=True)

    def test_unique_index_per_type(self, data_lookup_factory):
        data_lookup_factory(type="attribute_field_type", index=1)
        with pytest.raises(IntegrityError):
            data_lookup_factory(type="attribute_field_type", index=1)


class TestSystemSettingModel:
    def test_unique_key_constraint(self, system_setting_factory):
        system_setting_factory(key="unique-key")
        with pytest.raises(IntegrityError):
            system_setting_factory(key="unique-key")

    def test_system_setting_with_data_type(self, system_setting_factory, data_lookup_factory):
        data_type = data_lookup_factory(type="data_type")
        system_setting = system_setting_factory(data_type=data_type)
        assert system_setting.data_type == data_type
