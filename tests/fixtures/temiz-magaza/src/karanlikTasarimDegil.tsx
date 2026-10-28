// Şüpheli görünen ama karanlık tasarım olmayan gerçek dünya kodları.

export function oturumTokeni(ttlSaniye: number) {
  const expiresAt = new Date(Date.now() + ttlSaniye * 1000).toISOString();
  return { expires_at: expiresAt };
}

export async function yuklemeyiBekle(timeoutMs: number) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) await new Promise((r) => setTimeout(r, 100));
}

export function Anahtar({ checked }: { checked: boolean }) {
  return <span className={checked ? "bg-mavi" : "bg-gri"} />;
}

export function MevzuatArama() {
  return (
    <form>
      <input name="q" />
      <button type="submit">{t("Ara")}</button>
    </form>
  );
}

// Kapatmak, kaydedilmemiş değişiklikleri korumak için son fırsat; yeniden dene.
export const istekNo = () => `${Date.now()}-${Math.random().toString(16).slice(2)}`;

function t(s: string) {
  return s;
}

// Hukuki süre hesabı: "son gün" burada satış baskısı değil.
export const sureMetni = (gun: string) => `Son gün ${gun}; öğleden sonra resmî tatildir.`;

export function MfaKapisi({ gateState }: { gateState: string }) {
  if (gateState === "required") return <p>İki adımlı doğrulama gerekli. Profil ayarlarınızı kontrol edin.</p>;
  return null;
}
