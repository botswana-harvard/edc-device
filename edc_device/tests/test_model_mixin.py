from django.apps import apps as django_apps
from django.test import TestCase
from django.test.utils import override_settings

from ..constants import CLIENT
from .models import TestModel


class TestModelMixin(TestCase):

    def test_model(self):
        obj = TestModel()
        self.assertFalse(obj.device_created)
        self.assertFalse(obj.device_modified)

    def test_model_on_create(self):
        app_config = django_apps.get_app_config('edc_device')
        with override_settings(DEVICE_ID='10', DEVICE_ROLE=CLIENT):
            app_config.device_id = None
            app_config.ready()
            obj = TestModel.objects.create()
            self.assertEqual(obj.device_created, '10')
            self.assertEqual(obj.device_modified, '10')

    def test_model_on_modified(self):
        app_config = django_apps.get_app_config('edc_device')
        with override_settings(DEVICE_ID='10', DEVICE_ROLE=CLIENT):
            app_config.device_id = None
            app_config.ready()
            obj = TestModel.objects.create()
            self.assertEqual(obj.device_created, '10')
            self.assertEqual(obj.device_modified, '10')
        with override_settings(DEVICE_ID='20', DEVICE_ROLE=CLIENT):
            app_config.device_id = None
            app_config.ready()
            obj.save()
            self.assertEqual(obj.device_created, '10')
            self.assertEqual(obj.device_modified, '20')
