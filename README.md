#Cost Table
O Gerenciador de Tabelas de Custos é um aplicativo desenvolvido em Python com interface gráfica utilizando Tkinter. Ele foi criado para facilitar o controle e a organização de custos em diferentes projetos ou categorias, permitindo a criação de múltiplas tabelas, inserção, edição e remoção de itens, além da persistência dos dados em arquivos JSON.

Funcionalidades
Gerenciamento de Múltiplas Tabelas:
Crie, selecione e apague tabelas para organizar os custos por projeto ou categoria.

Inserção, Edição e Remoção de Itens:
Adicione itens informando nome, custo unitário e quantidade. O aplicativo calcula automaticamente o total por item e atualiza o total geral da tabela. É possível editar e remover itens conforme necessário.

Persistência de Dados:
Selecione uma pasta para salvar os dados. O aplicativo armazena todas as informações em arquivos JSON, permitindo que você retome seu trabalho exatamente de onde parou em futuras execuções.

Confirmação Personalizada para Exclusão de Tabelas:
Ao apagar uma tabela, o aplicativo exibe uma janela de confirmação customizada, garantindo que a exclusão seja feita de forma segura.

Interface Amigável:
Com uma interface limpa e organizada, o aplicativo proporciona uma experiência de uso intuitiva e eficiente.

Tecnologias Utilizadas
Python 3.x
Tkinter – Biblioteca padrão para interfaces gráficas em Python.
JSON – Para persistência e armazenamento dos dados.
OS e filedialog – Para manipulação de arquivos e seleção de pastas.
Instalação
Clone o Repositório

bash
Copy
Edit
git clone https://github.com/seu-usuario/gerenciador-tabelas-custos.git
cd gerenciador-tabelas-custos
Crie um Ambiente Virtual (Opcional, mas Recomendado)

bash
Copy
Edit
python -m venv venv
Em seguida, ative o ambiente virtual:

No Windows:
bash
Copy
Edit
venv\Scripts\activate
No macOS/Linux:
bash
Copy
Edit
source venv/bin/activate
Instale as Dependências

Este projeto utiliza apenas bibliotecas padrão do Python, portanto, não há necessidade de instalar dependências adicionais. Certifique-se de estar utilizando o Python 3.x.

Uso
Execute o Aplicativo

No terminal, execute:

bash
Copy
Edit
python app.py
Selecionar Pasta para Armazenamento dos Dados

Clique no botão "Selecionar Pasta de Dados" e escolha uma pasta onde os dados serão salvos e carregados automaticamente nas próximas execuções.

Gerencie suas Tabelas e Itens

Crie novas tabelas com o botão "Nova Tabela".
Insira novos itens preenchendo os campos Nome, Custo e Quantidade e clicando em "Inserir".
Edite ou remova itens conforme necessário.
Apague uma tabela utilizando o botão "Apagar Tabela", que solicitará confirmação através de uma janela customizada.
