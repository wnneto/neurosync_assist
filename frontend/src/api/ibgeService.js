export const getEstados = async () => {
  try {
    const response = await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome');
    const estados = await response.json();
    return estados.map(estado => ({
      sigla: estado.sigla,
      nome: estado.nome
    }));
  } catch (error) {
    console.error('Erro ao buscar estados:', error);
    return [];
  }
};

export const getCidadesPorEstado = async (uf) => {
  try {
    const response = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios?orderBy=nome`);
    const cidades = await response.json();
    return cidades.map(cidade => ({
      nome: cidade.nome,
      id: cidade.id
    }));
  } catch (error) {
    console.error(`Erro ao buscar cidades para ${uf}:`, error);
    return [];
  }
};