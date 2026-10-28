# Kalıp kataloğu

Her kalıpta şunlar var: ne olduğu, kodda nasıl göründüğü, hukuki dayanak (önce
birincil, sonra ikincil), risk düzeyi ve uygun alternatif. `Tarayıcı kuralı`,
`scripts/scan.py` içinde aday üreten kuralın adıdır. "elle" yazıyorsa o kalıp
yalnızca akış incelemesiyle bulunur.

## Kısaltmalar

| Kısaltma | Kaynak |
|---|---|
| **KVKK** | 6698 sayılı Kişisel Verilerin Korunması Kanunu (7499 sayılı Kanunla değişik m.9 dahil; değişiklik yürürlüğü 1.6.2024) |
| **İlke-2026/347** | KVK Kurulunun 18.02.2026 tarihli ve 2026/347 sayılı İlke Kararı: açık rıza ve aydınlatma metinlerinin ayrı düzenlenmesi (RG 24.03.2026, 33203) |
| **Çerez Rehberi** | KVKK Çerez Uygulamaları Hakkında Rehber (KVKK Yayınları No: 69, Temmuz 2025) |
| **Aktarım Yön.** | Kişisel Verilerin Yurt Dışına Aktarılmasına İlişkin Usul ve Esaslar Hakkında Yönetmelik (RG 10.07.2024) |
| **TKHK** | 6502 sayılı Tüketicinin Korunması Hakkında Kanun |
| **TRHTUY** | Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği. Karanlık tasarım hükmü (Ek, A-Aldatıcı Ticari Uygulamalar, bent 22) ile m.28/B, RG 01.02.2022 tarihli ve 31737 sayılı değişiklikle eklendi, 01.03.2022'de yürürlüğe girdi. |
| **MSY** | Mesafeli Sözleşmeler Yönetmeliği (RG 27.11.2014) |
| **6563** | 6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun |
| **TİY** | Ticari İletişim ve Ticari Elektronik İletiler Hakkında Yönetmelik |
| **RK-2024** | Ticaret Bakanlığı, Reklam Kurulu 2024 Yılı Raporu (Ankara, 2025). Sayfa numaraları rapora göre verilmiştir. |

## Risk ölçeği

- **Yüksek:** Açık bir hüküm (ör. önceden seçili onay yasağı) ya da Reklam Kurulunun yaptırım uyguladığı somut bir örnek var.
- **Orta:** Bağlama göre aykırılık olasılığı yüksek.
- **Düşük:** Düzeltilmesi önerilen tasarım riski.

> **Genel kural.** TRHTUY Ek A-22, internet ortamında yönlendirici arayüz
> tasarımları, seçenekler ya da ifadeler yoluyla tüketicinin karar verme veya
> seçim yapma iradesini olumsuz etkileyen uygulamaları haksız ticari uygulama
> sayar. Aşağıdaki kalıpların birçoğu ayrıca bu genel hükme de dayanır. Haksız
> ticari uygulama yasağının kanuni dayanağı TKHK m.62'dir; denetim ve
> yaptırım yetkisi Reklam Kurulundadır (TKHK m.63).

---

## TR-01 Ek ücretli, önceden işaretli seçenek
- **Kodda:** Sigorta, bağış, hızlı kargo, ek hizmet gibi ücretli bir kalemin yanında `checked` / `defaultChecked` / `useState(true)` kullanılması.
- **Dayanak:** MSY m.19/1: temel ücret dışındaki her ödeme için tüketicinin açık onayı sözleşme kurulmadan ayrıca alınmalıdır. MSY m.19/2: kendiliğinden seçili sunulan bir seçenek nedeniyle ödeme yapılmışsa iade gerekir. Ayrıca TRHTUY Ek A-22. Reklam Kurulu, önceden seçili paket ve ek hizmetleri karanlık tasarım saymıştır (RK-2024 s.13–14).
- **Risk:** Yüksek.
- **Düzeltme:** Ücretli seçenekler varsayılan olarak boş olmalı ve yalnızca kullanıcı tıklayınca eklenmeli.
- **Tarayıcı kuralı:** `prechecked-checkbox`

