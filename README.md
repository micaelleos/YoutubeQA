# YoutubeQA

Este repositório contém o código para um bot de perguntas e respostas (QA) para vídeos no YouTube, construído usando Python, Streamlit, LangGraph e Chroma. O bot permite que os usuários realizem perguntas relacionadas a vídeos no YouTube e obtenham respostas precisas baseadas no conteúdo dos vídeos.

## Funcionalidades

- **Análise Automática de Vídeos:** Extração de conteúdo textual de vídeos no YouTube.
- **Respostas Inteligentes:** Uso de LangGraph para processar e responder perguntas sobre os vídeos.
- **Interface Intuitiva:** Interface de usuário simples e interativa desenvolvida com Streamlit.
- **Gerenciamento de Dados:** Utilização do Chroma para armazenamento e recuperação eficiente de dados.

## Tecnologias Utilizadas

- **[Python](https://www.python.org/):** Linguagem de programação principal.
- **[Streamlit](https://streamlit.io/):** Framework para criar aplicações web interativas.
- **[LangGraph](https://github.com/langgraph/langgraph):** Ferramenta para criação e gerenciamento de fluxos de linguagem.
- **[Chroma](https://www.trychroma.com/):** Plataforma para armazenamento e busca vetorial de dados.

## Requisitos

Certifique-se de que você tenha os seguintes itens instalados em seu ambiente:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/micaelleos/YoutubeQA.git
   cd YoutubeQA
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente necessárias (como chaves de API para o YouTube, LangGraph e Chroma):

   ```bash
   export OPEN_API_KEY="sua_chave_aqui"
   ```

4. Inicie o aplicativo Streamlit:

   ```bash
   streamlit run app.py
   ```

5. Acesse o aplicativo no navegador em: [http://localhost:8501](http://localhost:8501)

## Como Usar

1. Cole o URL de um vídeo do YouTube no campo de entrada.
2. Aguarde a extração e indexação do conteúdo do vídeo.
3. Digite suas perguntas no campo apropriado.
4. Receba respostas baseadas no conteúdo do vídeo.

## Estrutura do Projeto

```
├── main.py             # Arquivo principal da aplicação Streamlit
├── README.md          # Documentação do projeto
├── prompt.py
├── requirements.txt
├── tools.py
└── youtubeqa.py
```

## Contribuições

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork deste repositório.
2. Crie uma branch para sua funcionalidade ou correção de bug:
   ```bash
   git checkout -b minha-nova-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie para o GitHub:
   ```bash
   git push origin minha-nova-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

Desenvolvido com ❤ por [Micaelle Souza].

