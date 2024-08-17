import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.image("superhero.png", width=200)

st.title("Base de Heróis")


# Função auxiliar para exibir mensagens de erro detalhadas
def show_response_message(response, custom_msg=None):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # Se o erro for uma lista, extraia as mensagens de cada erro
                if isinstance(data["detail"], list):
                    errors_list = [error["msg"] for error in data["detail"]]
                    errors = "\n".join(errors_list) 
                    if len(errors_list) == 1 and "not a valid email" in errors:
                        st.error(f"Erro: Email inválido, favor corrigir")
                    else:
                        st.error(f"Erros: {errors}")
                else:
                    # Caso contrário, mostre a mensagem de erro diretamente
                    st.error(f"Erro: {data['detail']['msg']}")
        except ValueError:
            st.error(f"Erro desconhecido. Não foi possível decodificar a resposta.{custom_msg}")


# Adicionar Heroi
with st.expander("Cadastrar um Novo Herói"):
    with st.form("new_hero"):
        name = st.text_input("Nome do Herói")
        description = st.text_area("Descrição do Herói")
        categoria = st.selectbox(
            "Categoria de Poder",
            ["Fire", "Water", "Wood", "Wind"],
        )
        email_heroi = st.text_input("Email do Heroi")
        submit_button = st.form_submit_button("Adicionar Heroi")

        if submit_button:
            response = requests.post(
                "http://backend:8000/heros/",
                json={
                    "name": name,
                    "description": description,
                    "categoria": categoria,
                    "email_heroi": email_heroi,
                },
            )
            show_response_message(response)
# Visualizar Herois
with st.expander("Visualizar Heróis"):
    if st.button("Exibir Todos os Heróis"):
        response = requests.get("http://backend:8000/heros/")
        if response.status_code == 200:
            hero = response.json()
            df = pd.DataFrame(hero)

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "categoria",
                    "email_heroi",
                    "created_at",
                ]
            ]

            # Exibe o DataFrame sem o índice
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Obter Detalhes de um Heroi
with st.expander("Obter Detalhes de um Heroi"):
    get_id = st.number_input("ID do Heroi", min_value=1, format="%d")
    if st.button("Buscar Heroi"):
        response = requests.get(f"http://backend:8000/heros/{get_id}")
        if response.status_code == 200:
            hero = response.json()
            df = pd.DataFrame([hero])
            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "categoria",
                    "email_heroi",
                    "created_at",
                ]
            ]

            # Exibe o DataFrame sem o índice
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Deletar Heroi
with st.expander("Deletar Heroi"):
    delete_id = st.number_input("ID do Heroi para Deletar", min_value=1, format="%d")
    if st.button("Deletar Heroi"):
        response = requests.delete(f"http://backend:8000/heros/{delete_id}")
        show_response_message(response)

# Atualizar Heroi
with st.expander("Atualizar Heroi"):
    with st.form("update_hero"):
        update_id = st.number_input("ID do Heroi", min_value=1, format="%d")
        new_name = st.text_input("Novo Nome do Heroi")
        new_description = st.text_area("Nova Descrição do Heroi")
        new_categoria = st.selectbox(
            "Nova Categoria",
            ["Fire", "Water", "Wood", "Wind"],
        )
        new_email = st.text_input("Novo Email do Heroi")

        update_button = st.form_submit_button("Atualizar Heroi")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_categoria:
                update_data["categoria"] = new_categoria
            if new_email:
                update_data["email_heroi"] = new_email
            if update_data:
                
                response = requests.put(
                    f"http://backend:8000/heros/{update_id}", json=update_data
                )

                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")