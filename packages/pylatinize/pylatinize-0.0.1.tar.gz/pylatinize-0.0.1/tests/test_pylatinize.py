import pytest
from pylatinize import PyLatinize, Normalization, default_mapping, emoji_mapping


class TestPylatinize:
    def test_decompose_shouldreturn_complexeol(self):
        input = "To insert this: \tPress these keys:\r\nà, è, ì, ò, ù, À, È, Ì, Ò, Ù \tCtrl+` (accent grave), the letter\r\ná, é, í, ó, ú, ý, Á, É, Í, Ó, Ú, Ý\tCtrl+' (apostrophe), the letter\r\nâ, ê, î, ô, û, Â, Ê, Î, Ô, Û\tCtrl+Shift+^ (caret), the letter\r\nã, ñ, õ, Ã, Ñ, Õ\tCtrl+Shift+~ (tilde), the letter\r\nä, ë, ï, ö, ü, ÿ, Ä, Ë, Ï, Ö, Ü, Ÿ\tCtrl+Shift+: (colon), the letter\r\nå, Å\tCtrl+Shift+@ (At), a or A\r\næ, Æ\tCtrl+Shift+& (ampersand), a or A\r\nœ, Œ\tCtrl+Shift+& (ampersand), o or O\r\nç, Ç\tCtrl+, (comma), c or C\r\nð, Ð\tCtrl+' (apostrophe), d or D\r\nø, Ø\tCtrl+/, o or O\r\n¿\tAlt+Ctrl+Shift+?\r\n¡\tAlt+Ctrl+Shift+!\r\nß\tCtrl+Shift+&, s"
        expected = "To insert this: \tPress these keys:\r\na, e, i, o, u, A, E, I, O, U \tCtrl+` (accent grave), the letter\r\na, e, i, o, u, y, A, E, I, O, U, Y\tCtrl+' (apostrophe), the letter\r\na, e, i, o, u, A, E, I, O, U\tCtrl+Shift+^ (caret), the letter\r\na, n, o, A, N, O\tCtrl+Shift+~ (tilde), the letter\r\nae, e, i, oe, ue, y, Ae, E, I, Oe, Ue, Y\tCtrl+Shift+: (colon), the letter\r\na, A\tCtrl+Shift+@ (At), a or A\r\nae, AE\tCtrl+Shift+& (ampersand), a or A\r\nœ, Œ\tCtrl+Shift+& (ampersand), o or O\r\nc, C\tCtrl+, (comma), c or C\r\nd, D\tCtrl+' (apostrophe), d or D\r\no, O\tCtrl+/, o or O\r\n¿\tAlt+Ctrl+Shift+?\r\n¡\tAlt+Ctrl+Shift+!\r\nss\tCtrl+Shift+&, s"
        latinizer = PyLatinize(mappings=(default_mapping,))
        assert latinizer.decompose(input) == expected

    def test_decompose_shouldreturn_headshakinghorizontally(self):
        input = "🙂‍↔️"
        expected = "head shaking horizontally"
        latinizer = PyLatinize(mappings=(emoji_mapping,))
        assert latinizer.decompose(input) == expected

    def test_decompose_shouldreturn_nerdface(self):
        input = "🤓"
        expected = "nerd face"
        latinizer = PyLatinize(mappings=(emoji_mapping,))
        assert latinizer.decompose(input) == expected

    def test_decompose_shouldreturn_decomposedbasicunicodetext(self):
        input = "éáűőúóüöíÉÁŰÚŐÓÜÖÍôňúäéáýžťčšľÔŇÚÄÉÁÝŽŤČŠĽ"
        expected = "eauououeoeiEAUUOOUeOeIonuaeeayztcslONUAeEAYZTCSL"
        latinizer = PyLatinize(mappings=(default_mapping,))
        assert latinizer.decompose(input) == expected

    def test_decompose_shouldreturn_complextext(self):
        input = "你好, 世界! This is a test with ümlauts(üöä) and emojis 😊👍."
        expected = "你好, 世界! This is a test with uemlauts(ueoeae) and emojis smiling face with smiling eyesthumbs up."
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_englishwithsymbolsandaccents(self):
        input = "I ❤ cofée"
        expected = "I red heart cofee"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_germanwithumlauts(self):
        input = "Fußgängerübergänge"
        expected = "Fussgaengeruebergaenge"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_russian(self):
        input = "Я люблю единорогов"
        expected = "Ya lyublyu edinorogov"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_arabic(self):
        input = "أنا أحب حيدات"
        expected = "ana ahb hydat"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_vietnamese(self):
        input = "tôi yêu những chú kỳ lân"
        expected = "toi yeu nhung chu ky lan"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        assert latinizer.decompose(input) == expected

    def test_testdecompose_none_input(self):
        input = None
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        with pytest.raises(ValueError):
            latinizer.decompose(input)

    def test_testdecompose_emptyinput(self):
        input = ""
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        with pytest.raises(ValueError):
            latinizer.decompose(input)

    def test_testdecompose_invalidunicodestring(self):
        input = f"ValidPart {chr(0xD800)} AnotherValidPart"
        latinizer = PyLatinize(mappings=(default_mapping, emoji_mapping))
        with pytest.raises(ValueError):
            latinizer.decompose(input)


if __name__ == "__main__":
    pytest.main()
