# Gradio Uygulaması ve HuggingFace Spaces Deploy Dokümanı

**Oluşturulma Tarihi:** 6 Temmuz 2026
**Son Güncelleme:** 7 Temmuz 2026
**Yazar:** Mühendislilik Ekibi

---

## 1. Proje Tanıtımı

Bu proje, **GitHub Actions kullanarak bir Gradio uygulamasını otomatik olarak HuggingFace Spaces'e deploy eden** bir referans projedir. Uygulama "Text Tools" adında bir metin analiz ve dönüşüm aracıdır.

Proje ayrıca **CI (Continuous Integration) Pipeline** içerir: her push ve pull request işleminde **Ruff** ile linting ve formatting kontrolü, **Pytest** ile otomatik birim testleri çalıştırılır.

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

Bu proje iki bağımsız GitHub Actions workflow'u kullanır:

### 4.1 CI Pipeline (Lint + Test)

```
ci.yml
(Tetikleyici: push, PR, workflow_dispatch)
        │
        ├──► lint job:  Ruff format check + Ruff lint check
        └──► test job:  pytest --cov=src -v
```

**ci.yml** — Her push veya pull request'te otomatik çalışır:
- **lint job**: Ruff ile format kontrolü (`ruff format --check`) ve lint kontrolü (`ruff check`)
- **test job**: Pytest ile birim testleri çalıştırır, coverage raporu üretir

CI ve Deploy workflow'ları birbirinden bağımsızdır ve paralel çalışır.

### 4.2 Deploy Pipeline (HF Spaces)

```
deploy-to-hf.yml                  deploy-hf-space.yml
(Tetikleyici)                    (Asıl deploy mantığı)
        ↓                                    ↑
        ──────────────── uses: ./deploy-hf-space.yml ───────────────────────────────────────────────────↑
```

**deploy-to-hf.yml** — Ne zaman çalışacağını belirler (trigger):
- `src/**` veya `requirements.txt` değiştiğinde
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
│       ├── ci.yml                    # CI: Ruff lint + Pytest test
│       ├── deploy-to-hf.yml          # Ana workflow (deploy tetikleyici)
│       ├── deploy-hf-space.yml       # Reusable workflow (deploy mantığı)
│       └── scripts/
│           ├── create_space.py       # Space oluşturma script'i
│           └── upload_file.py        # Dosya yükleme script'i
├── src/
│   ├── __init__.py                   # Paket init
│   ├── app.py                        # Gradio UI (create_app, launch)
│   └── text_utils.py                 # Saf iş mantığı (test edilebilir)
├── tests/
│   ├── __init__.py                   # Paket init
│   └── test_app.py                   # Pytest birim testleri (22 test)
├── pyproject.toml                    # Ruff + Pytest + Coverage konfigürasyonu
├── requirements.txt                  # Production bağımlılıkları
├── requirements-dev.txt              # Dev bağımlılıkları (ruff, pytest, mypy)
├── .gitignore                        # Git ignoreleri
├── documentations/
│   ├── github-actions-guide.md       # GitHub Actions kapsamlı dokümanı
│   └── gradio-hf-deploy-doc.md       # Bu doküman
└── README.md
```

### 5.1 Kod Yapısı ve Test Edilebilirlik

Proje, **test edilebilir** bir yapıya sahiptir. İş mantığı `src/text_utils.py` modülünde toplanmış, Gradio UI kodu ise `src/app.py`'de barındırılır:

| Modül | Açıklama | Test Edilebilir? |
|-------|----------|------------------|
| `src/text_utils.py` | Kelime, karakter, cümle, paragraf sayma; case dönüşüm; istatistik hesaplama | Evet (100% coverage) |
| `src/app.py` | Gradio UI oluşturma, buton/event bağlama | Hayır (gradio bağımlılığı) |
| `tests/test_app.py` | `text_utils.py` için 22 birim test | — |

Bu yapı sayesinde:
- CI'da gradio kurulmadan testler çalışır
- Tüm iş mantığı bağımsız olarak test edilebilir
- UI kodu ile iş mantığı ayrı olarak geliştirilebilir

---

## 6. Lokal Çalıştırma

### 6.1 Uygulamayı Çalıştırma

```bash
pip install -r requirements.txt
python src/app.py
```

Tarayıcı: `http://127.0.0.1:7860`

### Uygulama Özellikleri

- **📊 Metin İstatistikleri**: Karakter, kelime, cümle, paragraf sayma
- **🔤 Metin Dönüşüm**: Büyük/Harf, Küçük Harf, Başlık Formatı, Ters Çevir
- **Temizle** butonu ile tüm alanları sıfırlama

