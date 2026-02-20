import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{w \in \{0,1\}^* \mid \text{at least two maximal runs of } \mathtt{0}\text{s in } w \text{ have the same length}\}$$"""
    server_base.generate(data)
