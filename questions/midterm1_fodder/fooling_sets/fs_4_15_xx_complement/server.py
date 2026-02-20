import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{xx^c \mid x \in \{0,1\}^*\}$$"""
    server_base.generate(data)
