from typing import Dict, Set, Tuple

class DFA:
    def __init__(self, start: str, accept: Set[str],
                 trans: Dict[Tuple[str, str], str], alphabet: Set[str]):
        self.start = start
        self.accept = accept
        self.trans = trans
        self.alpha = alphabet
        self.dead = "DEAD"
        # заполним недостающие переходы в DEAD и петли из DEAD
        states = {start, *accept, *[s for s,_ in trans], *trans.values(), self.dead}
        for q in states:
            for ch in self.alpha:
                if (q, ch) not in self.trans:
                    self.trans[(q, ch)] = self.dead
        for ch in self.alpha:
            self.trans[(self.dead, ch)] = self.dead

    def accepts(self, s: str) -> bool:
        q = self.start
        for ch in s:
            if ch not in self.alpha:
                return False
            q = self.trans[(q, ch)]
        return q in self.accept

def abcd_then_ef_dfa() -> DFA:
    A = set("abcdef")
    q0,q1,q2,q3,q4,q5,q6 = "q0","q1","q2","q3","q4","q5","q6"
    T = {}
    # abcd^+
    T[(q0,'a')] = q1
    T[(q1,'b')] = q2
    T[(q2,'c')] = q3
    T[(q3,'d')] = q4
    T[(q4,'a')] = q1          # ещё abcd
    # переход к ef^+
    T[(q4,'e')] = q5
    T[(q5,'f')] = q6
    T[(q6,'e')] = q5          # ещё ef
    return DFA(start=q0, accept={q6}, trans=T, alphabet=A)

if __name__ == "__main__":
    A = abcd_then_ef_dfa()
    good = ["abcdef", "abcdabcdef", "abcdefef", "abcdabcdefef"]
    bad  = ["abcefg", "abcde", "abcdabce", "ef", "abcdff", "aabcdef", "abcdab", "efef", "abcdabcdfe"]

    print("GOOD:")
    for s in good:
        print(s, A.accepts(s))

    print()
    print("BAD:")
    for s in bad:
        print(s, A.accepts(s))