## TR-02 Önceden işaretli ticari elektronik ileti onayı
- **Kodda:** "Kampanyalardan haberdar olmak istiyorum", "SMS/e-posta ile bilgilendirme" gibi kutuların varsayılan olarak işaretli gelmesi.
- **Dayanak:** TİY m.7/8: olumlu irade beyanı önceden seçilmiş olarak yer alamaz. 6563 m.6 (önceden onay). Kişisel veri işleme de söz konusuysa KVKK m.3/1(a) (açık rıza: özgür iradeyle açıklanan rıza).
- **Risk:** Yüksek.
- **Düzeltme:** Kutu boş gelmeli. Onay alındıktan sonra İYS'ye kaydedilmeli (TİY m.5).
- **Tarayıcı kuralı:** `prechecked-checkbox`, `consent-default-granted`

## TR-03 Onayın hizmet şartına bağlanması
- **Kodda:** Ticari ileti, açık rıza, hedefli reklam ya da profilleme kutusunun `required` olması ya da işaretlenmeden "Üye ol" / "Devam" butonunun etkin olmaması.
- **Dayanak:** TİY m.7/9: ticari ileti onayı mal veya hizmet sunumu için ön şart olarak ileri sürülemez. KVKK m.3/1(a): rıza özgür iradeyle verilmelidir; hizmet şartına bağlanan rıza özgür sayılmaz. Reklam Kurulu, hedefli reklam, kişisel veri ve ticari ileti onaylarının üyelik için zorunlu tutulmasını karanlık tasarım saymıştır (RK-2024 s.16–18).
- **Risk:** Yüksek.
- **Düzeltme:** Hizmet için gerçekten gerekli olmayan onayları isteğe bağlı yap. Hizmet bu onaylar olmadan da sunulmalı.
- **Tarayıcı kuralı:** `required-consent`

## TR-04 Aydınlatma ile açık rızanın birleştirilmesi
- **Kodda:** Tek bir kutu ile hem aydınlatma metninin hem açık rızanın kabul edilmesi ("KVKK Aydınlatma Metnini okudum ve kişisel verilerimin işlenmesine onay veriyorum"); aydınlatma metni için "onaylıyorum / kabul ediyorum" kutusu.
- **Dayanak:** İlke-2026/347: aydınlatma ve açık rıza metinleri ayrı ayrı düzenlenmeli; aynı sayfada yer alıyorlarsa birbirinden açıkça ayrılmalı ve ayrı beyanlar içermelidir. Aydınlatma metni için kişiden onay istenmemeli; açık rıza gerekmeyen işlemlerde açık rıza alınmamalıdır. KVKK m.10 (aydınlatma yükümlülüğü).
- **Risk:** Yüksek.
- **Düzeltme:** Aydınlatma metnini bilgilendirme olarak bağlantıyla sun, onay kutusu koyma. Açık rıza gerekiyorsa ayrı, isteğe bağlı, boş bir kutu kullan.
- **Tarayıcı kuralı:** `combined-notice-consent`

## TR-05 Eşit "Reddet" seçeneği olmayan çerez bildirimi
- **Kodda:** Büyük bir "Kabul et" butonuna karşılık reddetmenin yalnızca "Ayarlar" içinde ya da küçük bir bağlantı olarak sunulması.
- **Dayanak:** Çerez Rehberi: "Kabul et", "Reddet" ve "Tercihler" butonlarının renk, boyut ve yazı tipi bakımından eşit sunulması iyi uygulamadır; rıza gerektiren çerezler panelde varsayılan olarak pasif olmalıdır. KVKK m.3/1(a), m.5/1. Ayrıca TRHTUY Ek A-22.
- **Risk:** Yüksek.
- **Düzeltme:** İlk katmanda "Kabul et" ile aynı ağırlıkta bir "Reddet" butonu koy.
- **Tarayıcı kuralı:** `cookie-accept-without-reject`

