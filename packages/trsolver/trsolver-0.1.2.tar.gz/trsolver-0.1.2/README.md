# TrSolver Kütüphanesi

Bu kütüphane, `trsolver.com` API'si ile etkileşim kurmak için bir Python istemcisidir. (API URL'sini kontrol edin, örnek trsolver.com idi)

## Kurulum

```bash
pip install trsolver
```

## Kullanım

```python
from trsolver import TrSolverClient, SiteNotAllowedError, NoTokenAvailableError, TrSolverError

# İstemciyi başlat
client = TrSolverClient()

# Müşteri bilgilerini al
try:
    # Geçerli bir token ile değiştirin
    customer_data = client.get_customer_data(token="YOUR_CUSTOMER_TOKEN")
    print("Müşteri Bilgileri:", customer_data)
except TrSolverError as e:
    print(f"Hata (Müşteri Bilgisi): {e}")

# Site için erişim değeri al
try:
    # Geçerli token ve site ile değiştirin
    access_value = client.get_access_value(token="YOUR_ACCESS_TOKEN", site="http://example.com")
    print("Erişim Değeri:", access_value)
except SiteNotAllowedError as e:
    print(f"Hata (Site İzin Hatası): {e}")
except NoTokenAvailableError as e:
    print(f"Hata (Token Kalmadı Hatası): {e}")
except TrSolverError as e:
    print(f"Hata (Genel): {e}")

```

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen pull request açmaktan çekinmeyin.

## Lisans

MIT # Varsa lisansınızı belirtin 