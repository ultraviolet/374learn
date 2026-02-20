import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{(\mathtt{01})^m(\mathtt{10})^n \mid n \geq m \geq 0\}$$"""
    server_base.generate(data)
