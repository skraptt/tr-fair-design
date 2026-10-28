// Test için bilerek hatalı yazılmış örnek. Kopyalamayın.
export function UyeOl() {
  return (
    <form>
      <input name="email" type="email" required />
      <select name="cinsiyet" required>
        <option>Kadın</option>
        <option>Erkek</option>
      </select>
      <label>
        <input type="checkbox" required />
        <a href="/kvkk">KVKK Aydınlatma Metni</a>'ni okudum ve kişisel verilerimin işlenmesine onay veriyorum.
      </label>
      <label>
        <input type="checkbox" required />
        Hedefli reklam ve kampanya amaçlı ticari ileti almayı kabul ediyorum.
      </label>
      <button type="submit">Üye ol</button>
    </form>
  );
}