## TR-06 Rızadan önce çalışan takip kodları
- **Kodda:** Google Analytics, Meta Pixel, Hotjar gibi kodların, onay alınmadan sayfa açılır açılmaz yüklenmesi.
- **Dayanak:** Çerez Rehberi: hukuki sebep açık rızaysa rıza, ilgili çerezler yerleştirilmeden önce alınmalıdır; davranışsal reklam çerezleri açık rıza gerektirir. KVKK m.5/1. Veriler yurt dışına gidiyorsa TR-21'e de bakılmalı.
- **Risk:** Yüksek.
- **Düzeltme:** Takip kodlarını yalnızca onaydan sonra yükle.
- **Tarayıcı kuralı:** `tracker-before-consent`

## TR-07 Sahte ya da sıfırlanan geri sayım
- **Kodda:** Bitiş zamanı `Date.now() + N` ile hesaplanan, sayfa yenilenince baştan başlayan sayaçlar.
- **Dayanak:** TRHTUY Ek A-22; TKHK m.62. Gerçek olmayan bir süre sınırı, aldatıcı eylem olarak da değerlendirilebilir (TRHTUY m.29).
- **Risk:** Yüksek (süre gerçek değilse).
- **Düzeltme:** Sayaç yalnızca sunucuda tanımlı ve gerçekten sona eren bir süre için gösterilmeli.
- **Tarayıcı kuralı:** `countdown-timer`, `urgency-text`

## TR-08 Sahte kıtlık
- **Kodda:** "Son 3 ürün", "Tükenmek üzere" gibi ifadelerin `Math.random()` ile ya da sabit bir sayıyla üretilmesi.
- **Dayanak:** TRHTUY m.29 (aldatıcı eylemler), Ek A-22; TKHK m.62.
- **Risk:** Yüksek (gerçek stok verisine dayanmıyorsa).
- **Düzeltme:** Gerçek stok verisini kullan ya da ifadeyi kaldır.
- **Tarayıcı kuralı:** `scarcity-message`, `random-number-in-ui`

## TR-09 Sahte etkinlik bildirimleri
- **Kodda:** "Şu an 23 kişi bakıyor", "Ayşe az önce satın aldı" gibi rastgele ya da sabit listeden üretilen bildirimler.
- **Dayanak:** TRHTUY m.29, Ek A-22; TKHK m.62.
- **Risk:** Yüksek.
- **Düzeltme:** Yalnızca gerçek ve güncel veriyi göster.
- **Tarayıcı kuralı:** `social-proof-message`, `random-number-in-ui`

## TR-10 Sahte ya da yönlendirilmiş tüketici değerlendirmeleri
- **Kodda:** Koda gömülü sabit yorumlar; ürünü satın almamış kullanıcıların yorum yapabilmesi; yalnızca yüksek puanların gösterilmesi.
- **Dayanak:** TRHTUY m.28/B/1: değerlendirmeyi yalnızca ürünü veya hizmeti satın alanlar yapabilir. m.28/B/3: değerlendirmeler en az bir yıl boyunca yönlendirme yapılmadan, objektif bir ölçüte göre yayınlanır. m.28/B/6: satışı artırmak amacıyla doğru olmayan değerlendirme yapılamaz. Reklam Kurulu bu tür uygulamalara yaptırım uygulamıştır (RK-2024 s.19–20).
- **Risk:** Yüksek.
- **Düzeltme:** Yorum yapmayı satın alma kaydına bağla, sıralama ölçütünü açıkla.
- **Tarayıcı kuralı:** `hardcoded-reviews` + elle

