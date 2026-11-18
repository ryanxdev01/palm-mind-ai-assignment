
import unittest

from app.services.chunking_service import (
    fixed_size_chunking,
    recursive_character_chunking,
)


class TestChunking(unittest.TestCase):

    def test_fixed_size_chunking(self):
        text = "A" * 250

        chunks = fixed_size_chunking(
            text,
            chunk_size=100,
            overlap=20
        )

        self.assertGreater(len(chunks), 1)
        self.assertEqual(len(chunks[0]), 100)
        self.assertEqual(chunks[0][-20:], chunks[1][:20])

    def test_recursive_chunking(self):
        text = "This is a sample sentence. " * 20

        chunks = recursive_character_chunking(
            text,
            chunk_size=100,
            overlap=20
        )

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 100 for chunk in chunks))

    def test_empty_text(self):
        self.assertEqual(fixed_size_chunking(""), [])
        self.assertEqual(recursive_character_chunking(""), [])


if __name__ == "__main__":
    unittest.main()
