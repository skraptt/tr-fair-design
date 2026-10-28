"""Çalıştırma: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import scan  # noqa: E402

FIX = os.path.join(HERE, "fixtures")

BEKLENEN = {
    "prechecked-checkbox", "consent-default-granted", "countdown-timer", "urgency-text",
    "scarcity-message", "random-number-in-ui", "social-proof-message", "confirmshaming-text",
    "order-button-wording", "fake-reference-price", "free-trial-text", "late-fee",
    "manipulative-ai-prompt", "required-consent", "combined-notice-consent", "popularity-badge",
    "hardcoded-reviews", "required-sensitive-field", "cookie-accept-without-reject",
    "tracker-before-consent", "cancellation-missing", "foreign-data-transfer",
}


class ScanTest(unittest.TestCase):
    def test_kotu_magaza_her_kurali_tetikler(self):
        sonuc = scan.scan(os.path.join(FIX, "kotu-magaza"))
        bulunan = {c["rule"] for c in sonuc["candidates"]}
        self.assertEqual(BEKLENEN - bulunan, set(), "tetiklenmeyen kurallar")
        self.assertEqual(bulunan - BEKLENEN, set(), "beklenmeyen kurallar")

    def test_temiz_magaza_sessiz_kalir(self):
        sonuc = scan.scan(os.path.join(FIX, "temiz-magaza"))
        self.assertEqual(sonuc["candidates"], [])

    def test_her_aday_kanit_ve_tr_kalibi_tasir(self):
        for c in scan.scan(os.path.join(FIX, "kotu-magaza"))["candidates"]:
            self.assertTrue(c["file"] and c["line"] > 0)
            self.assertTrue(c["patterns"] and all(p.startswith("TR-") for p in c["patterns"]))

    def test_yurt_disi_servisleri_ayri_ayri_listelenir(self):
        sonuc = scan.scan(os.path.join(FIX, "kotu-magaza"))
        notlar = [c["note"] for c in sonuc["candidates"] if c["rule"] == "foreign-data-transfer"]
        self.assertTrue(any(n.startswith("Google Analytics") for n in notlar))
        self.assertTrue(any(n.startswith("OpenAI") for n in notlar))

    def test_katalogdaki_kaliplar_tarayicidakilerle_uyusur(self):
        katalog = open(os.path.join(HERE, "..", "references", "kaliplar.md"), encoding="utf-8").read()
        for rule in scan.LINE_RULES:
            for p in rule.patterns:
                self.assertIn(f"## {p} ", katalog, f"{rule.id} kuralı katalogda olmayan {p} kalıbına işaret ediyor")


if __name__ == "__main__":
    unittest.main()
