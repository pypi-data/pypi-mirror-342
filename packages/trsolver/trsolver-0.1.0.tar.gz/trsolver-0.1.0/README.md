**DİKKAT:** Bu paket [TestPyPI](https://test.pypi.org/project/trsolver/) deposuna yüklenmiş bir **test sürümüdür**. Gerçek kullanım için [PyPI](https://pypi.org/project/trsolver/) üzerindeki sürümü kullanın (eğer yayınlandıysa).

---

# TrSolver Kütüphanesi

Bu kütüphane, `whov.dev` API'si ile etkileşim kurmak için bir Python istemcisidir.

## Kurulum

**TestPyPI'den Kurulum:**
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple trsolver
```

**(Gerçek PyPI'den Kurulum - Yayınlandıysa):**
```bash
pip install trsolver
```

## Kullanım

```python
from trsolver import TrSolverClient

# İstemciyi başlat
client = TrSolverClient()

# Müşteri bilgilerini al
try:
    customer_data = client.get_customer_data(token="YOUR_CUSTOMER_TOKEN")
    print("Müşteri Bilgileri:", customer_data)
except Exception as e:
    print(f"Müşteri bilgisi alınırken hata: {e}")

# Site için erişim değeri al
try:
    access_value = client.get_access_value(token="YOUR_ACCESS_TOKEN", site="http://example.com")
    print("Erişim Değeri:", access_value)
except Exception as e:
    print(f"Erişim değeri alınırken hata: {e}")

```

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen pull request açmaktan çekinmeyin.

## Lisans

MIT # Varsa lisansınızı belirtin 