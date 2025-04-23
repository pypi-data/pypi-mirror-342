from unittest import TestCase


class TestVirtualReaction(TestCase):
    def test_get_my_reaction(self):
        from ccml2021 import VirtualReaction

        vr = VirtualReaction(gakusei_id=371)
        assert "Wittig alkene synthesis" == vr.get_my_reaction()

