# Uygulanabilirlik: hangi kurallar bu projeye uygulanır?

Bulguları kurallara bağlamadan önce bu soruları netleştir. Varsayım yaptığın her
yeri rapora açıkça yaz.

## 1. Tüketiciye yönelik mi?
- **TKHK, TRHTUY ve MSY** tüketiciyle yapılan işlemlere ve tüketiciye yönelik
  ticari uygulamalara uygulanır. Yalnızca tacirlere ya da kurumlara satılan
  ürünlerde (B2B) bu kurallar büyük ölçüde devre dışı kalır; ancak kullanıcı
  bir gerçek kişiyse KVKK yine uygulanır.
- Reklam Kurulu, karanlık tasarımlara yaptırım uygulayabilir (TKHK m.63).

## 2. Kişisel veri işleniyor mu, çerez veya benzeri teknoloji kullanılıyor mu?
- Gerçek kişilere ait her türlü veri işlemede **KVKK** uygulanır.
- Çerez, yerel depolama, SDK veya parmak izi gibi teknolojiler için **KVKK Çerez
  Uygulamaları Hakkında Rehber** (Temmuz 2025) esas alınır.
- Aydınlatma ve açık rıza metinleri için **KVK Kurulunun 2026/347 sayılı İlke
  Kararı** (RG 24.03.2026) dikkate alınmalıdır.

## 3. Veriler yurt dışına gidiyor mu?
- Yurt dışındaki bir sunucuya, buluta veya hizmete (analitik, hata izleme,
  yapay zekâ sağlayıcısı, e-posta servisi) kişisel veri gidiyorsa **KVKK m.9**
  uygulanır.
- 1 Haziran 2024'ten bu yana açık rıza ana dayanak değildir. Sıra şöyledir:
  yeterlilik kararı, uygun güvenceler (çoğu durumda standart sözleşme) ve
  arızi aktarım. Standart sözleşme 5 iş günü içinde Kurula bildirilir.
- Kurulun yeterlilik kararı verip vermediğini güncel olarak kontrol et.

## 4. İnternetten sözleşme kuruluyor mu, satış yapılıyor mu?
- **MSY:** ön bilgilendirme (m.5, m.6), sipariş onayı (m.8/1), ek ödemeler
  (m.19) ve cayma hakkı (m.11).
- **TRHTUY m.14:** indirimli satış ve önceki fiyat kuralı (son 10 gün).

## 5. Abonelik ya da üyelik var mı?
- **TKHK m.52:** fesih, sözleşmenin kurulmasından daha zor bir yöntemle
  yapılmaya zorlanamaz; fesih için uygun bir sistem kurulmalıdır.
- Abonelik Sözleşmeleri Yönetmeliği ve sektörel düzenlemeler (ör. elektronik
  haberleşme) ayrıca uygulanabilir. Sektörü kullanıcıya sor.

## 6. SMS, e-posta veya bildirimle pazarlama yapılıyor mu?
- **6563 sayılı Kanun ve TİY:** önceden onay, önceden seçilmemiş onay kutusu
  (m.7/8), onayın hizmet şartına bağlanmaması (m.7/9), kolay ve ücretsiz ret
  (m.9) ve İYS kaydı (m.5).
- Alıcılar tacir veya esnafsa önceden onay gerekmez, ama ret hakkı geçerlidir
  (TİY m.6/3).

## 7. Yapay zekâ kullanıcıyla etkileşiyor mu?
- Türkiye'de yapay zekâya özgü genel bir düzenlemenin yürürlükte olup
  olmadığını kontrol et ve yürürlükte değilse bunu rapora yaz.
- Ürün AB'deki kullanıcılara da sunuluyorsa AB Yapay Zekâ Tüzüğü (AI Act) de
  uygulanabilir. Bu durumda AB kuralları için `eu-fair-design` skill'ini kullan.

## 8. AB'deki kullanıcılara da hizmet veriliyor mu?
- Evet ise GDPR, DSA ve AB tüketici hukuku da uygulanabilir. Bunları bu skill
  kapsamaz; `eu-fair-design` ile birlikte kullan.
