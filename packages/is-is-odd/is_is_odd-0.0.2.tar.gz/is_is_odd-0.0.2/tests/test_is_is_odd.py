import is_is_odd
import is_odd
import pytest


def test_is_is_odd():
	assert is_is_odd(is_odd)


@pytest.mark.parametrize(
	("x",),
	(
		(1,),
		(is_is_odd,),
		(True,),
		(False,),
		(type,),
		(1 + 2j,),
		(10.0e3,),
		("",),
		([],),
		({},),
		(set(),),
		(BaseException,),
		(pytest,),
		(pytest.mark,),
		(pytest.mark.parametrize,),
	),
)
def test_is_not_is_odd(x):
	assert not is_is_odd(x)
