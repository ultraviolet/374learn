import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{w \in \{0,1\}^* \mid \#(\mathtt{0}, w) > \#(\mathtt{1}, w)\}$$"""
    server_base.generate(data)