## TR-11 Ölçütü belirsiz "En popüler" etiketi
- **Kodda:** Bir paketin ya da ürünün yanında sabit olarak "En popüler", "En çok tercih edilen", "Önerilen" etiketi.
- **Dayanak:** Reklam Kurulu, şeffaf bir ölçüt olmadan kullanılan "En Popüler" / "En çok tercih edilen" ibarelerini karanlık tasarım saymıştır (RK-2024 s.13–14, 18). TRHTUY Ek A-22. Sıralama içeren platformlarda ayrıca TRHTUY m.28/A.
- **Risk:** Orta.
- **Düzeltme:** Etiketi gerçek satış verisine dayandır ve ölçütü açıkla ya da kaldır.
- **Tarayıcı kuralı:** `popularity-badge`

## TR-12 Utandırarak reddettirme
- **Kodda:** "Hayır, indirim istemiyorum", "Tam fiyat ödemeyi tercih ederim" gibi reddetme ifadeleri.
- **Dayanak:** TRHTUY Ek A-22 (yönlendirici ifadeler); ağır durumlarda TRHTUY m.31 (saldırgan ticari uygulamalar).
- **Risk:** Orta.
- **Düzeltme:** İki seçenek için de nötr ifade kullan ("Evet" / "Hayır").
- **Tarayıcı kuralı:** `confirmshaming-text`

## TR-13 Reddetmenin gizlenmesi ya da zorlaştırılması
- **Kodda:** Kabul büyük ve renkli bir buton, reddetme ise köşede küçük bir "X" ya da gri ve küçük bir bağlantı.
- **Dayanak:** Reklam Kurulu, "Kabul Et"in öne çıkarılıp reddetmenin küçük bir "X" ile sunulmasını karanlık tasarım saymıştır; "X" işareti reddetme olarak yorumlanamaz (RK-2024 s.14–15). TRHTUY Ek A-22.
- **Risk:** Orta–Yüksek.
- **Düzeltme:** Açıkça "Hayır, teşekkürler" ya da "Reddet" yazan, kabul butonuyla eşit ağırlıkta bir seçenek koy.
- **Tarayıcı kuralı:** elle (çerez bildirimleri için `cookie-accept-without-reject`)

## TR-14 Üye olmadan devam etmenin gizlenmesi
- **Kodda:** Satın alma sırasında "Üye olmadan devam et" seçeneğinin hiç olmaması, küçük puntoyla ya da silik renkte sunulması; "Üyeliğimi otomatik oluştur" kutusunun işaretli gelmesi.
- **Dayanak:** RK-2024 s.16–18 (öne çıkarma ve önceden seçili üyelik örnekleri); satın alma için üyeliğin zorunlu tutulup üyelik metnine profilleme ve reklam amaçlı veri kullanımının konması da karanlık tasarım sayılmıştır (RK-2024 s.18). TRHTUY Ek A-22; KVKK m.4/2(ç).
- **Risk:** Orta.
- **Düzeltme:** Misafir olarak satın alma seçeneğini üye olma seçeneğiyle eşit görünürlükte sun.
- **Tarayıcı kuralı:** elle (`prechecked-checkbox` otomatik üyelik kutusunu yakalayabilir)

## TR-15 Gereksiz zorunlu bilgi
- **Kodda:** Üyelik veya sipariş formunda cinsiyet, doğum tarihi, T.C. kimlik numarası gibi hizmet için gerekli olmayan alanların `required` olması.
- **Dayanak:** KVKK m.4/2(ç): veriler işlendikleri amaçla bağlantılı, sınırlı ve ölçülü olmalıdır. Reklam Kurulu, cinsiyet bilgisinin zorunlu istenmesini karanlık tasarım örnekleri arasında saymıştır (RK-2024 s.16–18).
- **Risk:** Orta.
- **Düzeltme:** Alanı isteğe bağlı yap ya da kaldır. Yasal olarak gerekiyorsa (ör. fatura için T.C. kimlik no) nedenini belirt.
- **Tarayıcı kuralı:** `required-sensitive-field`

