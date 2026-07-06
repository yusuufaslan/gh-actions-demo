# Gradio Uygulaması ve HuggingFace Spaces Deploy Dokümanı

**Oluşturulma Tarihi:** 6 Temmuz 2026
**Son Güncelleme:** 6 Temmuz 2026
**Yazar:** Mühendislilik Ekibi

---

## 1. Proje Tanıtımı

Bu proje, **GitHub Actions kullanarak bir Gradio uygulamasını otomatik olarak HuggingFace Spaces'e deploy eden** bir referans projedir. Uygulama "Text Tools" adında bir metin analiz ve dönüşüm aracıdır.

---

## 2. HuggingFace Spaces Nedir?

HuggingFace Spaces, Gradio veya Streamlit tabanlı uygulamalarınızı ücretsiz host edebileceğiniz bir platformdur.

| Tier | Fiyat |
|------|-------|
| CPU Basic | Bedava |
| T4 GPU | Orta |
| A100 GPU | Yüksek |

Gradio SDK ile oluşturulan uygulamalar, Space oluşturulduktan sonra otomatik olarak CPU Basic tier'da çalışmaya başlar.

---

## 3. Gradio Nedir?

ML modelleri için hızlı web arayüzü oluşturmayı sağlayan bir Python kütüphanesidir.

```python
import gradio as gr

def selamla(isim):
    return f"Merhaba {isim}!"

demo = gr.Interface(fn=selamla, inputs="textbox", outputs="textbox")
demo.launch()
```

Bu projede `gr.Blocks` API kullanılarak daha gelişmiş bir arayüz oluşturulmuştur.

---

## 4. Teknik Mimari

```
deploy-to-hf.yml                  deploy-hf-space.yml
(Tetikleyici)                    (Asıl deploy mantığı)
        ↓                                    ↑
        ──────────────── uses: ./deploy-hf-space.yml ───────────────────────────────────────────────────↑
```

**deploy-to-hf.yml** — Ne zaman çalışacağını belirler (trigger):
- `src/app.py` veya `requirements.txt` değiştiğinde
- `.github/workflows/**` yolundaki bir dosya değiştiğinde
- Manuel olarak `workflow_dispatch` ile

**deploy-hf-space.yml** — Deploy işlemini gerçekleştirir (reusable workflow):
- Space yoksa oluşturur
- Dosyaları yükler
- Deploy durumunu kontrol eder

---

## 5. Proje Dosya Yapısı

```
gh-actions-demo/
├── .github/
│   └── workflows/
│       ├── deploy-to-hf.yml          # Ana workflow (tetikleyici)
│       ├── deploy-hf-space.yml       # Reusable workflow (deploy mantığı)
│       └── scripts/
│           ├── create_space.py       # Space oluşturma script'i
│           └── upload_file.py        # Dosya yükleme script'i
├── src/
│   └── app.py                        # Gradio uygulaması
├── requirements.txt                  # Python bağımlılıkları
├── documentations/
│   ├── github-actions-guide.md       # GitHub Actions kapsamlı dokümanı
│   └── gradio-hf-deploy-doc.md       # Bu doküman
└── README.md
```

---

## 6. Lokal Çalıştırma

```bash
pip install -r requirements.txt
python src/app.py
```

Tarayıcı: `http://127.0.0.1:7860`

### Uygulama Özellikleri

- **📊 Metin İstatistikleri**: Karakter, kelime, cümle, paragraf sayma
- **🔤 Metin Dönüşüm**: Büyük/Harf, Küçük Harf, Başlık Formatı, Ters Çevir
- **Temizle** butonu ile tüm alanları sıfırlama

---

## 7. HuggingFace Spaces'e Manuel Deploy

```bash
pip install "huggingface_hub[hf_hub]"

# Space oluştur
huggingface-cli create-repo yusuf-aslan/text-tools --type space --space-sdk gradio

# Dosyaları yükle
huggingface-cli upload yusuf-aslan/text-tools src/app.py --repo-type space --filename app.py
huggingface-cli upload yusuf-aslan/text-tools requirements.txt --repo-type space
```

---

## 8. GitHub Actions ile Otomatik Deploy

### 8.1 HF Token Oluşturma

1. https://huggingface.co/settings/tokens → **New token** → **Write** role seçin
2. Token'ı güvenli bir yerde saklayın (tek kez gösterilir)

### 8.2 GitHub Secret Ekleme

1. Repo → Settings → Secrets and variables → Actions
2. **New repository secret** → Name: `HF_TOKEN`, Value: (token değeri)

### 8.3 Workflow Nasıl Çalışır

**deploy-to-hf.yml** (Ana workflow - tetikleyici):

