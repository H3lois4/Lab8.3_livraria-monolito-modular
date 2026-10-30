import unicodedata


def normalizar(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sem_acentos if not unicodedata.combining(c)).casefold().strip()


def moeda(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"
