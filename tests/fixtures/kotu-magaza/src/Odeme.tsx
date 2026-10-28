// Test için bilerek hatalı yazılmış örnek. Kopyalamayın.
import { useState } from "react";

export function Odeme({ fiyat }: { fiyat: number }) {
  const [sigorta, setSigorta] = useState(true);
  const [bitis] = useState(Date.now() + 15 * 60 * 1000); // indirim sayacı her yenilemede baştan başlar
  const [bakan] = useState(Math.floor(Math.random() * 40) + 5);
  const eskiFiyat = fiyat * 2;

  return (
    <div className="odeme">
      <p>Kampanya bitiyor! Kalan süre: {Math.max(0, bitis - Date.now())} ms</p>
      <p>Stokta son {bakan % 4 + 1} ürün</p>
      <p>{bakan} kişi şu anda bu ürünü inceliyor</p>
      <span className="rozet">En popüler</span>
      <p>
        <s>{eskiFiyat} TL</s> {fiyat} TL
      </p>
      <label>
        <input type="checkbox" defaultChecked /> Seyahat sigortası ekle (+49,90 TL)
      </label>
      <label>
        <input type="checkbox" defaultChecked /> Kampanyalardan SMS ve e-posta ile haberdar olmak istiyorum
      </label>
      <p>Hizmet bedeli: 29,90 TL (ödeme adımında eklenir)</p>
      <button className="birincil" onClick={siparisVer}>Devam</button>
      <a className="kucuk-gri" href="/">Hayır, indirim istemiyorum</a>
    </div>
  );
}

function siparisVer() {}
