import random

from promptnoise.noise.keyboard import keyboard_noise
from promptnoise.noise.textese import textese_noise


def test_keyboard_noise_is_deterministic_and_preserves_numbers():
    text = "A train travels 180 km in 3 hours."
    out1, edits1 = keyboard_noise(text, 0.10, random.Random(7), ["180", "3"])
    out2, edits2 = keyboard_noise(text, 0.10, random.Random(7), ["180", "3"])
    assert out1 == out2
    assert edits1 == edits2
    assert "180" in out1
    assert "3" in out1
    assert out1 != text


def test_textese_replaces_common_forms():
    output, _ = textese_noise(
        "Can you tell me something because you know?",
        random.Random(1),
        probability=1.0,
    )
    assert " u " in f" {output} "
    assert "smth" in output
    assert "bc" in output
