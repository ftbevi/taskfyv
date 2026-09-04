async def test_criar_e_listar(cliente):
    resposta = await cliente.post("/tarefas", json={"titulo": "Estudar FastAPI"})
    assert resposta.status_code == 201

    criada = resposta.json()
    assert criada["titulo"] == "Estudar FastAPI"
    assert criada["concluida"] is False

    listagem = await cliente.get("/tarefas")
    assert listagem.status_code == 200
    assert len(listagem.json()) == 1


async def test_concluir_tarefa(cliente):
    criada = await cliente.post("/tarefas", json={"titulo": "Fazer deploy"})
    tarefa_id = criada.json()["id"]

    resposta = await cliente.patch(f"/tarefas/{tarefa_id}", json={"concluida": True})
    assert resposta.status_code == 200
    assert resposta.json()["concluida"] is True


async def test_titulo_vazio_rejeitado(cliente):
    resposta = await cliente.post("/tarefas", json={"titulo": ""})
    assert resposta.status_code == 422


async def test_tarefa_inexistente(cliente):
    resposta = await cliente.patch("/tarefas/9999", json={"concluida": True})
    assert resposta.status_code == 404


async def test_healthcheck(cliente):
    resposta = await cliente.get("/health")
    assert resposta.status_code == 200