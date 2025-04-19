import pytest
from src.pswrd_entropy_gen.generator import Generator


@pytest.mark.parametrize("length",
                         [
                             12,
                             -1,
                             0,
                             17,
                             'Hello',
                             12
                         ])
def test_create_password(length):

    if not isinstance(length, int):

        with pytest.raises(Exception):

            Generator.generate_password(length)

    elif length <= 0:

        with pytest.raises(Exception):

            Generator.generate_password(length)

    elif not isinstance(Generator.generate_password(length), str):

        with pytest.raises(Exception):

            Generator.generate_password(length)

    else:
        test_case = Generator.generate_password(length)
        assert len(test_case) == length
        assert isinstance(test_case, str) == True
