import re
import requests


def buscar_endereco_por_cep(cep):
    cep = re.sub(r'\D', '', cep)
    if len(cep) != 8:
        return None

    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()

        if 'erro' in data:
            return None

        return {
            'logradouro': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'estado': data.get('uf', ''),
            'cep': formatar_cep(cep),
        }
    except requests.RequestException:
        return None


def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) == 11:
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    return cpf


def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False

    return True


def formatar_telefone(telefone):
    telefone = re.sub(r'\D', '', telefone)
    if len(telefone) == 13:  # Ex: +55 DDD 9XXXXXXX
        return f'+{telefone[:2]} ({telefone[2:4]}) {telefone[4:9]}-{telefone[9:]}'
    elif len(telefone) == 12:
        return f'+{telefone[:2]} ({telefone[2:4]}) {telefone[4:8]}-{telefone[8:]}'
    elif len(telefone) == 11:
        return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
    elif len(telefone) == 10:
        return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}'
    return telefone


def formatar_cep(cep):
    cep = re.sub(r'\D', '', cep)
    if len(cep) == 8:
        return f'{cep[:5]}-{cep[5:]}'
    return cep


def upload_path(instance, filename):
    return f"exames/{instance.usuario.id}/{filename}"