import re


def count_words(text: str) -> int:
    if not text or not text.strip():
        return 0
    return len(text.strip().split())


def count_characters(text: str) -> int:
    return len(text)


def count_characters_no_spaces(text: str) -> int:
    return len(text.replace(" ", ""))


def count_sentences(text: str) -> int:
    if not text or not text.strip():
        return 0
    sentences = re.split(r"[.!?]+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def count_paragraphs(text: str) -> int:
    if not text or not text.strip():
        return 0
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return len(paragraphs)


def to_upper(text: str) -> str:
    return text.upper()


def to_lower(text: str) -> str:
    return text.lower()


def to_title(text: str) -> str:
    return text.title()


def to_reverse(text: str) -> str:
    return text[::-1]


def transform_case(text: str, operation: str) -> str:
    operations = {
        "Büyük Harf": to_upper,
        "Küçük Harf": to_lower,
        "Başlık Formatı": to_title,
        "Ters Çevir": to_reverse,
    }
    fn = operations.get(operation, to_upper)
    return fn(text)


def get_stats(text: str) -> str:
    if not text or not text.strip():
        return "Lütfen analiz edilecek bir metin girin."

    stats = {
        "Karakter (toplam)": count_characters(text),
        "Karakter (boşluksuz)": count_characters_no_spaces(text),
        "Kelime": count_words(text),
        "Cümle": count_sentences(text),
        "Paragraf": count_paragraphs(text),
    }

    lines = ["📊 Metin İstatistikleri", "=" * 40]
    for label, value in stats.items():
        lines.append(f"  {label}: {value}")

    return "\n".join(lines)
