export function CerezBildirimi({ onKabul, onReddet, onTercihler }) {
  return (
    <div className="cerez-bildirimi">
      <p>Analitik çerezleri yalnızca onay verirseniz kullanırız.</p>
      <button className="secim" onClick={onReddet}>Reddet</button>
      <button className="secim" onClick={onKabul}>Kabul et</button>
      <button className="secim" onClick={onTercihler}>Tercihler</button>
    </div>
  );
}
