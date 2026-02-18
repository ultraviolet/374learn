import theorielearn.CFGs.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{0^i 1^j 0^i \mid i \geq 0,\; j \geq 0\}$$"
    )
    server_base.generate(data)
