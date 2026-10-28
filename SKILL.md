---
name: tr-fair-design
description: Bir web sitesi veya uygulamanın kodunu yayına çıkmadan önce karanlık tasarımlar (dark pattern) ve KVKK açısından inceler; her bulguyu Türk hukukuna (KVKK, TKHK, Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği, Mesafeli Sözleşmeler Yönetmeliği, 6563 / İYS) bağlar. Use for a KVKK review, Turkish dark pattern audit, çerez bildirimi, açık rıza / aydınlatma metni, İYS onayı, yurt dışına aktarım, checkout or cancellation flow review for the Turkish market.
license: Apache-2.0
metadata:
  version: "0.1.1"
  domain: turk-tuketici-ve-veri-koruma-hukuku
  tags: "kvkk, karanlik-tasarim, dark-patterns, reklam-kurulu, trhtuy, mesafeli-sozlesmeler, iys, cerez"
---

# TR Fair Design: kod için KVKK ve karanlık tasarım incelemesi

Bu skill, bir projenin **kendi kaynak kodunu** Türk hukukunun kısıtladığı arayüz
kalıpları ve kişisel veri uygulamaları açısından inceler. Geliştiricinin
uygulayabileceği, hukukçunun da kontrol edebileceği bir rapor üretir.

> **Hukuki görüş değildir.** Her çıktı, bir hukukçunun incelemesi için hazırlanmış
> bir taslaktır. Kullanıcıya hiçbir zaman ürününün "uyumlu" veya "hukuka aykırı"
> olduğunu söyleme. Kodun ne gösterdiğini, bunun hangi kuralla ilgili
> olabileceğini ve bir hukukçunun neyi teyit etmesi gerektiğini yaz.

Kullanıcıyla onun dilinde konuş. Kullanıcı Türkçe yazıyorsa raporu Türkçe yaz.

## İş akışı

Aşamaları sırayla uygula. Aşama 1'i atlama: bazı kurallar yalnızca belirli
işletmelere ve işlemlere uygulanır, yanlış kurala dayanan bir bulgu yalnızca
gürültüdür.

### Aşama 1: Uygulanabilirlik (sor, tahmin etme)

`references/uygulanabilirlik.md` dosyasını oku. Sonra kullanıcıya sor ya da
projenin README'sinden ve sitedeki metinlerden çıkar, çıkardıklarını varsayım
olarak belirt:

1. Ürün tüketicilere mi sunuluyor?
2. Kişisel veri işleniyor mu, çerez veya benzeri teknoloji kullanılıyor mu?
3. Veriler yurt dışındaki servislere gidiyor mu? Hangileri?
4. İnternetten satış yapılıyor ya da sözleşme kuruluyor mu?
5. Abonelik veya üyelik var mı?
6. SMS, e-posta veya bildirimle pazarlama yapılıyor mu?
7. Yapay zekâ kullanıcıyla etkileşiyor mu?
8. AB'deki kullanıcılara da hizmet veriliyor mu? (Evet ise AB kuralları için
   `eu-fair-design` skill'inin de kullanılmasını öner.)

Cevapları raporun en başına yaz.

### Aşama 2: Otomatik aday taraması

Tarayıcıyı skill klasöründen, projenin kök dizinine karşı çalıştır:

```bash
python3 scripts/scan.py <proje_kökü> --out fair-design-review/adaylar.json
```

Tarayıcı yalnızca Python standart kütüphanesini kullanır ve bir özet yazdırır.
Ürettiği şeyler **bulgu değil, adaydır**: JSX/TSX/Vue/Svelte/HTML/şablon
dosyaları ve çeviri JSON'ları üzerinde çalışan düzenli ifade kurallarıdır. Yanlış
alarm ve kaçırılan durumlar beklenir. Test, e2e ve Storybook dosyaları varsayılan
olarak atlanır.

### Aşama 3: Bağlam içinde inceleme (asıl iş)

Her aday için dosyayı aç, bileşeni ve verinin nereden geldiğini oku. Her birine
şu kararlardan birini ver: **doğrulandı**, **çalışma anında kontrol gerekir** ya
da **elendi** (tek satırlık gerekçeyle). Tipik sorular:

- Geri sayım ve aciliyet: Süre gerçek mi (sunucudan veya ayardan geliyor mu),
  yoksa sayfa yenilenince sıfırlanıyor mu?
- Kıtlık ve sosyal kanıt: Sayı stoktan veya gerçek veriden mi geliyor, yoksa
  `Math.random()` ya da sabit bir değer mi?
- Önceden işaretli kutular: Kutu bir ücret mi, bir ticari ileti onayı mı, bir
  açık rıza mı ekliyor?
- Onay kutuları: Hizmet için gerçekten gerekli mi, yoksa zorunlu tutulan bir
  pazarlama veya açık rıza onayı mı? Aydınlatma ile açık rıza tek kutuda mı?
- Yurt dışına aktarım: Servise kişisel veri gidiyor mu, yoksa yalnızca anonim
  veri mi?
- İptal: Abone olmak kaç adım, iptal etmek kaç adım? İnternetten iptal yolu var
  mı?

Ardından düzenli ifadelerin göremeyeceği şeyler için `references/kaliplar.md`
dosyasını kontrol listesi olarak kullan: üyelik, sepet, ödeme, çerez, hesap
ayarları ve iptal akışlarını rotaları ve bileşenleri okuyarak gez.

### Aşama 4: Hukuki eşleştirme

Doğrulanan her bulgu için hukuki dayanağı `references/kaliplar.md` dosyasından
al. Yalnızca Aşama 1'den sonra uygulanabilir olan hükümleri yaz. Madde numarası
uydurma; emin değilsen "dayanak hukukçu tarafından teyit edilmeli" yaz.

### Aşama 5: Rapor

`references/rapor-sablonu.md` şablonuyla `fair-design-review/rapor.md`
dosyasını yaz: uygulanabilirlik cevapları, bulgu tablosu (no, kalıp, dosya:satır
kanıtı, dayanak, risk, düzeltme), riske göre sıralanmış düzeltme listesi ve
uyarı notu. Her bulgu **dosya:satır kanıtı** taşımalı. Kullanıcı isterse
düzeltmeleri koda da uygula.

## Davranış kuralları

- Önce kanıt: dosya ve satır olmadan bulgu olmaz.
- "Kod şunu yapıyor" (olgu) ile "bu, şu kurala aykırı olabilir" (hukuki
  değerlendirme) ayrımını koru.
- Kullanıcılara gerçek ve eşit bir seçim sunan düzeltmeleri, görüntüyü
  değiştiren kozmetik düzeltmelere tercih et.
- Mevzuat değişir. Raporu yazarken bir kuralın güncelliğinden şüphe ediyorsan
  bunu belirt; para cezası tutarlarını yazma, çünkü her yıl yeniden değerlenir.
- Projede hukukçunun yazdığı `.fair-design/kurallar.md` dosyası varsa oku; bu
  dosyadaki kurallar skill'in varsayılanlarından önce gelir.