## TR-16 Ücretsiz deneme tuzağı
- **Kodda:** "Ücretsiz dene" çağrısının yanında kart bilgisinin zorunlu istenmesi, deneme bitince ücretli aboneliğe otomatik geçiş ve bunun çağrının yanında açıkça yazılmaması.
- **Dayanak:** Reklam Kurulu, deneme için kart bilgisinin istenip süre sonunda otomatik abonelik başlatılmasını karanlık tasarım saymıştır (RK-2024 s.13). TRHTUY Ek A-22, m.30 (aldatıcı ihmaller).
- **Risk:** Orta–Yüksek.
- **Düzeltme:** Deneme sonrası fiyatı, tarihi ve iptal yolunu çağrının hemen yanında yaz. Mümkünse deneme bitmeden önce hatırlatma gönder.
- **Tarayıcı kuralı:** `free-trial-text`

## TR-17 Zor iptal
- **Kodda:** İnternetten abone olunabilen ama internetten iptal edilemeyen hizmetler; iptalin yalnızca telefonla ya da dilekçeyle yapılabilmesi; abonelikten çok daha fazla adım gerektiren iptal akışı.
- **Dayanak:** TKHK m.52: satıcı ya da sağlayıcı fesih için sözleşmenin kurulmasından daha zor bir yöntem öngöremez ve fesih için uygun bir sistemi kurup açık tutmakla yükümlüdür. Reklam Kurulu, üyelikten çıkışın gizlenmesini ya da daha ağır koşullara bağlanmasını karanlık tasarım saymıştır (RK-2024 s.16–18).
- **Risk:** Yüksek.
- **Düzeltme:** Hesap ayarlarından erişilebilen, abone olmaktan daha zor olmayan bir çevrim içi iptal yolu sun.
- **Tarayıcı kuralı:** `cancellation-missing` + elle

## TR-18 Gizli maliyet
- **Kodda:** Hizmet bedeli, işlem ücreti, kargo gibi masrafların yalnızca son ödeme adımında eklenmesi.
- **Dayanak:** MSY m.5/1(d): ön bilgilendirmede tüm vergiler dahil toplam fiyat ve varsa tüm ek masraflar belirtilmelidir. MSY m.6/2(a): internet satışında bu bilgiler ödeme yükümlülüğünden hemen önce açıkça gösterilmelidir. Ek masraflar bildirilmezse tüketici bunları ödemekle yükümlü değildir. TRHTUY m.30.
- **Risk:** Yüksek.
- **Düzeltme:** Kaçınılmaz bütün masrafları ilk fiyat gösteriminden itibaren toplam fiyata dahil et.
- **Tarayıcı kuralı:** `late-fee` + elle

## TR-19 Ödeme yükümlülüğünü belirtmeyen sipariş butonu
- **Kodda:** Ödeme yükümlülüğü doğuran son butonun "Devam", "İleri", "Tamamla", "Onayla" gibi genel bir ifade taşıması ve yanında bir açıklama bulunmaması.
- **Dayanak:** MSY m.8/1: siparişin onaylanmasından önce tüketiciye, verilen siparişin ödeme yükümlülüğü anlamına geldiği açık ve anlaşılır şekilde bildirilmelidir; bildirilmezse tüketici siparişle bağlı değildir.
- **Risk:** Yüksek.
- **Düzeltme:** "Siparişi onayla ve öde" gibi ödeme yükümlülüğünü açıkça belirten bir ifade kullan ve yanında bunu açıkla.
- **Tarayıcı kuralı:** `order-button-wording`

