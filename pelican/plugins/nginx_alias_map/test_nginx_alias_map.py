import locale
import os
from tempfile import mkdtemp
import unittest

from pelican import Pelican
from pelican.settings import read_settings

from . import nginx_alias_map

CUR_DIR = os.path.dirname(__file__)


class TestNginxAliasMap(unittest.TestCase):
    """Test mapping Aliases for Nginx"""

    def setUp(self, override=None):
        self.temp_path = mkdtemp(prefix="pelicantests.")
        settings = {
            "PATH": os.path.join(CUR_DIR, "test_data"),
            "OUTPUT_PATH": self.temp_path,
            "PLUGINS": [nginx_alias_map],
            "LOCALE": locale.normalize("en_US"),
            "TIMEZONE": "UTC",
            "SITEURL": "https://mysite.dev",
        }
        if override:
            settings.update(override)

        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)

        pelican.run()

    def test_create_alias(self):
        self.assertTrue(os.path.exists(os.path.join(self.temp_path, "alias_map.txt")))
        expected = open(os.path.join(CUR_DIR, "test_data", "alias_map.expected")).read()
        actual = open(os.path.join(self.temp_path, "alias_map.txt")).read()
        self.assertEqual(expected, actual)
