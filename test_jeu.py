import tempfile
import unittest
from pathlib import Path

from auth import lire_utilisateurs, register_user
from jeu import ajouter_points


class JeuTests(unittest.TestCase):
    def test_la_progression_est_enregistree(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "users.json"
            register_user("carlos", "secret123", fichier)

            score, niveau = ajouter_points("carlos", 35, fichier)
            utilisateurs = lire_utilisateurs(fichier)

            self.assertEqual(score, 35)
            self.assertEqual(niveau, 2)
            self.assertEqual(utilisateurs["carlos"]["score"], 35)
            self.assertEqual(utilisateurs["carlos"]["niveau"], 2)


if __name__ == "__main__":
    unittest.main()
