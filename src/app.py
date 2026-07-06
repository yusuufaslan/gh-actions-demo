import gradio as gr


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
    import re
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
    """Generate statistics report for the given text."""
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


def clear_all():
    return "", "", ""


def create_app() -> gr.Blocks:
    """Create and return the Gradio application."""
    css = """
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        font-size: 28px;
        margin-bottom: 8px;
    }
    .main-header p {
        font-size: 14px;
        opacity: 0.9;
    }
    .stats-output {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .footer-text {
        text-align: center;
        font-size: 12px;
        color: #888;
        margin-top: 20px;
    }
    """

    with gr.Blocks(
        title="Text Tools",
        theme=gr.themes.Soft(),
        css=css,
    ) as demo:
        gr.HTML("""
        <div class="main-header">
            <h1>📝 Text Tools</h1>
            <p>Metin Analiz ve Dönüşüm Araçları — GitHub Actions ile HuggingFace Spaces'e Deploy Edildi</p>
        </div>
        """)

        text_input = gr.Textbox(
            label="Metin",
            placeholder="Analiz etmek veya dönüştürmek için metninizi buraya yazın...",
            lines=5,
            max_lines=20,
        )

        with gr.Row():
            # Left column: Statistics
            with gr.Column(scale=1):
                gr.Markdown("### 📊 İstatistikler")
                stats_btn = gr.Button("İstatistikleri Göster", variant="primary")
                stats_output = gr.Textbox(
                    label="Sonuç",
                    lines=8,
                    max_lines=10,
                    show_copy_button=True,
                )

            # Right column: Transformation
            with gr.Column(scale=1):
                gr.Markdown("### 🔤 Dönüşüm")
                case_dropdown = gr.Dropdown(
                    choices=["Büyük Harf", "Küçük Harf", "Başlık Formatı", "Ters Çevir"],
                    value="Büyük Harf",
                    label="İşlem",
                )
                transform_btn = gr.Button("Dönüştür", variant="secondary")
                transform_output = gr.Textbox(
                    label="Dönüştürülmüş Metin",
                    lines=5,
                    max_lines=20,
                    show_copy_button=True,
                )

        with gr.Row():
            clear_btn = gr.Button("🗑️ Temizle", variant="stop")

        # Event handlers
        stats_btn.click(get_stats, inputs=text_input, outputs=stats_output)
        transform_btn.click(
            transform_case, inputs=[text_input, case_dropdown], outputs=transform_output
        )
        clear_btn.click(clear_all, outputs=[text_input, stats_output, transform_output])

        gr.HTML('<div class="footer-text">Powered by Gradio & GitHub Actions</div>')

    return demo


if __name__ == "__main__":
    demo = create_app()
    demo.launch(server_name="0.0.0.0", server_port=7860)