```yaml
name: Deploy to HuggingFace Spaces

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "requirements.txt"
      - ".github/workflows/**"
  workflow_dispatch:

jobs:
  deploy:
    uses: ./.github/workflows/deploy-hf-space.yml
    with:
      space-id: "yusuf-aslan/text-tools"
    secrets:
      HF_TOKEN: ${{ secrets.HF_TOKEN }}
```

**deploy-hf-space.yml** (Reusable workflow - deploy mantığı):

```yaml
name: HuggingFace Spaces Deploy (Reusable)

on:
  workflow_call:
    inputs:
      space-id:
        description: "HuggingFace Space ID (owner/name)"
        required: true
        type: string
    secrets:
      HF_TOKEN:
        required: true

env:
  HF_TOKEN: ${{ secrets.HF_TOKEN }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install huggingface-hub

      - name: Create Space if Not Exists
        env:
          SPACE_ID: ${{ inputs.space-id }}
        run: |
          python .github/workflows/scripts/create_space.py

      - name: Upload Files to Space
        env:
          SPACE_ID: ${{ inputs.space-id }}
        run: |
          FILE_LIST=(
            "src/app.py:app.py"
            "requirements.txt:requirements.txt"
          )
          for entry in "${FILE_LIST[@]}"; do
              IFS=':' read -r local remote <<< "$entry"
              if [[ -f "$local" ]]; then
                  echo "Yukleniyor: $local -> $remote"
                  LOCAL_PATH="$local" REMOTE_PATH="$remote" python .github/workflows/scripts/upload_file.py
              else
                  echo "UYARI: $local bulunamadi, atlan."
              fi
          done
          echo "Dosyalar Space yuklendi."

      - name: Verify Deployment
        run: |
          echo "Deploy tamamlandi!"
          echo "Space adresi: https://huggingface.co/spaces/${{ inputs.space-id }}"
```

### 8.4 Yardımcı Script'ler

**`create_space.py`** — Space yoksa oluşturur:

```python
#!/usr/bin/env python3
import os
from huggingface_hub import HfApi

space_id = os.environ.get("SPACE_ID", "")
api = HfApi()

api.create_repo(
    repo_id=space_id,
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)
print("Space mevcut veya olusturuldu.")
```

**`upload_file.py`** — Belirli bir dosyayı Space'e yükler:

```python
#!/usr/bin/env python3
import os
from huggingface_hub import HfApi

space_id = os.environ.get("SPACE_ID", "")
local_path = os.environ.get("LOCAL_PATH", "")
remote_path = os.environ.get("REMOTE_PATH", "")

api = HfApi()
api.upload_file(
    path_or_fileobj=local_path,
    path_in_repo=remote_path,
    repo_id=space_id,
    repo_type="space",
)
print(f"Yuklendi: {local_path} -> {remote_path}")
```

---

## 9. Workflow Akış Şeması

```
[Push to main / Workflow Dispatch]
        │
        ▼
  [deploy-to-hf.yml tetiklenir]
        │
        ▼
  [deploy-hf-space.yml çağrılır]
        │
        ├──► 1. Checkout
        ├──► 2. Python 3.11 Kural
        ├──► 3. Install huggingface-hub
        ├──► 4. Space oluştur (yoksa)
        ├──► 5. Dosyaları yükle
        │       ├── src/app.py → app.py
        │       └── requirements.txt → requirements.txt
        └──► 6. Deploy doğrulama
                 │
                 ▼
           [Space canlı: https://huggingface.co/spaces/yusuf-aslan/text-tools]
```

---

## 10. Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| Workflow çalışmıyor | `.github/workflows/` yolunu kontrol edin |
| 403 Forbidden | HF Token'ının Write yetkisi olduğundan emin olun |
| Space başlamıyor | Space sayfasında "Factory Reboot" yapın |
| "Space bulunamadi" hatası | Space adını ve HF Token'ı kontrol edin |
| Dosya güncelleme yansımadı | Space sayfalarından "Factory Reboot" yapın (bazen cache nedeniyle gecikmeli olabilir) |

---

## 11. Yeni Dosya Ekleme

Space'e yeni bir dosya eklemek istediğinizde, `deploy-hf-space.yml` workflow içindeki `FILE_LIST` dizisine ekleyin:

```yaml
FILE_LIST=(
  "src/app.py:app.py"
  "requirements.txt:requirements.txt"
  "src/static/style.css:static/style.css"  # Yeni dosya
)
```

---

## Ek Kaynaklar

| Kaynak | Link |
|--------|------|
| Gradio Docs | https://www.gradio.app/docs |
| HF Spaces Docs | https://huggingface.co/docs/hub/spaces-overview |
| GitHub Actions Docs | https://docs.github.com/en/actions |
| HuggingFace Hub API | https://huggingface.co/docs/huggingface_hub |

---

**Son Düzenleme:** 6 Temmuz 2026