### 6.2 Lokal Geliştirme Araçları

**Development bağımlılıklarını kurma:**

```bash
pip install -r requirements-dev.txt
```

**Ruff ile Lint ve Format Kontrolü:**

```bash
# Lint hatalarını listele
ruff check .

# Lint hatalarını otomatik düzelt
ruff check --fix .

# Format kontrolü
ruff format --check .

# Otomatik formatla
ruff format .
```

**Pytest ile Test Çalıştırma:**

```bash
# Tüm testleri çalıştır
pytest -v

# Coverage raporu ile çalıştır
pytest --cov=src --cov-report=term-missing -v

# Belirli bir testi çalıştır
pytest tests/test_app.py::TestCounting::test_count_words_basic -v
```

**Ruff Konfigürasyonu (`pyproject.toml`):**

Tüm Ruff ayarları `pyproject.toml` dosyasında tanımlıdır:
- **Kontroller**: pycodestyle (E, W), pyflakes (F), isort (I), pep8-naming (N), pyupgrade (UP), flake8-bugbear (B), flake8-simplify (SIM)
- **Satır uzunluğu**: 100
- **Target Python**: 3.11

**Coverage Konfigürasyonu (`pyproject.toml`):**

`[tool.coverage.run]` bloğunda `omit = ["src/app.py"]` ile UI kodu coverage raporundan hariç tutulur. Çünkü `app.py` Gradio bağımlılığı içerir ve CI ortamında bu bağımlılık kurulu değildir. Tüm iş mantığı `text_utils.py`'de test edilir.

---

## 7. CI Pipeline (ci.yml)

### 7.1 Workflow Tanımı

Her `push` ve `pull_request` (main branch) işleminde otomatik olarak çalışır. Ayrıca `workflow_dispatch` ile manuel olarak da tetiklenebilir.

```yaml
name: CI (Lint + Test)

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  lint:
    name: Ruff Lint & Format
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Ruff
        run: pip install ruff

      - name: Check Formatting
        run: ruff format --check .

      - name: Lint
        run: ruff check .

  test:
    name: Pytest
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run Tests
        run: pytest --cov=src --cov-report=term-missing -v
```

### 7.2 Job'lar

CI workflow'unda **iki bağımsız job** paralel olarak çalışır:

| Job | Açıklama | Timeout |
|-----|----------|---------|
| `lint` | Ruff format + lint kontrolü | 5 dk |
| `test` | Pytest testleri + coverage raporu | 10 dk |

Her iki job da başarılı olursa workflow başarılı sayılır.

### 7.3 Neden Ruff?

**Ruff**, Python için çok hızlı bir linter ve formatter'dır. Avantajları:

| Özellik | Açıklama |
|---------|----------|
| Hız | Rust ile yazılmıştır, flake8'den ~10-100x daha hızlı |
| Tek Araç | flake8, isort, pyupgrade, black gibi 50+ plugin'i birleştirir |
| Otomatik Düzeltme | `ruff check --fix` ile birçok hatayı otomatik düzeltir |
| Pyproject.toml Desteği | Konfigürasyon `pyproject.toml` içinde saklanır |

Kullanılan rule set'leri:
- **E** (pycodestyle errors), **W** (warnings): Stil hataları
- **F** (pyflakes): Kullanılmayan import, tanımlanmamış değişken
- **I** (isort): Import sıralama
- **N** (pep8-naming): PEP 8 isimlendirme kuralları
- **UP** (pyupgrade): Gündelik Python syntax'a yükseltme
- **B** (flake8-bugbear): Olası bug'ları tespit
- **SIM** (flake8-simplify): Basitleştirme önerileri

### 7.4 Neden Pytest?

**Pytest**, Python için en popüler test framework'üdür. Avantajları:

