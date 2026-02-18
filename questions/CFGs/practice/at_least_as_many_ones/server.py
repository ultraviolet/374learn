import theorielearn.CFGs.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{0^i 1^j \mid 0 \leq i \leq j\}$$"
    )
    server_base.generate(data)
