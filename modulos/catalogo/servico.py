from compartilhado import normalizar


class LivroNaoEncontrado(Exception):
    def __init__(self):
        super().__init__("Livro não encontrado")


class ServicoCatalogo:
    def __init__(self, repositorio):
        self._repo = repositorio

    def buscar(self, termo=""):
        livros = [l for l in self._repo.listar() if l.corresponde(termo)]
        return sorted(livros, key=lambda l: normalizar(l.titulo))

    def obter(self, isbn):
        livro = self._repo.buscar(isbn)
        if livro is None:
            raise LivroNaoEncontrado()
        return livro
