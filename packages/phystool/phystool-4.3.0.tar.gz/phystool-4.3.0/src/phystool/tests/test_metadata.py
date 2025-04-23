from unittest import TestCase

from phystool.tags import Tags
from phystool.metadata import Metadata
from phystool.pdbfile import VALID_TYPES


class TestMetadata(TestCase):
    @classmethod
    def setUp(cls):
        cls._metadata = Metadata()

    def test_filter(self):
        selected_tags = Tags.validate("A1,B1")
        excluded_tags = Tags.validate("C2")

        filtered = self._metadata.filter(
            query="",
            uuid_bit="",
            file_types=VALID_TYPES,
            selected_tags=selected_tags,
            excluded_tags=excluded_tags,
        )
        self.assertEqual(len(filtered), 2)
        for pdb_file in filtered:
            self.assertTrue(pdb_file.tags.without_overlap(Tags({})))
            self.assertTrue(pdb_file.tags.without_overlap(excluded_tags))
            self.assertTrue(pdb_file.tags.with_overlap(selected_tags))
            self.assertTrue(pdb_file.tags.with_overlap(Tags({})))
