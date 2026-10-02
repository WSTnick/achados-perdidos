document.addEventListener("DOMContentLoaded", () => {
    const descricao = document.getElementById("descricao");
    const contador = document.getElementById("contador");

    if (descricao && contador) {
        const atualizarContador = () => {
            contador.textContent = descricao.value.length;
        };

        descricao.addEventListener("input", atualizarContador);
        atualizarContador();
    }

    const imagem = document.getElementById("imagem");
    const nomeArquivo = document.getElementById("nome-arquivo");

    if (imagem && nomeArquivo) {
        imagem.addEventListener("change", () => {
            nomeArquivo.textContent = imagem.files.length
                ? imagem.files[0].name
                : "Clique para selecionar uma imagem";
        });
    }

    setTimeout(() => {
        document.querySelectorAll(".alerta").forEach((alerta) => {
            alerta.style.transition = "opacity .4s";
            alerta.style.opacity = "0";
            setTimeout(() => alerta.remove(), 400);
        });
    }, 4000);
});
