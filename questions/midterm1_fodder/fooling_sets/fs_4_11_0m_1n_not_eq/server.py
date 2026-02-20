import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{0^m\mathtt{1}^n \mid m \neq 2n\}$$"""
    server_base.generate(data)
