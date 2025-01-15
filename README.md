<h1 align="center">Hefesto</h1>

Hefesto foi projetado para facilitar a organização e a junção de múltiplos arquivos PDF de plantas de engenharia. Seu objetivo principal é **auxiliar o processo de plotagem dos arquivos**, recebendo grandes quantidades de desenhos técnicos de diferentes formatos (A0, A1, A2, etc.), juntando-os de forma estruturada em um único PDF por formato.


## 📋 Principais Funcionalidades:

- **Seleção de Pastas:** Selecione uma pasta e o software identificará todos os PDFs dentro dela recursivamente.

- **Agrupamento Inteligente:** Agrupa os PDF pelo seus respectivos formatos (A0, A1, A2, A3, A4, Variantes Estendidas e Formatos Desconhecidos).

- **Página Separadora - A4:** Ao mesclar arquivos em formato A4, duas páginas em branco são adicionadas entre cada documento. Essas páginas funcionam como separadores, permitindo que o usuário envie um arquivo único para a impressora e obtenha divisões claras entre os trabalhos impressos.

- **Arquivos Organizados:** Os PDFs mesclados são salvos automaticamente na pasta Downloads, organizados em pastas sequenciais (ex: he_001, he_002, etc.), permitindo rastrear facilmente diferentes tarefas.

- **Logs Detalhados:** Gera um arquivo de log informativo com a quantidade de arquivos processados por formato. Após a plotagem, esses logs permitem ao usuário validar se a quantidade de arquivos plotados corresponde à quantidade real de documentos.


## 🎥 Funcionamento
https://github.com/user-attachments/assets/12cc2707-05f4-4cf8-8506-8900f7121e74


## 🚀 Arquitetura e Boas Práticas:

- **Código Limpo e Estruturado:**
O projeto segue boas práticas de programação, essa abordagem modular torna o código mais legível, fácil de manter e escalar.

- **Pronto para Expansão:**
Projetado desde o início para ser facilmente extensível, o projeto está licenciado sob a **Licença MIT**, o que permite que você utilize o código-fonte livremente, adicione novas funcionalidades e o modifique conforme as suas necessidades.


## 🛠️ Tecnologias Utilizadas
- Python 3.12.6
- PyQt6: Framework para criação de interfaces gráficas.
- pypdf: Biblioteca para manipulação de arquivos PDF.


## 📦 Instalação

Você pode baixar a versão executável do Hefesto diretamente do [último release](https://github.com/hyagodejesus/Hefesto/releases/tag/Release-1).

1. Clique no link acima para acessar a página de Releases.
2. Baixe o arquivo `hefesto.zip`.
3. Descompacte, execute o instalador e siga as instruções para concluir a instalação.


