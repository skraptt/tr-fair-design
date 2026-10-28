export function Hesap({ aboneligiIptalEt }: { aboneligiIptalEt: () => void }) {
  return (
    <section>
      <h2>Aboneliğiniz</h2>
      <button onClick={aboneligiIptalEt}>Aboneliği iptal et</button>
    </section>
  );
}
