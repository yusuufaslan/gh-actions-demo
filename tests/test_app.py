import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from text_utils import (
    count_characters,
    count_characters_no_spaces,
    count_paragraphs,
    count_sentences,
    count_words,
    get_stats,
    to_lower,
    to_reverse,
    to_title,
    to_upper,
    transform_case,
)


class TestCounting:
    def test_count_words_basic(self):
        assert count_words("hello world") == 2

    def test_count_words_multiple_spaces(self):
        assert count_words("hello   world   foo") == 3

    def test_count_words_empty(self):
        assert count_words("") == 0

    def test_count_words_whitespace_only(self):
        assert count_words("   \t\n  ") == 0

    def test_count_characters(self):
        assert count_characters("hello") == 5
        assert count_characters("") == 0

    def test_count_characters_no_spaces(self):
        assert count_characters_no_spaces("hello world") == 10
        assert count_characters_no_spaces("a b c") == 3
        assert count_characters_no_spaces("nospace") == 7

    def test_count_sentences_basic(self):
        assert count_sentences("Hello. World!") == 2

    def test_count_sentences_single(self):
        assert count_sentences("One sentence.") == 1

    def test_count_sentences_no_punctuation(self):
        assert count_sentences("No punctuation here") == 1

    def test_count_sentences_empty(self):
        assert count_sentences("") == 0

    def test_count_paragraphs_basic(self):
        assert count_paragraphs("Para1\n\nPara2\n\nPara3") == 3

    def test_count_paragraphs_single(self):
        assert count_paragraphs("Just one paragraph.") == 1

    def test_count_paragraphs_empty(self):
        assert count_paragraphs("") == 0


class TestTransforms:
    def test_to_upper(self):
        assert to_upper("hello world") == "HELLO WORLD"

    def test_to_lower(self):
        assert to_lower("HELLO WORLD") == "hello world"

    def test_to_title(self):
        assert to_title("hello world") == "Hello World"

    def test_to_reverse(self):
        assert to_reverse("abc") == "cba"
        assert to_reverse("") == ""

    def test_transform_case_valid_operations(self):
        assert transform_case("hello", "Büyük Harf") == "HELLO"
        assert transform_case("HELLO", "Küçük Harf") == "hello"
        assert transform_case("hello world", "Başlık Formatı") == "Hello World"
        assert transform_case("abc", "Ters Çevir") == "cba"

    def test_transform_case_unknown_defaults_to_upper(self):
        assert transform_case("hello", "Bilinmeyen Islem") == "HELLO"


class TestGetStats:
    def test_get_stats_output_contains_labels(self):
        result = get_stats("Hello world. This is a test.")
        assert "Kelime" in result
        assert "Karakter" in result
        assert "Cümle" in result

    def test_get_stats_empty_input(self):
        result = get_stats("")
        assert result == "Lütfen analiz edilecek bir metin girin."

    def test_get_stats_word_count(self):
        result = get_stats("one two three")
        assert "Kelime: 3" in result
