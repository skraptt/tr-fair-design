export function UyeOl() {
  return (
    <form>
      <input name="email" type="email" required />
      <select name="cinsiyet">
        <option value="">Belirtmek istemiyorum</option>
        <option>Kadın</option>
        <option>Erkek</option>
      </select>

      <p>
        Kişisel verilerinizin nasıl işlendiğini <a href="/kvkk">KVKK Aydınlatma Metni</a>'nde bulabilirsiniz.
      </p>

      <label>
        <input type="checkbox" required />
        <a href="/kosullar">Kullanım koşullarını</a> kabul ediyorum.
      </label>

      <fieldset>
        <legend>İsteğe bağlı</legend>
        <label>
          <input type="checkbox" />
          Kampanyalar hakkında e-posta almak istiyorum.
        </label>
      </fieldset>
      <button type="submit">Üye ol</button>
      <a href="/misafir">Üye olmadan devam et</a>
    </form>
  );
}
