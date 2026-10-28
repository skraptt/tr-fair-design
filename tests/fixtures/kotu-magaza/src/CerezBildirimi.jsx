// Test için bilerek hatalı yazılmış örnek: ilk katmanda reddetme seçeneği yok.
export function CerezBildirimi({ onKabul, onAyarlar }) {
  const tercihler = { analytics: true, marketing: true };
  return (
    <div className="cerez-bildirimi">
      <p>Deneyiminizi iyileştirmek için çerez kullanıyoruz.</p>
      <button className="buyuk" onClick={() => onKabul(tercihler)}>Tümünü kabul et</button>
      <a className="kucuk" onClick={onAyarlar}>Ayarlar</a>
    </div>
  );
}
