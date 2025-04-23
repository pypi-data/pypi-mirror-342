from unittest import TestCase

from phystool.helper import ContextIterator, greptex
from phystool.config import config


class TestContextIterator(TestCase):
    def test_A(self):
        my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        wrapper = ContextIterator(my_list, before=1, after=3)
        for entry in wrapper:
            if entry == 3:
                self.assertEqual(
                    wrapper.get(),
                    [2, 3, 4, 5, 6]
                )
            elif entry == 7:
                self.assertEqual(
                    wrapper.get(),
                    [6, 7, 8, 9]
                )

    def test_B(self):
        my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        wrapper = ContextIterator(my_list, before=0, after=2)
        for entry in wrapper:
            if entry == 3:
                self.assertEqual(
                    wrapper.get(),
                    [3, 4, 5]
                )
            elif entry == 9:
                self.assertEqual(
                    wrapper.get(),
                    [9]
                )


class TestTextGrepTex(TestCase):
    def test_backslash(self):
        self.assertEqual(
            {'b23d2f32-da63-46fd-86a2-ceaec3b87168'},
            greptex(r"très utile afin de tester \emph{ripgrep}.", config.DB_DIR, True)
        )
        self.assertEqual(
            {'050f9e5c-0acd-400a-a775-9886d6675a6b'},
            greptex("tres utile afin de tester emph{ripgrep}.", config.DB_DIR, True)
        )

    def test_dollar(self):
        self.assertEqual(
            {'b23d2f32-da63-46fd-86a2-ceaec3b87168'},
            greptex("les $dollars$ ainsi que les accents", config.DB_DIR, True)
        )
        self.assertEqual(
            {'050f9e5c-0acd-400a-a775-9886d6675a6b'},
            greptex("les dollars ainsi que les accents", config.DB_DIR, True)
        )

    def test_e_grave(self):
        self.assertEqual(
            {'b23d2f32-da63-46fd-86a2-ceaec3b87168'},
            greptex("les accents sont bien trouvés.", config.DB_DIR, True)
        )
        self.assertEqual(
            {'050f9e5c-0acd-400a-a775-9886d6675a6b'},
            greptex("les accents sont bien trouves.", config.DB_DIR, True)
        )

    def test_e_aigue(self):
        self.assertEqual(
            {'b23d2f32-da63-46fd-86a2-ceaec3b87168'},
            greptex("très utile", config.DB_DIR, True)
        )
        self.assertEqual(
            {'050f9e5c-0acd-400a-a775-9886d6675a6b'},
            greptex("tres utile", config.DB_DIR, True)
        )

    def test_smart_calse(self):
        self.assertEqual(
            {'b23d2f32-da63-46fd-86a2-ceaec3b87168'},
            greptex("INTELLigement.", config.DB_DIR, True)
        )
        self.assertEqual(
            {
                'b23d2f32-da63-46fd-86a2-ceaec3b87168',
                '050f9e5c-0acd-400a-a775-9886d6675a6b'
            },
            greptex("intelligement.", config.DB_DIR, True)
        )
