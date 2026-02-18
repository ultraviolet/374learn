import theorielearn.CFGs.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{0,1\}^* \setminus \{ww \mid w \in \{0,1\}^*\}$$"
        r" — all binary strings that cannot be written as $ww$ for any $w$"
    )
    server_base.generate(data)
