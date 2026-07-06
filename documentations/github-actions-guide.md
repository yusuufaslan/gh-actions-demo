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
6. [Trigger'lar (Tetikleyiciler)](#6-triggerları-tetikleyiciler)
7. [Actions Hub ve Hazır Actions](#7-actions-hub-ve-hazır-actions)
8. [Kendi Action'ınızı Yazma](#8-kendi-actionınızı-yazma)
9. [Environment Variables ve Secrets](#9-environment-variables-ve-secrets)
10. [Cache ve Artifact'lar](#10-cache-ve-artifactlar)
11. [Matrix Builds](#11-matrix-builds)
12. [Practical Örnekler](#12-practical-örnekler)
13. [En İyi Uygulamalar](#13-en-ıyi-uygulamalar)
14. [Sık Karşılaşılan Hatalar ve Çözümleri](#14-sık-karşılaşılan-hatalar-ve-çözümleri)
15. [Sıfırdan Sonuçlandırılmış Proje: Gradio → HuggingFace Spaces](#15-sıfırdan-sonuçlandırılmış-proje-gradio--huggingface-spaces)

---

## 1. Giriş

### 1.1 Hedef Kitle
Bu doküman, CI/CD (Continuous Integration/Continuous Deployment - Sürekli Entegrasyon/Sürekli Dağıtım) ve GitHub Actions konularına yeni başlayan geliştiriciler için hazırlanmıştır. Temel Git bilginizin olması yeterlidir.

### 1.2 Öğrenme Hedefleri
Bu dokümanı tamamladıktan sonra şunları yapabileceksiniz:

- GitHub Actions'ın ne olduğunu ve neden ihtiyaçmız olduğunu açıklayabileceksiniz
- Workflow, Job, Step, Action kavramlarını birbirinden ayırt edebileceksiniz
- YAML formatında workflow dosyaları yazabileceksiniz
- Mevcut Actions Marketplace'ten hazır action'ları kullanabileceksiniz
- Kendi özel action'ınızı sıfırdan yazabileceksiniz
- Secrets (gizli değişenler) yönetimini güvenle yapabileceksiniz
- Bir Python projesini otomatik olarak HuggingFace Spaces'e deploy edebileceksiniz

### 1.3 CI/CD Nedir?

**CI - Continuous Integration (Sürekli Entegrasyon):**
Kod değişikliklerinin sık sık main branch'e intgre edilmesidir. Amaç: hataların erken tespit edilmesidir.

**CD - Continuous Deployment/Delivery (Sürekli Dağıtım):**
Testleri başarıyla geçen kodun otomatik olarak production veya staging ortamlarına dağıtılmasıdır.

---

## 2. GitHub Actions Nedir?

### 2.1 Tanım
GitHub Actions, GitHub üzerinde doğrudan çalıştırılabilecek bir **CI/CD platformudur**.

### 2.2 Nasıl Çalışır?
1. Bir repo içinde `.github/workflows/` klasörü oluşturursunuz
2. Bu klasörün içine `.yml` veya `.yaml` uzantılı workflow dosyaları yazarsınız
3. Belirttiğiniz koşullar sağlandığında (push, pull request, schedule vb.) GitHub bu dosyaları okur

---

## 3. Neden GitHub Actions?

### 3.1 Avantajlar
- GitHub ile doğrudan entegre
- Actions Marketplace'te 10.000+ hazır action
- Ubuntu, Windows, macOS desteği
- Public repos için sınırsız bedava

---

## 4. Temel Kavramlar

```
Repository
  ↳ Workflow (.yml dosyası)
    ↳ Job (workflow'daki bir iş birimi)
      ↳ Step (job içindeki adımlar)
        ↳ Run / Uses (her step'in komutu)
```

---

## 5. Workflow Dosyası Yapısı

Bir workflow dosyası YAML formatındadır ve şu temel bölümlerden oluşur:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"

jobs:
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
```

### 5.1 Context Syntax: `${{ }}`

| Context | Açıklama |
|---------|----------|
| `github` | Event bilgileri |
| `env` | Environment variables |
| `secrets` | Gizli değişenler |
| `steps` | Önceki step sonuçları |
| `needs` | Önceki job sonuçları |
| `matrix` | Matrix değişenleri |
| `inputs` | Manual trigger inputları |

---

## 6. Trigger'lar (Tetikleyiciler)

### 6.1 push
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!src/test*'
```

### 6.2 pull_request
```yaml
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```

### 6.3 schedule
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Her gün 02:00 UTC
```

### 6.4 workflow_dispatch
```yaml
on:
  workflow_dispatch:  # Manuel tetikleme
```

### 6.5 workflow_call (Reusable Workflow)
```yaml
# Reusable workflow:
on:
  workflow_call:
    inputs:
      env:
        required: true
        type: string

# Çağırma:
jobs:
  call-deploy:
    uses: ./.github/workflows/reusable.yml
    with:
      env: production
```

---

## 7. Hazır Actions

| Action | Kullanım |
|--------|----------|
| `actions/checkout@v4` | Kodu clone etme |
| `actions/setup-python@v5` | Python kurma |
| `actions/cache@v4` | Cache yönetimi |
| `actions/upload-artifact@v4` | Artifacts yükleme |
| `docker/build-push-action@v5` | Docker build+push |

---

## 8. Kendi Action'ınızı Yazma

3 farklı şekilde yazabilirsiniz:
- **Docker-Tabanl1**: Docker container içinde çalışır
- **JavaScript-Tabanl1**: Node.js ile yazılır (en yayın)
- **Composite Action**: Birden fazla step'i paketleme

---

## 9. Environment Variables ve Secrets

**Secrets:** GitHub'da güvenle saklanan hassas bilgilerdir.
- Repo → Settings → Secrets and variables → Actions
- `${{ secrets.HF_TOKEN }}` ile erişilir

---

## 10. Cache ve Artifact'lar

**Cache:** `actions/cache@v4` ile bağımlılıkları cacheleyin.

**Artifact'lar:** `actions/upload-artifact@v4` ile build çıktılarını saklayın.

---

## 11. Matrix Builds

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.9', '3.11']
```

---

## 12. Practical Örnekler

### CI Pipeline
```yaml
name: CI
on: pull_request
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff && ruff check .
```

### Docker Build
```yaml
name: Docker CI
on: push:
  tags: ['v*']
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: myuser/myapp:latest
```

---

## 13. En İyi Uygulamalar

1. Cache kullanın
2. Path filter kullanın
3. Versiyonlu action kullanın
4. Secrets kullanın
5. Concurrency kullanın
6. Minimal izin kullanın
7. Step isimleri verin
8. Reusable workflow kullanın

---

## 14. Sık Karşılaşılan Hatalar

| Hata | Çözüm |
|------|--------|
| Permission denied | `GITHUB_TOKEN` kullanın |
| Action not found | Action adını kontrol edin |
| Cache çalışmıyor | key'i kontrol edin |
| Timeout | `timeout-minutes` artırın |

---

## 15. Sıfırdan Proje: Gradio → HuggingFace Spaces

Ayrıntılı bilgi için **[Gradio HF Spaces Deploy Dokümanı](./gradio-hf-deploy-doc.md)** bakınız.

---

## Ek Kaynaklar

| Kaynak | Link |
|--------|------|
| GitHub Actions Docs | https://docs.github.com/en/actions |
| Actions Marketplace | https://github.com/marketplace?type=actions |

---

**Son Düzenleme:** 6 Temmuz 2026
