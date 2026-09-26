from promptnoise.evaluation import score_response


def test_numeric_scoring():
    assert score_response("102", "102", "numeric") == (True, True)
    assert score_response("The answer is 102.", "102", "numeric") == (True, False)


def test_mcq_scoring():
    assert score_response("B", "B", "mcq") == (True, True)
    correct, formatted = score_response("I choose B.", "B", "mcq")
    assert correct is True
    assert formatted is False


def test_exact_is_case_insensitive():
    assert score_response("kyoto", "Kyoto", "exact") == (True, True)
