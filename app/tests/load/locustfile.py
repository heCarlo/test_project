from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    """
    Comportamento do usuário para testar endpoints relacionados a roles e criação de usuários.

    Esta classe define as tarefas a serem executadas durante o teste de carga,
    incluindo a obtenção de roles por ID e a criação de novos usuários com dados simulados.
    """

    @task(2)
    def get_role_by_id(self):
        """
        Testa o endpoint de obter role por ID.

        Este método simula a consulta a diferentes IDs de roles, incluindo IDs válidos e inválidos,
        e avalia o comportamento do sistema com base nos status de resposta recebidos.
        
        A tarefa envia um ID aleatório (entre 1 e 5) para verificar o comportamento do endpoint `/role/{role_id}`.

        Caso um ID inválido seja enviado e o sistema retorne um 404, considera-se que o teste foi bem-sucedido.
        Caso o status seja 200, considera-se que o role foi encontrado corretamente.

        :return: None
        """
        role_id = random.randint(1, 5)
        with self.client.get(f"/role/{role_id}", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
                print(f"Role ID {role_id} não encontrado. Status: {response.status_code}")
            elif response.status_code == 200:
                response.success()
                print(f"Role ID {role_id} encontrado com sucesso.")
            else:
                response.failure(f"Falha ao obter role com ID {role_id}. Status: {response.status_code}")

    @task(1)
    def create_user(self):
        """
        Testa o endpoint de criação de usuário.

        Este método envia dados fictícios para criar novos usuários no sistema através do endpoint `/users/`.

        A tarefa envia um conjunto de dados, incluindo nome, e-mail, senha e ID de role.
        Caso o usuário seja criado com sucesso (status 201 ou 200), considera-se que o teste foi bem-sucedido.
        Se o erro for "e-mail já registrado" (status 400), esse erro é tratado como esperado e considerado sucesso.
        
        :return: None
        """
        user_data = {
            "name": f"Test User {random.randint(1, 1000)}",
            "email": f"user{random.randint(1, 1000)}@example.com",
            "password": "test1234",
            "role_id": random.randint(1, 2)
        }
        with self.client.post("/users/", json=user_data, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
                print(f"Usuário criado com sucesso: {response.json()}")
            elif response.status_code == 200:
                response.success()
                print(f"Usuário criado com sucesso: {response.json()}")
            elif response.status_code == 400 and "email already registered" in response.text:
                response.success()
                print("Erro esperado: E-mail já registrado.")
            else:
                response.failure(f"Falha ao criar usuário (Status: {response.status_code}): {response.text}")

class WebsiteUser(HttpUser):
    """
    Define o usuário de carga para testar os endpoints com comportamento definido em `UserBehavior`.

    Esta classe herda de `HttpUser` e inclui o comportamento de carga que foi definido na classe `UserBehavior`.
    Define também o intervalo de tempo entre as requisições, para simular a atividade do usuário.

    :param tasks: A lista de tarefas a serem realizadas, definida como `UserBehavior`.
    :param wait_time: Intervalo entre as requisições (em segundos), determinado entre 1 e 5 segundos.
    """
    tasks = [UserBehavior]
    wait_time = between(1, 5)
