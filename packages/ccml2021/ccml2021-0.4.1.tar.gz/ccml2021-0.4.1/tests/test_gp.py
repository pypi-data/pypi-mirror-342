from unittest import TestCase
import subprocess


class TestGP(TestCase):
    def test_one(self):
        cmd = "four_dim_exp1"

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        out, err = p.communicate(bytearray("0 0 0 0", "utf-8"))
        out = out.decode("utf-8")
        err = err.decode("utf-8")
    
        assert "0.0,0.0,0.0,0.0,0.0207810" == out[:25]

    def test_one5555(self):
        cmd = "four_dim_exp1"

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        out, err = p.communicate(bytearray("5 5 5 5", "utf-8"))
        out = out.decode("utf-8")
        err = err.decode("utf-8")
    
        assert "5.0,5.0,5.0,5.0,0.0497213" == out[:25]