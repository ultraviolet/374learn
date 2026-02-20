import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{w \in \{0,1\}^* \mid w = w^R \text{ and } |w| \equiv 0 \pmod{3}\}$$"""
    server_base.generate(data)
