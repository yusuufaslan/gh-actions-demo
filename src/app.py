import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gradio as gr

from text_utils import (
    get_stats,
    transform_case,
)

CSS = """
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


def clear_all():
    return "", "", ""


def create_app() -> gr.Blocks:
    with gr.Blocks(title="Text Tools") as demo:
        gr.HTML("""
        <div class="main-header">
            <h1>📝 Text Tools</h1>
            <p>Metin Analiz ve Dönüşüm Aracı Demo</p>
        </div>
        """)

        text_input = gr.Textbox(
            label="Metin",
            placeholder="Analiz etmek veya dönüştürmek için metninizi buraya yazın...",
            lines=5,
            max_lines=20,
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📊 İstatistikler")
                stats_btn = gr.Button("İstatistikleri Göster", variant="primary")
                stats_output = gr.Textbox(
                    label="Sonuç",
                    lines=8,
                    max_lines=10,
                )

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
                )

        with gr.Row():
            clear_btn = gr.Button("🗑️ Temizle", variant="stop")

        stats_btn.click(get_stats, inputs=text_input, outputs=stats_output)
        transform_btn.click(
            transform_case, inputs=[text_input, case_dropdown], outputs=transform_output
        )
        clear_btn.click(clear_all, outputs=[text_input, stats_output, transform_output])

        gr.HTML('<div class="footer-text">Powered by Gradio & GitHub Actions</div>')

    return demo


if __name__ == "__main__":
    demo = create_app()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Soft(),
        css=CSS,
    )
