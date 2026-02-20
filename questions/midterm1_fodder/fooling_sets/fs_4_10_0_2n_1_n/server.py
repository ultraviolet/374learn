import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{0^{2n}\mathtt{1}^n \mid n \geq 0\}$$"""
    server_base.generate(data)
