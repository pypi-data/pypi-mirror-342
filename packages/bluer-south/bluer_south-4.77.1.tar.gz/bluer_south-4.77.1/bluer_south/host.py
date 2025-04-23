from typing import List

from bluer_ai.host import signature as abcli_signature

from bluer_south import fullname


def signature() -> List[str]:
    return [
        fullname(),
    ] + abcli_signature()
