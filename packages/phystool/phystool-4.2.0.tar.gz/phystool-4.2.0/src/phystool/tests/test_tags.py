from unittest import TestCase

from phystool.tags import Tags


_tags_A = {
    'Cat1': ['A1', 'B1'],
    'Cat2': ['A2'],
}
_tags_B = {
    'Cat1': ['B1', 'C1'],
    'Cat2': ['B2'],
}
_tags_C = {
    'Cat1': ['B1'],
    'Cat2': ['C2'],
}
_tags_D: dict[str, list[str]] = {}


def mock_filter(selected: Tags, excluded: Tags, among: list[Tags]) -> list[int]:
    return [
        idx
        for idx, tags in enumerate(among)
        if (tags.with_overlap(selected) and tags.without_overlap(excluded))
    ]


class TestTags(TestCase):
    @classmethod
    def setUp(cls):
        # Tags.TAGS needs to contain all the tags used in this file.
        Tags.TAGS = Tags(
            {
                "Cat1": ["A1", "B1", "C1", "D1"],
                "Cat2": ["A2", "B2", "C2", "D2"],
            }
        )
        cls.tags_A = Tags(_tags_A)
        cls.tags_B = Tags(_tags_B)
        cls.tags_C = Tags(_tags_C)
        cls.tags_D = Tags(_tags_D)

    def test_valid_tags(self):
        for test_tags in [_tags_A, _tags_B, _tags_C]:
            for category, tags in test_tags.items():
                for tag in tags:
                    self.assertTrue(Tags.TAGS.with_overlap(Tags({category: [tag]})))

    def test_default_constructor(self):
        self.assertEqual(Tags({}).data, {})

    def test_validate(self):
        self.assertEqual(
            Tags.validate("A1,A2,B1,A1").data,
            {'Cat1': ['A1', 'B1'], 'Cat2': ['A2']}
        )
        self.assertEqual(
            Tags.validate("A1,foo,B2").data,
            {'Cat1': ['A1'], 'Cat2': ['B2']}
        )
        self.assertEqual(
            Tags.validate("").data,
            {}
        )

    def test_bool(self):
        self.assertFalse(Tags({}))
        self.assertTrue(Tags({'foo': "bar"}))

    def test_with_overlap(self):
        t = Tags({})
        self.assertTrue(self.tags_A.with_overlap(t))
        self.assertTrue(self.tags_B.with_overlap(t))
        self.assertTrue(self.tags_C.with_overlap(t))
        self.assertTrue(self.tags_D.with_overlap(t))

        t = Tags.validate("A1")
        self.assertTrue(self.tags_A.with_overlap(t))
        self.assertFalse(self.tags_B.with_overlap(t))
        self.assertFalse(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

        t = Tags.validate("A1,A2")
        self.assertTrue(self.tags_A.with_overlap(t))
        self.assertFalse(self.tags_B.with_overlap(t))
        self.assertFalse(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

        t = Tags.validate("A1,C1")
        self.assertTrue(self.tags_A.with_overlap(t))
        self.assertTrue(self.tags_B.with_overlap(t))
        self.assertFalse(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

        t = Tags.validate("A1,C2")
        self.assertFalse(self.tags_A.with_overlap(t))
        self.assertFalse(self.tags_B.with_overlap(t))
        self.assertFalse(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

        t = Tags.validate("B1,C2")
        self.assertFalse(self.tags_A.with_overlap(t))
        self.assertFalse(self.tags_B.with_overlap(t))
        self.assertTrue(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

        t = Tags.validate("D1,D2")
        self.assertFalse(self.tags_A.with_overlap(t))
        self.assertFalse(self.tags_B.with_overlap(t))
        self.assertFalse(self.tags_C.with_overlap(t))
        self.assertFalse(self.tags_D.with_overlap(t))

    def test_without_overlap(self):
        t = Tags({})
        self.assertTrue(self.tags_A.without_overlap(t))
        self.assertTrue(self.tags_B.without_overlap(t))
        self.assertTrue(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("A1")
        self.assertFalse(self.tags_A.without_overlap(t))
        self.assertTrue(self.tags_B.without_overlap(t))
        self.assertTrue(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("A1,A2")
        self.assertFalse(self.tags_A.without_overlap(t))
        self.assertTrue(self.tags_B.without_overlap(t))
        self.assertTrue(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("A1,C1")
        self.assertFalse(self.tags_A.without_overlap(t))
        self.assertFalse(self.tags_B.without_overlap(t))
        self.assertTrue(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("A1,C2")
        self.assertFalse(self.tags_A.without_overlap(t))
        self.assertTrue(self.tags_B.without_overlap(t))
        self.assertFalse(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("B1,C2")
        self.assertFalse(self.tags_A.without_overlap(t))
        self.assertFalse(self.tags_B.without_overlap(t))
        self.assertFalse(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

        t = Tags.validate("D1,D2")
        self.assertTrue(self.tags_A.without_overlap(t))
        self.assertTrue(self.tags_B.without_overlap(t))
        self.assertTrue(self.tags_C.without_overlap(t))
        self.assertTrue(self.tags_D.without_overlap(t))

    def test_add(self):
        t1 = self.tags_A + self.tags_B
        t2 = Tags(_tags_A)
        t2 += self.tags_B
        # check that the addition left the original tags untouched
        self.assertEqual(self.tags_A.data, _tags_A)
        self.assertEqual(self.tags_B.data, _tags_B)

        t = Tags.validate("A1,B1,C1,A2,B2")
        self.assertEqual(t.data, t1.data)
        self.assertEqual(t.data, t2.data)

    def test_sub(self):
        t1 = self.tags_A - self.tags_B
        t2 = Tags(_tags_A)
        t2 -= self.tags_B
        # check that the substraction left the original tags untouched
        self.assertEqual(self.tags_A.data, _tags_A)
        self.assertEqual(self.tags_B.data, _tags_B)

        t = Tags.validate("A1,A2")
        self.assertEqual(t1.data, t.data)
        self.assertEqual(t2.data, t.data)

        t1 -= t
        t2 -= t
        self.assertEqual(t1.data, {})
        self.assertEqual(t2.data, {})

    def test_filter(self):
        available = [
            self.tags_A,
            self.tags_B,
            self.tags_C,
            self.tags_D,
        ]
        # PDB: tag[cat1] = [A1,B1]
        # filter: include A1 & exclude B1 -> not select
        self.assertEqual(
            mock_filter(
                Tags.validate("A1"),
                Tags.validate("B1"),
                available + [Tags.validate("A1,C2")]
            ),
            [4]
        )
        # PDB: tag[cat1] = [B1]
        #      tag[cat2] = [B2]
        # filter: include B1 & exclude B2 -> not select
        self.assertEqual(
            mock_filter(
                Tags.validate("B1"),
                Tags.validate("B2"),
                available + [Tags.validate("B1")]
            ),
            [0, 2, 4]
        )
        # PDB: tag[cat1] = [A1,B1]
        #      tag[cat2] = [A2]
        # filter: include A1 & exclude B1 & include A2 -> not select
        self.assertEqual(
            mock_filter(
                Tags.validate("A1, A2"),
                Tags.validate("B1"),
                available + [Tags.validate("A1,A2,C2")]
            ),
            [4]
        )
        # PDB: tag[cat1] = [A1,B1]
        #      tag[cat2] = [B2]
        # filter: include A1 & exclude B1 & without_overlap B2 -> not select
        self.assertEqual(
            mock_filter(
                Tags.validate("A1"),
                Tags.validate("B1, B2"),
                available + [Tags.validate("A1,B2")]
            ),
            []
        )
