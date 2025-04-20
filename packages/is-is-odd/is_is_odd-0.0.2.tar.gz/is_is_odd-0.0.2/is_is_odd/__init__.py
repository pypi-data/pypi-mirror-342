import sys
from typing import Any

import is_odd


class IsIsOdd:
	def __call__(self, __o: Any, /) -> bool:
		return __o is is_odd


sys.modules[__name__] = IsIsOdd()
