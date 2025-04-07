def gerar_resumo_paciente(consulta):
    paciente = consulta.paciente
    dados = getattr(paciente, 'dadosmedicos', None)

    idade = getattr(paciente, 'idade', 'não informada')
    sexo = paciente.sexo.capitalize() if paciente.sexo else "Não informado"
    altura = f"{dados.altura} m" if dados and dados.altura else "não informada"
    peso = f"{dados.peso} kg" if dados and dados.peso else "não informado"
    fumante = "fumante" if dados and dados.fumante else "não fumante"
    etilista = "bebe socialmente" if dados and dados.bebe else "não consome álcool"

    historico = ""
    if dados and hasattr(dados, 'historico_familiar') and dados.historico_familiar.exists():
        historico = ", com histórico familiar relevante"

    resumo = (
        f"Paciente do sexo {sexo.lower()}, idade {idade}, altura {altura}, peso {peso}, "
        f"{fumante}, {etilista}{historico}."
    )

    return resumo
