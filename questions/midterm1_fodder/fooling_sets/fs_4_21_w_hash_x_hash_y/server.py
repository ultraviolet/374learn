import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{w\#x\#y \mid w, x, y \in \{0,1\}^*, w, x, y \text{ are not all equal}\}$$"""
    server_base.generate(data)
