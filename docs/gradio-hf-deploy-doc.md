# Gradio Uygulaması ve HuggingFace Spaces Deploy Dokümanı

**Oluşturulma Tarihi:** 6 Temmuz 2026
**Son Güncelleme:** 6 Temmuz 2026
**Yazar:** Mühendislilik Ekibi

---

## 1. Proje Tanıtımı

Bu proje, **GitHub Actions kullanarak bir Gradio uygulamasını otomatik olarak HuggingFace Spaces'e deploy eden** bir referans projedir.

---

## 2. HuggingFace Spaces Nedir?

Gradio veya Streamlit tabanlı uygulamalarınızı host edebilirsiniz.

| Tier | Fiyat |
|------|-------|
| CPU Basic | Bedava |
| T4 GPU | Orta |
| A100 GPU | Yüksek |

---

## 3. Gradio Nedir?

ML modelleri için hızlı web arayüzü oluşturmayı sağlayan bir Python kütüpanesidir.

```python
import gradio as gr

def selamla(isim):
    return f"Merhaba {isim}!"

demo = gr.Interface(fn=selamla, inputs="textbox", outputs="textbox")
demo.launch()
```

---

## 4. Teknik Mimari

```
deploy-to-hf.yml                  deploy-hf-space.yml
(Tetikleyici)                    (Asıl deploy mantığı)
        ↓                                    ↑
        ──────────────── uses: ./deploy-hf-space.yml ───────────────────────────────────────────────────↑
```

---

## 5. Proje Dosya Yapısı

```
gh-actions-demo/
├── .github/
│   └── workflows/
│       ├── deploy-to-hf.yml        # Ana workflow (tetikleyici)
│       └── deploy-hf-space.yml     # Reusable workflow (deploy mantığı)
├── src/
│   └── app.py
├── requirements.txt
├── Dockerfile
└── docs/
    ├── github-actions-guide.md
    └── gradio-hf-deploy-doc.md
```

---

## 6. Lokal Çalıştırma

```bash
pip install -r requirements.txt
python src/app.py
```

Tarayıcı: `http://127.0.0.1:7860`

---

## 7. HuggingFace Spaces'e Manuel Deploy

```bash
pip install huggingface_hub[hf_hub]

huggingface-cli create-repo text-tools --type space --space-sdk gradio
huggingface-cli upload yusuf-aslan/text-tools src/app.py ./app.py
```

---

## 8. GitHub Actions ile Otomatik Deploy

### 8.1 HF Token Oluşturma
1. https://huggingface.co/settings/tokens → New token → **Write** role

### 8.2 GitHub Secret Ekleme
1. Repo → Settings → Secrets → Actions → New repository secret
2. Name: `HF_TOKEN`, Value: (token değeri)

### 8.3 Workflow Çalışır
- `deploy-to-hf.yml` ana workflow'dur (ne zaman çalışır)
- `deploy-hf-space.yml` asıl deploy mantığını içerir

---

## 9. Workflow Açıklaması

### deploy-to-hf.yml
```yaml
on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "requirements.txt"
  workflow_dispatch:

jobs:
  deploy:
    uses: ./.github/workflows/deploy-hf-space.yml
    with:
      space-id: "yusuf-aslan/text-tools"
    secrets:
      HF_TOKEN: ${{ secrets.HF_TOKEN }}
```

### deploy-hf-space.yml
```yaml
on:
  workflow_call:
    inputs:
      space-id:
        required: true
        type: string
    secrets:
      HF_TOKEN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install huggingface-hub
      # Space oluştur, dosyaları yükle, doğrula
```

---

## 10. Sorun Giderme

| Sorun | Çözüm |
|-------|--------|
| Workflow çalışmıyor | `.github/workflows/` yolunu kontrol edin |
| 403 Forbidden | HF Token'ının Write yetkisi olduğundan emin olun |
| Space başlamıyor | Factory Reboot yapın |
| Build Error | Dockerfile + Gradio SDK çakışması olabilir |

---

## Ek Kaynaklar

| Kaynak | Link |
|--------|------|
| Gradio Docs | https://www.gradio.app/docs |
| HF Spaces Docs | https://huggingface.co/docs/hub/spaces-overview |
| GitHub Actions Docs | https://docs.github.com/en/actions |

---

**Son Düzenleme:** 6 Temmuz 2026