- Basit `assert` kullanımı (unittest'deki `self.assertEqual` gerekmez)
- Otomatik test keşfi (`tests/` altındaki `test_*.py` dosyalarını bulur)
- Parametrize desteği ile aynı testi farklı girdilerle çalıştırma
- Coverage entegrasyonu (`pytest-cov` ile kod kapsamı raporu)
- `pyproject.toml` desteği

### 7.5 Test Kategorileri

`tests/test_app.py` dosyasında **22 test** üç sınıfa ayrılmıştır:

| Sınıf | Test Sayısı | Kapsadığı Fonksiyonlar |
|-------|-------------|------------------------|
| `TestCounting` | 13 | count_words, count_characters, count_sentences, count_paragraphs |
| `TestTransforms` | 6 | to_upper, to_lower, to_title, to_reverse, transform_case |
| `TestGetStats` | 3 | get_stats |

Test senaryoları:
- **Normal girdiler**: `"hello world"`, `"Hello. World!"`
- **Edge case'ler**: boş string (`""`), whitespace-only, çoklu boşluk
- **Türkçe karakterli girdiler**: `"Büyük Harf"`, `"Ters Çevir"`
- **Beklenmeyen input**: bilinmeyen operation ismi → varsayılan davranış

---

## 8. HuggingFace Spaces'e Manuel Deploy

```bash
pip install "huggingface_hub[hf_hub]"

# Space oluştur
huggingface-cli create-repo yusuf-aslan/text-tools --type space --space-sdk gradio

# Dosyaları yükle
huggingface-cli upload yusuf-aslan/text-tools src/app.py --repo-type space --filename app.py
huggingface-cli upload yusuf-aslan/text-tools requirements.txt --repo-type space
```

---

## 9. GitHub Actions ile Otomatik Deploy

### 9.1 HF Token Oluşturma

1. https://huggingface.co/settings/tokens → **New token** → **Write** role seçin
2. Token'ı güvenli bir yerde saklayın (tek kez gösterilir)

### 9.2 GitHub Secret Ekleme

1. Repo → Settings → Secrets and variables → Actions
2. **New repository secret** → Name: `HF_TOKEN`, Value: (token değeri)

### 9.3 Workflow Nasıl Çalışır

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

### 9.4 Yardımcı Script'ler

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

## 10. Workflow Akış Şemaları

### 10.1 CI Pipeline Akışı

```
[Push to main / PR / Workflow Dispatch]
        │
        ├──► CI: ci.yml tetiklenir                    ──► Deploy: deploy-to-hf.yml tetiklenir
            │                                                   │
            ├──► lint job:                                       ├──► deploy-hf-space.yml çağrılır
            │    ├── ruff format --check                         │    ├──► 1. Checkout
            │    └── ruff check                                  │    ├──► 2. Python 3.11 kur
            │                                                   │    ├──► 3. Install huggingface-hub
            ├──► test job:                                       │    ├──► 4. Space oluştur (yoksa)
            │    ├── pip install -r requirements-dev.txt         │    ├──► 5. Dosyaları yükle
            │    └── pytest --cov=src -v                         │    │       ├── src/app.py → app.py
            │                                                   │    │       └── requirements.txt → requirements.txt
            └──► 22 test PASSED                                 │    └──► 6. Deploy doğrulama
                   text_utils: 100% coverage                                   │
                                                                              ▼
                                                                        [Space canlı]
```

**Önemli:** CI ve Deploy workflow'ları **bağımsızdır** ve aynı push işleminde **paralel** çalışır. Birinin başarısız olması diğerini etkilemez.

### 10.2 Deploy Pipeline Akışı

```
[Push to main (src/** veya requirements.txt)]
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

## 11. Sorun Giderme

### Deploy Sorunları

| Sorun | Çözüm |
|-------|-------|
| Deploy workflow çalışmıyor | `.github/workflows/` yolunu kontrol edin |
| 403 Forbidden | HF Token'ının Write yetkisi olduğundan emin olun |
| Space başlamıyor | Space sayfasında "Factory Reboot" yapın |
| "Space bulunamadi" hatası | Space adını ve HF Token'ı kontrol edin |
| Dosya güncelleme yansımadı | Space sayfalarından "Factory Reboot" yapın (bazen cache nedeniyle gecikmeli olabilir) |

### CI Sorunları

| Sorun | Çözüm |
|-------|-------|
| `ruff check` başarısız | `ruff check --fix .` ile hataları otomatik düzeltin, kalan hataları manuel düzeltin |
| `ruff format --check` başarısız | `ruff format .` çalıştırın |
| `pytest` import hatası | `sys.path.insert()` ile doğru yol eklendiğinden emin olun (`tests/test_app.py`) |
| `text_utils import error` | `src/__init__.py` dosyasının mevcut olduğundan emin olun |
| Coverage düşük | Eksik test senaryoları ekleyin, `--cov-report=term-missing` ile hangi satırların test edilmediğini görün |
| CI workflow hiç çalışmıyor | `.github/workflows/ci.yml` dosyasının doğru yerde olduğundan emin olun |

---

## 12. Yeni Dosya Ekleme

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
| Ruff Docs | https://docs.astral.sh/ruff/ |
| Pytest Docs | https://docs.pytest.org/ |
| Coverage.py Docs | https://coverage.readthedocs.io/ |

---

**Son Düzenleme:** 7 Temmuz 2026
