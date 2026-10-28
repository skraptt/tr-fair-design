// Hatalı örneğin adil karşılığı: tarayıcı burada sessiz kalmalı.
import { useState } from "react";

type Props = { toplam: number; son10GunEnDusuk: number | null; stok: number; kampanyaBitis: string | null };

export function Odeme({ toplam, son10GunEnDusuk, stok, kampanyaBitis }: Props) {
  const [sigorta, setSigorta] = useState(false);
  const [smsOnayi, setSmsOnayi] = useState(false);

  return (
    <div className="odeme">
      {kampanyaBitis && <p>İndirimli fiyat {new Date(kampanyaBitis).toLocaleDateString("tr-TR")} tarihine kadar geçerli</p>}
      {son10GunEnDusuk !== null && <p>Son 10 günün en düşük fiyatı: {son10GunEnDusuk} TL</p>}
      <p>Tüm vergiler ve masraflar dahil toplam: {toplam} TL</p>
      <p>{stok > 0 ? "Stokta var" : "Stokta yok"}</p>
      <label>
        <input type="checkbox" checked={sigorta} onChange={(e) => setSigorta(e.target.checked)} />
        Seyahat sigortası ekle (+49,90 TL)
      </label>
      <label>
        <input type="checkbox" checked={smsOnayi} onChange={(e) => setSmsOnayi(e.target.checked)} />
        Kampanyalardan SMS ile haberdar olmak istiyorum (isteğe bağlı)
      </label>
      <p>"Siparişi onayla ve öde" butonuna bastığınızda ödeme yükümlülüğü altına girersiniz.</p>
      <button onClick={siparisVer}>Siparişi onayla ve öde</button>
    </div>
  );
}

function siparisVer() {}
