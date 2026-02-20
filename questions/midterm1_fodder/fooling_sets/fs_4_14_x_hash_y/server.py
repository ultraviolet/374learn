import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{x\#y \mid x, y \in \{0,1\}^*, \#(\mathtt{0}, x) = \#(\mathtt{1}, y)\}$$"""
    server_base.generate(data)
