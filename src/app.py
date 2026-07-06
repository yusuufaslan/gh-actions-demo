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
        "Bu\u00fcy\u00fck Harf": to_upper,
        "K\u00fc\u00e7\u00fck Harf": to_lower,
        "Ba\u015fl\u0131k Format\u0131": to_title,
        "Ters \u00c7evir": to_reverse,
    }
    fn = operations.get(operation, to_upper)
    return fn(text)


def get_stats(text: str) -> str:
    """Generate statistics report for the given text."""
    if not text or not text.strip():
        return "Lutfen analiz edilecek bir metin girin."

    stats = {
        "Karakter (toplam)": count_characters(text),
        "Karakter (bo\u015fluksuz)": count_characters_no_spaces(text),
        "Kelime": count_words(text),
        "Cumle": count_sentences(text),
        "Paragraf": count_paragraphs(text),
    }

    lines = ["Metin Istatistikleri", "=" * 40]
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
            <h1>Text Tools</h1>
            <p>Metin Analiz ve D\u00f6n\u00fc\u015f\u00fcm Ara\u00e7lar\u0131</p>
        </div>
        """)

        text_input = gr.Textbox(
            label="Metin",
            placeholder="Analiz etmek veya d\u00f6n\u00fc\u015ft\u00fcrmek i\u00e7in metninizi buraya yaz\u0131n...",
            lines=5,
            max_lines=20,
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Istatistikler")
                stats_btn = gr.Button("Istatistikleri G\u00f6ster", variant="primary")
                stats_output = gr.Textbox(
                    label="Sonu\u00e7",
                    lines=8,
                    max_lines=10,
                    show_copy_button=True,
                )

            with gr.Column(scale=1):
                gr.Markdown("### D\u00f6n\u00fc\u015f\u00fcm")
                case_dropdown = gr.Dropdown(
                    choices=[
                        "Bu\u00fcy\u00fck Harf",
                        "K\u00fc\u00e7\u00fck Harf",
                        "Ba\u015fl\u0131k Format\u0131",
                        "Ters \u00c7evir",
                    ],
                    value="Bu\u00fcy\u00fck Harf",
                    label="I\u015flem",
                )
                transform_btn = gr.Button("D\u00f6n\u00fc\u015ft\u00fcr", variant="secondary")
                transform_output = gr.Textbox(
                    label="D\u00f6n\u00fc\u015ft\u00fcr\u00fclm\u00fcs Metin",
                    lines=5,
                    max_lines=20,
                    show_copy_button=True,
                )

        with gr.Row():
            clear_btn = gr.Button("Temizle", variant="stop")

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