## TR-20 Sahte indirim / gerçek olmayan "önceki fiyat"
- **Kodda:** Üstü çizili "eski fiyat"ın sabit girilmesi ya da güncel fiyatın bir katsayıyla çarpılarak hesaplanması.
- **Dayanak:** TRHTUY m.14/3: mal satışında indirimden önceki fiyat, indirimin başlangıcından önceki **on gün** içinde uygulanan en düşük fiyattır (çabuk bozulan mallar ve hizmetlerde indirimli fiyattan bir önceki fiyat). m.14/4: ispat yükü reklam verendedir. *AB'deki 30 günlük kuraldan farklıdır.*
- **Risk:** Yüksek.
- **Düzeltme:** Önceki fiyatı gerçek fiyat geçmişinden (son 10 günün en düşüğü) hesapla.
- **Tarayıcı kuralı:** `fake-reference-price`

## TR-21 Yurt dışına veri aktaran servisler
- **Kodda:** Yurt dışındaki analitik, hata izleme, yapay zekâ veya pazarlama servislerine kişisel veri gönderen SDK'lar ve API çağrıları (ör. Google Analytics, Sentry, Mixpanel, Segment, OpenAI, Anthropic, Firebase).
- **Dayanak:** KVKK m.9 (7499 sayılı Kanunla değişik, 1.6.2024'ten beri yürürlükte): sırasıyla yeterlilik kararı, uygun güvenceler (standart sözleşme, bağlayıcı şirket kuralları, taahhütname) ya da arızi aktarım halleri. Standart sözleşme imzalandıktan sonra 5 iş günü içinde Kurula bildirilmelidir (Aktarım Yön.). Açık rıza artık ana dayanak değil, yalnızca arızi aktarım hallerinden biridir.
- **Risk:** Orta (bu bir ihlal değil, belgelenmesi gereken bir aktarımdır).
- **Düzeltme:** Her servis için aktarım dayanağını belirle, standart sözleşmeyi imzala ve bildir, aydınlatma metninde alıcıları ve aktarımı açıkla. Mümkünse kişisel veriyi göndermeden önce maskele.
- **Tarayıcı kuralı:** `foreign-data-transfer`

## TR-22 Kendini gizleyen ya da manipülatif yapay zekâ
- **Kodda:** Sohbet botu talimatlarında yapay zekâ olduğunu gizleme, baskı kurma ya da iptali engelleme yönergeleri.
- **Dayanak:** Türkiye'de yapay zekâya özgü genel bir kanunun yürürlükte olup olmadığını kontrol edin. Mevcut çerçevede: TRHTUY Ek A-22, m.29 ve m.31; TKHK m.62. Yalnızca otomatik analizle kişi aleyhine sonuç doğuyorsa KVKK m.11/1(g).
- **Risk:** Orta (kırılgan grupları, ör. çocukları hedefliyorsa Yüksek).
- **Düzeltme:** Manipülatif talimatları kaldır, kullanıcıya yapay zekâyla konuştuğunu açıkça söyle.
- **Tarayıcı kuralı:** `manipulative-ai-prompt`

## TR-23 Mahremiyete aykırı varsayılan ayarlar
- **Kodda:** Profilin varsayılan olarak herkese açık olması; konum paylaşımının ya da kişiselleştirilmiş reklamın varsayılan olarak açık gelmesi.
- **Dayanak:** KVKK m.4/2 (genel ilkeler, özellikle ölçülülük). Çerez Rehberi, rıza gerektiren seçeneklerin varsayılan olarak pasif olmasını önerir.
- **Risk:** Orta.
- **Düzeltme:** Varsayılan olarak en koruyucu seçeneği kullan.
- **Tarayıcı kuralı:** `consent-default-granted` + elle

---

### Yeni kalıp eklemek
Yukarıdaki biçimi kopyala. Bir kalıp ancak en az bir dayanak (mevzuat, madde,
fıkra) ve uygun bir alternatif içeriyorsa kabul edilir. Reklam Kurulu ya da KVK
Kurulu kararı varsa tarih ve sayısıyla ekle.
