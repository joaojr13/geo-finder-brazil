import difflib


class EstrategiaComparacao:
    def comparar(self, entrada: str, destino: str) -> bool:
        raise NotImplementedError("Estratégia de comparação não implementada.")


class ComparacaoExata(EstrategiaComparacao):
    def comparar(self, entrada: str, destino: str) -> bool:
        return entrada.strip().lower() == destino.strip().lower()


class ComparacaoFuzzy(EstrategiaComparacao):
    def comparar(self, entrada: str, destino: str) -> bool:
        ratio = difflib.SequenceMatcher(
            None, entrada.lower(), destino.lower()).ratio()
        return ratio >= 0.85
