import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{0^i\mathtt{1}^j\mathtt{0}^k \mid i + j = 2k\}$$"""
    server_base.generate(data)
