import theorielearn.CFGs.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{w \in \{0,1\}^* \mid w \text{ is a palindrome and } \#_1(w) \text{ is even}\}$$"
    )
    server_base.generate(data)
