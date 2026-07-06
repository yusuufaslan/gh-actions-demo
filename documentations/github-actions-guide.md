# GitHub Actions Kapsamlı Dokümanı

**Oluşturulma Tarihi:** 6 Temmuz 2026
**Son Güncelleme:** 6 Temmuz 2026
**Yazar:** Mühendislilik Ekibi
**Durum:** Aktif

---

## 📋 İçindekiler

1. [Giriş](#1-giriş)
2. [GitHub Actions Nedir?](#2-github-actions-nedir)
3. [Neden GitHub Actions?](#3-neden-github-actions)
4. [Temel Kavramlar](#4-temel-kavramlar)
5. [Workflow Dosyası Yapısı](#5-workflow-dosyası-yapısı)
6. [Trigger'lar (Tetikleyiciler)](#6-triggerlar-tetikleyiciler)
7. [Actions Hub ve Hazır Actions](#7-actions-hub-ve-hazır-actions)
8. [Kendi Action'ınızı Yazma](#8-kendi-actionlarınızı-yazma)
9. [Environment Variables ve Secrets](#9-environment-variables-ve-secrets)
10. [Cache ve Artifact'lar](#10-cache-ve-artifactlar)
11. [Matrix Builds](#11-matrix-builds)
12. [Gelişmiş Konular](#12-gelişmiş-konular)
13. [Practical Örnekler](#13-practical-örnekler)
14. [En İyi Uygulamalar](#14-en-ıyi-uygulamalar)
15. [Sık Karşılaşılan Hatalar ve Çözümleri](#15-sık-karşılaşılan-hatalar-ve-çözümleri)
16. [Sıfırdan Sonuçlandırılmış Proje: Gradio → HuggingFace Spaces](#16-sıfırdan-sonuçlandırılmış-proje-gradio--huggingface-spaces)

---

## 1. Giriş

### 1.1 Hedef Kitle

Bu doküman, CI/CD (Continuous Integration/Continuous Deployment - Sürekli Entegrasyon/Sürekli Dağıtım) ve GitHub Actions konularına yeni başlayan geliştiriciler için hazırlanmıştır. Temel Git ve terminal bilginizin olması yeterlidir.

### 1.2 Öğrenme Hedefleri

Bu dokümanı tamamladıktan sonra şunları yapabileceksiniz:

- GitHub Actions'ın ne olduğunu ve neden ihtiyacımız olduğunu açıklayabileceksiniz
- Workflow, Job, Step, Action kavramlarını birbirinden ayırt edebileceksiniz
- YAML formatında workflow dosyaları yazabileceksiniz
- Mevcut Actions Marketplace'ten hazır action'ları kullanabileceksiniz
- Slack, Discord, Email gibi bildirim servislerini entegre edebileceksiniz
- Kendi özel action'ınızı sıfırdan yazabileceksiniz
- Secrets (gizli değerler) yönetimini güvenle yapabileceksiniz
- Bir Python projesini otomatik olarak HuggingFace Spaces'e deploy edebileceksiniz

### 1.3 CI/CD Nedir?

**CI - Continuous Integration (Sürekli Entegrasyon):**
Kod değişikliklerinin sık sık ana branch'e entegre edilmesidir. Her entegrasyonda otomatik testler çalıştırılarak hataların erken tespit edilmesi hedeflenir.

**CD - Continuous Deployment/Delivery (Sürekli Dağıtım):**
Testleri başarıyla geçen kodun otomatik olarak staging veya production ortamlarına dağıtılmasıdır.

**Neden Önemli?**
- Manuel deploy süreçlerini ortadan kaldırır
- İnsan hatası riskini minimize eder
- Her deploy tekrarlanabilir ve izlenebilir olur
- Takım productivity'si artar

---

## 2. GitHub Actions Nedir?

### 2.1 Tanım

GitHub Actions, GitHub üzerinde doğrudan çalıştırılabilen bir **CI/CD platformudur**. Kodunuzun her değişiminde otomatik iş akışları (workflows) çalıştırmanızı sağlar.

### 2.2 Nasıl Çalışır?

1. Bir repo içinde `.github/workflows/` klasörü oluşturursunuz
2. Bu klasörün içine `.yml` veya `.yaml` uzantılı workflow dosyaları yazarsınız
3. Belirttiğiniz koşullar sağlandığında (push, pull request, schedule vb.) GitHub bu dosyaları okur
4. Workflow içinde tanımlanan adımlar sırayla çalışır

### 2.3 Runner'lar

Workflow'larınız GitHub'ın sağladığı sunucularda çalışır. Bu sunuculara **Runner** denir:

| Runner | İşletim Sistemi | Aylık Dakika (Free) |
|--------|-----------------|---------------------|
| `ubuntu-latest` | Linux (Ubuntu) | 2.000 dk |
| `windows-latest` | Windows | 2.000 dk |
| `macos-latest` | macOS | 2.000 dk |
| Self-hosted | Herhangi bir sunucu | Sınırsız |

Public repolar için dakikalar ücretsizdir. Private repolar için yukarıdaki limitler geçerlidir.

### 2.4 GitHub Actions vs Diğer CI/CD Araçları

| Özellik | GitHub Actions | Jenkins | GitLab CI | CircleCI |
|---------|---------------|---------|-----------|----------|
| Kurulum | Yok (cloud) | Self-host | Built-in | SaaS |
| Marketplace | 10.000+ action | Plugins | Yes | Orbs |
| Fiyat | Free (public) | Free | Free | Free tier |
| GitHub İntegrasyonu | Native | Plugin | Plugin | Plugin |

---

## 3. Neden GitHub Actions?

### 3.1 Avantajlar

- **GitHub ile doğrudan entegre**: Ayrı bir araç kurulumuna gerek yok
- **Actions Marketplace**: 10.000+ hazır action topluluğu tarafından paylaşılmış
- **Çoklu OS desteği**: Ubuntu, Windows, macOS runner'ları
- **Ücretsiz**: Public repos için sınırsız kullanım
- **YAML tabanlı**: Kodunuzla aynı repo'da saklanır, version control destekli
- **Güçlü context sistemi**: `${{ }}` syntax ile event bilgilerine erişim
- **Secrets yönetimi**: Hassas veriler güvenle saklanır
- **Reusable Workflows**: Tekrarlanan mantık ortak workflow'larda toplanır

### 3.2 Ne Zaman Kullanılır?

- Kod değişikliklerinde test çalıştırma
- Otomatik deployment (web, API, mobile)
- Docker image build ve push
- Dependency güncellemelerini kontrol etme
- Pull request'lerde kod kalitesi kontrolü (lint, format)
- Otomatik bildirim gönderme (Slack, Discord, Email)
- Scheduled işlemler (daily backup, health check)

---

## 4. Temel Kavramlar

```
Repository
  ↳ Workflow (.yml dosyası - bir iş akışı tanımı)
    ↳ Job (workflow içindeki bağımsız bir birim)
      ↳ Step (job içindeki sıralı adımlar)
        ↳ Run / Uses (her step'in çalıştıracağı komut veya action)
```

### 4.1 Workflow

Bir workflow, `.github/workflows/` dizini altında bulunan YAML dosyasıdır. Bir workflow birden fazla job içerebilir. Workflow'lar belirli event'larla tetiklenir veya manuel olarak başlatılabilir.

### 4.2 Job

Bir workflow'daki bağımsız bir iş bloğudur. Her job kendi.runner'ında çalışır. Varsayılan olarak job'lar paralel çalışır.

### 4.3 Step

Bir job içindeki sıralı adımdır. Step'ler sırayla (sequential) çalışır. Her step ya bir `run` komutu içerir ya da `uses` ile hazır bir action çağırır.

### 4.4 Action

Tekrar kullanılabilir bir kod parçasıdır. `uses:` ile çağrılır.

Action türleri:
- **Shell script**: `run:` bloğlarında çalıştırılan komutlar
- **Docker action**: Docker image'ı çalıştıran action'lar
- **JavaScript action**: Node.js ile yazılmış action'lar (en yaygın)
- **Composite action**: Birden fazla step'i bir arada tanımlayan action'lar

---

## 5. Workflow Dosyası Yapısı

Bir workflow dosyası YAML formatındadır ve şu temel bölümlerden oluşur:

```yaml
name: CI Pipeline

# Workflow ne zaman çalışır?
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Workflow seviyesinde çevre değişkenleri
env:
  PYTHON_VERSION: "3.11"

# Workflow jobs
jobs:
  # Job 1: test
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "${{ env.PYTHON_VERSION }}"
      - run: |
          pip install -r requirements.txt
          pytest tests/ -v

  # Job 2: deploy (test başarılı olduktan sonra)
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

### 5.1 `name` — Workflow Adı

Workflow'un GitHub Actions sekmesinde görünen adıdır. Belirtmezseniz GitHub otomatik bir isim atar.

### 5.2 `on` — Tetikleyiciler

Workflow'un ne zaman çalışacağını belirler. Tek bir event veya birden fazla event tanımlanabilir.

### 5.3 `env` — Environment Variables

Workflow seviyesinde tanımlanan değişkenler tüm job ve step'lerde erişilebilir.

### 5.4 `jobs` — Job Tanımları

Tüm iş birimleri bu blok altında tanımlanır.

### 5.5 `runs-on` — Runner Seçimi

Job'un hangi işletim sisteminde çalışacağını belirler.

### 5.6 `steps` — Adımlar

Job içindeki sıralı adımlar. Her step'in `name`, `uses` veya `run` alanları olabilir.

### 5.7 `needs` — Job Bağımlılıkları

Bir job'un başka bir job'un tamamlanmasını beklemesini sağlar:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing..."

  deploy:
    needs: test  # test başarılı olursa çalışır
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

Bir job birden fazla job'a bağımlı olabilir:

```yaml
integration:
  needs: [unit-test, lint, type-check]
  runs-on: ubuntu-latest
```

### 5.8 Context Syntax: `${{ }}`

GitHub Actions özel bir ifade dilini destekler. Sıklıkla kullanılan context'ler:

| Context | Açıklama | Örnek |
|---------|----------|-------|
| `github` | Event bilgileri | `${{ github.sha }}`, `${{ github.actor }}` |
| `env` | Environment variables | `${{ env.NODE_VERSION }}` |
| `secrets` | Gizli değerler | `${{ secrets.DB_PASSWORD }}` |
| `steps` | Önceki step sonuçları | `${{ steps.login.outputs.sdk_version }}` |
| `needs` | Önceki job sonuçları | `${{ needs.build.outputs.artifact }}` |
| `matrix` | Matrix değişkenleri | `${{ matrix.os }}` |
| `inputs` | Manual trigger inputları | `${{ inputs.deploy_env }}` |

### 5.9 İfaden İçinde Değişken Kullanma (YAML Context)

`$` ile başlatarak YAML içinde doğrudan değişken kullanabilirsiniz:

```yaml
jobs:
  build:
    env:
      REGISTRY: ghcr.io
    steps:
      - run: echo $REGISTRY
```

---

## 6. Trigger'lar (Tetikleyiciler)

### 6.1 `push` — Kod Değişikliklerinde

Branch'e push yapıldığında tetiklenir:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!src/test*'
```

`paths` ile hangi dosya değişikliklerinin workflow'u çalıştıracağını filtreleyebilirsiniz:
- `'src/**'` → `src/` altında tüm değişiklikler
- `'!src/test*'` → test klasöründeki değişiklikleri hariç tut
- `'requirements.txt'` → sadece bu dosya değişirse çalışır
- `'.github/workflows/**'` → workflow dosyaları değişirse çalışır

### 6.2 `pull_request` — Pull Request Oluşunca

```yaml
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```

`types` ile hangi PR olaylarının tetikleyeceğini belirtebilirsiniz:
- `opened` — yeni PR oluşturulduğunda
- `synchronize` — PR'ya yeni commit geldiğinde
- `reopened` — kapatılan PR tekrar açıldığında
- `closed` — PR kapatıldığında (merge veya dismiss)

### 6.3 `schedule` — Zamanlanmış Çalışma

Cron syntax kullanır (UTC saat diliminde):

```yaml
on:
  schedule:
    - cron: '0 2 * * *'       # Her gün 02:00 UTC
    - cron: '0 9 * * 1'       # Her Pazartesi 09:00 UTC
    - cron: '*/15 * * * *'    # Her 15 dakikada bir
    - cron: '0 0 1 * *'       # Her ayın 1'inde gece yarısı
```

Cron formatı: `dakika saat gün ay hafta`

> **Not:** Scheduled workflow'lar sadece açık (open) branch'lerde çalışır. Repo'da branch protection kuralları varsa, scheduled trigger'larda `GITHUB_TOKEN` ile merge işlemi yapılamaz.

### 6.4 `workflow_dispatch` — Manuel Tetikleme

Workflow'un GitHub Actions sekmesinden manuel olarak çalıştırılmasına olanak tanır:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy edilecek ortam'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      version:
        description: 'Sürüm numarası'
        required: false
        type: string
```

### 6.5 `workflow_call` — Reusable Workflow

Bir workflow'nun başka bir workflow tarafından çağrılabilmesini sağlar:

```yaml
# reusable.yml
on:
  workflow_call:
    inputs:
      env:
        required: true
        type: string
      image_tag:
        required: false
        type: string
        default: 'latest'
    secrets:
      API_KEY:
        required: true
    outputs:
      image:
        value: ${{ jobs.build.outputs.image }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.meta.outputs.tags }}
    steps:
      - run: echo "Building for ${{ inputs.env }}"
```

Çağıran workflow:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable.yml
    with:
      env: production
      image_tag: v1.2.0
    secrets:
      API_KEY: ${{ secrets.PROD_API_KEY }}
```

### 6.6 `workflow_run` — Başka Workflow Sonucunda

Başka bir workflow tamamlandığında tetiklenir:

```yaml
on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types:
      - completed
```

### 6.7 Birden Fazla Trigger

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

---

## 7. Actions Hub ve Hazır Actions

GitHub Actions Marketplace (https://github.com/marketplace?type=actions) binlerce hazır action içerir.

### 7.1 GitHub tarafından sağlanan temel action'lar

| Action | Kullanım | Açıklama |
|--------|----------|----------|
| `actions/checkout@v4` | `uses: actions/checkout@v4` | Repo kodunu checkout eder |
| `actions/setup-python@v5` | `with: { python-version: '3.11' }` | Python ortamı kurar |
| `actions/setup-node@v4` | `with: { node-version: '20' }` | Node.js ortamı kurar |
| `actions/cache@v4` | PATH + key ile cache | Bağımlılıkları önbelleğe alır |
| `actions/upload-artifact@v4` | `with: { name: 'build' }` | Build çıktılarını saklar |
| `actions/download-artifact@v4` | `with: { name: 'build' }` | Artifact'ları indirir |
| `actions/upload-pages-artifact@v3` | | GitHub Pages artifact |
| `actions/dependency-review-action@v4` | PR'da çağrılır | Güvenlik açıkları tarar |

### 7.2 Checkout Detaylı Kullanım

```yaml
- uses: actions/checkout@v4
  with:
    submodules: true          # Sub-modules dahil et
    fetch-depth: 0            # Tüm git geçmişini çek (varsayılan 1)
    ref: 'develop'            # Belirli bir branch/check
```

### 7.3 Python Setup Detaylı Kullanım

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'              # pip cache otomatik
    architecture: 'x64'       # x86 veya x64
```

### 7.4 Docker Action'ları

**Build ve Push:**

```yaml
- uses: actions/checkout@v4
- uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: myuser/myapp:latest,myuser/myapp:v1.0
```

**GitHub Container Registry'ye Push:**

```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
- uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/myuser/myapp:latest
```

### 7.5 Bildirim Action'ları

#### Slack Bildirimi

Workflow başarılı veya başarısız olduğunda Slack'e bildirim gönderir:

**Kurulum:**
1. Slack → Apps → Create an App → Slack OAuth token oluştur
2. Repo → Settings → Secrets → `SLACK_WEBHOOK_URL` ekle

**Kullanım:**

```yaml
name: Deploy & Notify Slack
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: echo "Deploying..."

    if: always()
    steps:
      - name: Slack Notification
        uses: slackapi/slack-github-action@v1.27.0
        with:
          payload: |
            {
              "text": "Deploy durumu: ${{ job.status }}\n",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Deploy tamamlandı!* :rocket:\n> Repo: ${{ github.repository }}\n> Branch: ${{ github.ref_name }}\n> Commit: ${{ github.sha }}\n> Actor: ${{ github.actor }}\n> Durum: ${{ job.status }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Discord Bildirimi

```yaml
- name: Discord Notification
  uses: Ilshidur/action-discord@master
  with:
    args: "Deploy ${{ job.status }} - ${{ github.repository }} - Commit: ${{ github.sha }}"
  env:
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
```

#### Email Bildirimi

```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_APP_PASSWORD }}
    subject: "Deploy Durumu: ${{ job.status }}"
    body: |
      Deploy sonuc: ${{ job.status }}
      Repo: ${{ github.repository }}
      Commit: ${{ github.sha }}
    to: team@example.com
    from: ci-notifier@example.com
```

### 7.6 Şablon Yükleme / GitHub Pages Action'ları

```yaml
- uses: actions/deploy-pages@v4
```

### 7.3 Hazır Action Sürümleme İyisi Uygulama

Her zaman sabit sürüm kullanın:
- ✅ `actions/checkout@v4` — sürüm etiketi
- ✅ `actions/checkout@ee0669bd1cc54295c223e0bb097b7b8e20e2bde` — tam commit SHA (en güvenli)
- ❌ `actions/checkout@master` — branch name, sürüm değişebilir

---

## 8. Kendi Action'ınızı Yazma

3 farklı şekilde action yazabilirsiniz:

### 8.1 Composite Action

Birden fazla step'i tek bir action içinde paketler. YAML tabanlıdır, farklı bir dil bilmeye gerek yoktur:

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Python ortamını ve bağımlılıkları kurar'

runs:
  using: 'composite'
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: |
        pip install --upgrade pip
        pip install -r requirements.txt
      shell: bash
```

Kullanımı:

```yaml
- uses: ./.github/actions/setup-project
```

### 8.2 JavaScript Action

Node.js kullanılarak oluşturulur. En esnek yöntemdir:

```
my-action/
├── action.yml         # Action manifesti
├── index.js           # Ana kod
├── package.json       # Bağımlılıklar
└── dist/              # Oluşturulmuş dosyalar
```

```yaml
# action.yml
name: 'Kullanıcı Selamları'
description: 'Verilen kullanıcıya selam gönderir'
inputs:
  username:
    description: 'Kullanıcı adı'
    required: true
outputs:
  greeting:
    description: 'Selamlama mesajı'
    value: ${{ steps.hello.outputs.result }}
runs:
  using: 'node20'
  main: 'index.js'
```

```javascript
// index.js
const core = require('@actions/core');

async function main() {
  const username = core.getInput('username');
  const greeting = `Merhaba ${username}!`;
  core.setOutput('greeting', greeting);
  console.log(greeting);
}

main();
```

### 8.3 Docker Action

Docker container ile çalışır:

```yaml
# action.yml
name: 'Docker Action'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

```dockerfile
# Dockerfile
FROM alpine:3.18
RUN apk add --no-cache curl
ENTRYPOINT ["curl", "--version"]
```

---

## 9. Environment Variables ve Secrets

### 9.1 Secrets Ekleme

GitHub'da güvenle saklanan hassas bilgilerdir:
1. Repo → Settings → Secrets and variables → Actions
2. **New repository secret** tıklanır
3. Name ve Value girilir

**Önemli:** Secrets workflow loglarında gösterilmez. Ancak, komut çıktılarında yanlışlıkla yazdırılabilirler. Dikkatli olun.

```yaml
# ✅ Doğru - secret kullanma
- run: echo "Deploying with token"
  env:
    TOKEN: ${{ secrets.HF_TOKEN }}
```

```yaml
# ❌ Yanlış - secret loglarda görünür
- run: echo "Token: ${{ secrets.HF_TOKEN }}"
```

### 9.2 Environment Variables Düzeyleri

Değişkenler dört düzeyde tanımlanabilir:

```yaml
name: Variable Düzeyleri
on: push

# Düzey 1: Workflow seviyesi
env:
  GLOBAL_VAR: "workflow-wide"

jobs:
  build:
    runs-on: ubuntu-latest

    # Düzey 2: Job seviyesi
    env:
      JOB_VAR: "job-wide"

    steps:
      # Düzey 3: Step seviyesi
      - name: Step Scope
        env:
          STEP_VAR: "step-only"
        run: echo "$GLOBAL_VAR $JOB_VAR $STEP_VAR"

      # Düzey 4: Komut seviyesi
      - run: |
          CMD_VAR="command-level" echo "$CMD_VAR"
```

### 9.3 Environment Protection Rules

Belirli ortamları korumak için environment tanımlayabilirsiniz:

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.example.com
    steps:
      - run: echo "Deploying to production"
```

Settings → Environments'ta şu kurallar tanımlanabilir:
- **Required reviewers** → deploy'dan önce insan onayı
- **Wait timer** → approval'dan sonra belirtilen süre kadar bekler
- **Protection rules** → belirli branch'lerden deploy etme

---

## 10. Cache ve Artifact'lar

### 10.1 Cache

`actions/cache@v4` ile bağımlılıkları önbelleğe alın:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Nasıl Çalışır:**
1. `key` ile eşleşen cache varsa yüklemeler atlanır
2. Eşleşme yoksa `restore-keys` ile kısmi eşleşme denenir
3. Hiçbir eşleşme yoksa cache boş başlar

`actions/setup-python@v5` ile `cache: 'pip'` kullanıldığında otomatik cache de mümkündür:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

### 10.2 Artifacts

`actions/upload-artifact@v4` ile build çıktılarını saklayın:

```yaml
# Upload
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: reports/
    retention-days: 7

# Bir başka job'da indirme
- uses: actions/download-artifact@v4
  with:
    name: test-results
    path: ./reports/
```

**Artifact vs Cache:**
- **Cache**: Performans iyileştirmesi amaçlı, key tabanlı
- **Artifact**: Build çıktılarını saklamak için, joblar arası veri geçişi

---

## 11. Matrix Builds

Farklı ortamlarda aynı workflow'u paralel olarak çalıştırır:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.9', '3.10', '3.11']

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.9', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: |
          pip install pytest
          pytest tests/ -v
```

Bu örnekte 2 OS x 3 Python versi = **6 paralel job** çalışır.

### Matrix İstekli Kullanma

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.9', '3.11']
    include:
      - os: ubuntu-latest
        python-version: '3.12'
        experimental: true
    exclude:
      - os: windows-latest
        python-version: '3.9'
```

---

## 12. Gelişmiş Konular

### 12.1 Concurrency

Aynı workflow'nun birden fazla kez paralel çalışmasını önlemeye yarar:

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

Bu tanımla:
- Aynı branch'e ardışık push'lar yapıldığında, önceki workflow iptal edilir
- Farklı branch'ler birbirini etkilemez

### 12.2 Conditional Execution

```yaml
- name: Debug (sadece develop'ta)
  if: github.ref == 'refs/heads/develop'
  run: |
    pip install debugpy
    python -m debugpy --listen 5678 app.py

- name: Release (sadece tag'le)
  if: startsWith(github.ref, 'refs/tags/v')
  run: echo "Releasing $GITHUB_REF_NAME"
```

Önemli koşullar:
- `if: always()` — bağımsız olarak çalış
- `if: failure()` — önceki step başarısızsa çalış
- `if: success()` — önceki step başarılıysa çalış (varsayılan)
- `if: cancelled()` — iptal edilmişse çalış
- `if: github.event_name == 'push'`

### 12.3 Timeout

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # 10 dakikada sonra workflow iptal edilir
    steps:
      - run: pytest tests/
```

### 12.4 Output Sharing Between Steps

```yaml
steps:
  - id: login
    uses: docker/login-action@v3
    with:
      registry: ghcr.io

  - id: meta
    uses: docker/metadata-action@v5
    with:
      images: ghcr.io/myuser/myapp

  - run: echo ${{ steps.meta.outputs.tags }}
```

### 12.5 Path-Based Triggers ile Farklı Workflow Tarihinde

Aynı repo'da birden fazla workflow ve her biri farklı dosyaları izler:

```yaml
# test.yml - Sadece testler değişince
on:
  push:
    paths:
      - 'tests/**'
      - 'src/**'

# docs.yml - Sadece dokümantasyon değişince
on:
  push:
    paths:
      - 'documentations/**'
```

---

## 13. Practical Örnekler

### 13.1: CI Pipeline

Pull request'lerde otomatik lint ve test:

```yaml
name: CI Pipeline
on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          pip install ruff
          ruff check .
          ruff format --check .

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: |
          pip install -r requirements.txt
          pytest tests/ -v --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-report
          path: report.xml
```

### 13.2 Docker Build and Push

```yaml
name: Docker CI
on:
  push:
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            myuser/myapp:latest
            myuser/myapp:${{ github.ref_name }}
```

### 13.3 Slack Bildirim ile Deploy

Deploy tamamlandığında Slack'e bildirim gönderen bir workflow:

```yaml
name: Deploy & Notify
on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Deploy
        id: deploy
        run: |
          echo "Deploy to ${{ github.event.inputs.environment }}"
          # Deploy komutu buraya

      - name: Slack - Başarılı
        if: success()
        uses: slackapi/slack-github-action@v1.27.0
        with:
          payload: |
            {
              "text": "✅ Deploy başarılı!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*✅ Deploy Başarılı*\n> Ortam: ${{ github.event.inputs.environment }}\n> Actor: ${{ github.actor }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Slack - Başarısız
        if: failure()
        uses: slackapi/slack-github-action@v1.27.0
        with:
          payload: |
            {
              "text": "❌ Deploy başarısız!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*❌ Deploy Başarısız*\n> Ortam: ${{ github.event.inputs.environment }}\n> Commit: ${{ github.sha }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 13.4: Reusable Workflow ile Multi-Env Deploy

Ortak deploy mantığını farklı ortamlarda tekrar kullanma:

**Reusable deploy workflow** `deploy-reusable.yml`:

```yaml
name: Deploy (Reusable)
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_TOKEN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - run: |
          echo "Deploying to ${{ inputs.environment }}"
      - env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: echo "Using token for ${{ inputs.environment }}"
```

**Ana workflow** `deploy-pipeline.yml`:

```yaml
name: Deploy Pipeline
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: staging
    secrets:
      DEPLOY_TOKEN: ${{ secrets.STAGING_TOKEN }}

  deploy-production:
    needs: deploy-staging
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: production
    secrets:
      DEPLOY_TOKEN: ${{ secrets.PROD_TOKEN }}
```

---

## 14. En İyi Uygulamalar

### 14.1 Performans

1. **Cache kullanın**: `actions/cache@v4` veya `cache: 'pip'` ile bağımlılığı önbelleğe alın
2. **Path filter kullanın**: İlgisiz dosyalar için workflow çalıştırmayın
3. **Checkout shallow fetch**: `fetch-depth: 1` (varsayılan) kullanın

### 14.2 Güvenlik

4. **Versiyonlu action kullanın**: `@v4` gibi sürüm etiketleri kullanın
5. **Secrets kullanın**: Hassas verileri workflow içinde açık olarak yazmayın
6. **Minimal izin kullanın**: `permissions:` bloğu ile gereksiz izinleri kapattırın
7. **Third-party action'larını inceleyin**: Açık kaynak olmayan action'lar şüpheli olabilir

### 14.3 Okunabilirlik

8. **Step isimleri verin**: Her adıma açıklayıcı bir `name:` ekleyin
9. **Reusabale workflow kullanın**: Tekrarlanan mantığı ortak dosyalarda toplayın
10. **Concurrency kullanın**: Gereksiz paralel çalışmaları önleyin
11. **Comment kullanın**: Karmaşık adımları yorumlayın

### 14.4 Özet Checklist

| Pratik | Neden |
|--------|-------|
| ✅ Cache kullanın | CI süresi kısalır |
| ✅ Path filter | Gereksiz çalıştırmalar azalır |
| ✅ Versiyonlu action | Beklenmedik kırılmalar önlenir |
| ✅ Secrets | Hassas veriler koruma altında |
| ✅ Concurrency | Gerekli kaynak tüketimi azaltılır |
| ✅ Minimal izin | Güvenlik riski düşer |
| ✅ Step isimleri | Debug süreci kolaylaşır |
| ✅ Reusable workflow | Kod tekrarı azalır |

---

## 15. Sık Karşılaşılan Hatalar ve Çözümleri

| Hata | Neden | Çözüm |
|------|-------|-------|
| `Permission denied (publickey)` | `GITHUB_TOKEN` yetki eksik | `permissions: { contents: write }` ekleyin |
| `Action not found` | Action adı yanlış | Action adını ve sürümü kontrol edin |
| `Cache hit failed` | Cache key eşleşmiyor | `hashFiles()` pattern'ını kontrol edin |
| `Timeout` | Job çok uzun sürüyor | `timeout-minutes` artırın veya işi parçalayın |
| `Self-hosted runner error` | Self-hosted runner offline | Runner'ı yeniden başlatın |
| `Secret not found` | Secret adında yanlış yazım | Settings > Secrets kontrol edin |
| `403 Forbidden` | Token yetki eksik | Token scope'larını genişletin |
| `Concurrency cancelled` | Önceki çalıştırma iptal edilmiş | `concurrency` gruba unique bir değer verin |
| `Job skipped` | `needs`'deki job başarısız | Önceki job'un neden başarısızlandığını inceleyin |

---

## 16. Sıfırdan Sonuçlandırılmış Proje: Gradio → HuggingFace Spaces

Bu dokümanın son bölümünde, GitHub Actions kullanarak bir Gradio uygulamasını otomatik olarak HuggingFace Spaces'e nasıl deploy edeceğinizi öğrenirsiniz.

Ayrıntılı bilgi için **[Gradio HF Spaces Deploy Dokümanı](./gradio-hf-deploy-doc.md)** bakınız.

Bu proje şu konuları kapsar:
- Reusable workflow kullanımı (`workflow_call`)
- `huggingface_hub` Python kütüphanesi ile API kullanımı
- Secrets yönetimi (HF_TOKEN)
- Path-based trigger'lar ile seçici deployment
- Manuel tetikleyici (workflow_dispatch) kullanımı

---

## Ek Kaynaklar

| Kaynak | Link |
|--------|------|
| GitHub Actions Docs | https://docs.github.com/en/actions |
| Actions Marketplace | https://github.com/marketplace?type=actions |
| Expression Syntax | https://docs.github.com/en/actions/learn-github-actions/expressions |
| Context Reference | https://docs.github.com/en/actions/learn-github-actions/contexts |
| Gradio Docs | https://www.gradio.app/docs |
| HF Spaces Docs | https://huggingface.co/docs/hub/spaces-overview |

---

**Son Düzenleme:** 6 Temmuz 2026
