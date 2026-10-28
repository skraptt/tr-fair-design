# TR Fair Design

**Kodunuz için KVKK ve karanlık tasarım denetleyicisi.** Yapay zekâ kodlama
ajanlarına (Claude Code ve benzerleri) eklenen açık kaynak bir skill. Projenizin
kodunu *yayına çıkmadan önce* okur; önceden işaretli onay kutularını, "Reddet"
seçeneği olmayan çerez bildirimlerini, hizmet şartına bağlanmış açık rızaları,
sahte geri sayımları, iptal edilemeyen abonelikleri bulur. Her bulguyu
dosya:satır kanıtıyla ve ilgili Türk mevzuatı hükmüyle birlikte, nasıl
düzeltileceğini de yazarak raporlar.

> ⚠️ **Hukuki görüş değildir.** Bu araç, bir hukukçunun incelemesi için taslak
> ve aday bulgular üretir. Bir ürünün hukuka uygun olup olmadığına karar vermez.
> Proje sahipleri, araç çıktısına dayanılarak verilen kararlardan sorumluluk
> kabul etmez.

## Neleri kapsar (v0.1)

| Alan | Başlıca kaynaklar |
|---|---|
| Aydınlatma, açık rıza, çerezler | KVKK m.3, 4, 5, 10; KVK Kurulu İlke Kararı 2026/347; KVKK Çerez Rehberi (2025) |
| Yurt dışına veri aktarımı | KVKK m.9 (7499 sayılı Kanunla değişik), Aktarım Yönetmeliği (2024) |
| Karanlık tasarımlar, aldatıcı uygulamalar, tüketici yorumları | TKHK m.62–63; Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği (Ek A-22, m.14, 28/B, 29–31); Reklam Kurulu kararları |
| İnternetten satış, ek ödemeler, sipariş butonu | Mesafeli Sözleşmeler Yönetmeliği m.5, 6, 8, 19 |
| Abonelik iptali | TKHK m.52 |
| SMS/e-posta pazarlama onayı | 6563 sayılı Kanun; Ticari İletişim ve Ticari Elektronik İletiler Hakkında Yönetmelik; İYS |

23 kalıbın tam listesi ve dayanakları: [`references/kaliplar.md`](references/kaliplar.md)

AB'deki kullanıcılara da hizmet veriyorsanız AB kuralları (GDPR, DSA, AI Act)
için kardeş projeyi kullanın: [eu-fair-design](https://github.com/skraptt/eu-fair-design).

## Kurulum

Claude Code (ve Markdown skill yükleyen diğer ortamlar) için:

```bash
git clone https://github.com/skraptt/tr-fair-design ~/.claude/skills/tr-fair-design
```

Sonra projenizin klasöründe Claude Code'a şunu yazın:

> Bu projede KVKK ve karanlık tasarım incelemesi yap.

Tarayıcı tek başına da çalışır:

```bash
python3 ~/.claude/skills/tr-fair-design/scripts/scan.py . --format md
```

## Nasıl çalışır?

1. **Uygulanabilirlik:** Hangi kuralların geçerli olduğu ürüne bağlıdır
   (tüketiciye mi satıyorsunuz, abonelik var mı, veriler yurt dışına gidiyor
   mu?). Ajan önce bunları sorar.
2. **Tarama:** `scripts/scan.py` (yalnızca Python standart kütüphanesi), düzenli
   ifadelerle *aday* bulgular işaretler.
3. **İnceleme:** Ajan her adayı bağlamında okur (süre gerçek mi, stok sayısı
   rastgele mi?) ve üyelik, ödeme, çerez ve iptal akışlarını gezer.
4. **Rapor:** `fair-design-review/rapor.md`: bulgular, kanıtlar, dayanaklar ve
   düzeltmeler.

## Hukukçular için: kendi kurallarınızı ekleyin

Kod yazmanız gerekmez. Büronuzun ya da müvekkilinizin görüşlerini, incelenen
projede `.fair-design/kurallar.md` dosyasına yazın ya da buradaki
`references/kaliplar.md` dosyasını bir pull request ile geliştirin. Ajan, proje
kurallarını varsayılan kurallardan önce uygular.

## Katkı

Yeni bir kalıp önerisinde şunlar bulunmalı: kısa bir açıklama, kodda nasıl
göründüğü, en az bir hukuki dayanak (mevzuat, madde, fıkra; varsa Reklam Kurulu
ya da KVK Kurulu kararı) ve uygun bir alternatif.

## English

A KVKK and dark pattern linter for the Turkish market: an agent skill that
reviews your codebase before release and maps each finding to Turkish law (the
Personal Data Protection Law KVKK, the Consumer Protection Law, the Regulation
on Commercial Advertising and Unfair Commercial Practices, the Distance
Contracts Regulation, and e-commerce messaging rules). Documentation is in
Turkish. Not legal advice. For EU law, see
[eu-fair-design](https://github.com/skraptt/eu-fair-design).

## Lisans

Apache-2.0
