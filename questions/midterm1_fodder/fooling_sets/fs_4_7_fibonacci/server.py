import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"""$$L = \{0^{F_n} \mid n \geq 0\}$$
where $F_n$ is the $n$th Fibonacci number: $F_0 = 0$, $F_1 = 1$, $F_n = F_{n-1} + F_{n-2}$."""
    server_base.generate(data)
