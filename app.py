import pandasai as pai
import gradio as gr
from config import carregar_variaveis_ambiente, get_api_key, get_llm
from database import get_engine, listar_tabelas, carregar_tabelas
from descriptions import gerar_descricoes

def obter_ou_criar_dataset(nome, df, descricao):
    path = f"chatbox/{nome.lower()}"
    try:
        return pai.create(path=path, df=pai.DataFrame(df), description=descricao)
    except ValueError as e:
        if "already exists" in str(e):
            return pai.load(path)
        raise


def main():

    # Configuração inicial
    carregar_variaveis_ambiente()
    api_key = get_api_key()
    llm = get_llm()
    pai.config.set({'llm': llm})

    # Carregar o db e as tabelas
    engine = get_engine()
    nomes_tabelas = listar_tabelas(engine)
    tabelas = carregar_tabelas(engine, nomes_tabelas)

    # Gerar descrições das tabelas
    descricoes = gerar_descricoes(tabelas, api_key)

    # Converter para o formato do PandasAI
    dataframes_pai = {
        nome: obter_ou_criar_dataset(nome, df, descricoes[nome])
        for nome, df in tabelas.items()
    }

    # Função para responder pergunta
    def responder(pergunta, historico):
        try:
            resposta = pai.chat(pergunta, *dataframes_pai.values())

            if resposta.type == 'dataframe':
                return resposta.value.to_markdown(index=False)
            elif resposta.type == 'number':
                return str(resposta.value)
            elif resposta.type == 'string':
                return resposta.value
            else:
                return str(resposta.value)            

        except Exception as e:
            return f'Ocorreu um erro ao processar a pergunta{e}'

    # Limpar pergunta e resposta
    def limpar_pergunta_resposta():
        return [],''


    # Interface do Gradio
    with gr.Blocks() as demo:
        gr.Markdown('# **Assistente de consulta do Banco de Dados**')
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder='Faça sua pergunta e tecle enter para enviar ')
        botao_limpar = gr.Button('Limpar conversa.')

        def enviar_pergunta(pergunta, historico):
            resposta = responder(pergunta, historico)
            historico = historico + [
                {"role": "user", "content": pergunta},
                {"role": "assistant", "content": resposta},
            ]
            return historico, ""

        msg.submit(enviar_pergunta, [msg, chatbot], [chatbot, msg])
        botao_limpar.click(limpar_pergunta_resposta, None, [chatbot, msg])

    demo.launch()


if __name__ == '__main__':
    main()



