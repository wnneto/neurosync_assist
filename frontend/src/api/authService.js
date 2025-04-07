import api from './api'; // Importando a instância do axios

export const registerUser = async (userData) => {
  try {
    console.log('Dados sendo enviados:', userData);
    
    const response = await api.post('/dj-rest-auth/registration/', {
      email: userData.email,
      password1: userData.password,
      password2: userData.password2,
      nome: userData.nome,
      sexo: userData.sexo,
      data_nascimento: userData.data_nascimento,
      telefone: userData.telefone,
      cpf: userData.cpf,
      cep: userData.cep,
      logradouro: userData.logradouro,
      numero: userData.numero,
      complemento: userData.complemento || '',
      bairro: userData.bairro,
      cidade: userData.cidade,
      estado: userData.estado,
      pais: userData.pais || 'Brasil'
    });

    console.log('Resposta da API:', response);
    
    return {
      success: true,
      token: response.data.key || response.data.access_token,
      user: response.data.user
    };
    
  } catch (error) {
    console.error('Erro completo:', error);
    
    return {
      success: false,
      error: error.response?.data || { message: error.message }
    };
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/dj-rest-auth/login/', credentials);
    return {
      key: response.data.key,
      user: {
        email: credentials.email,
        // Adicione outros dados do usuário conforme retornado pelo backend
      }
    };
  } catch (error) {
    let errorMessage = 'Credenciais inválidas';
    if (error.response?.data?.non_field_errors) {
      errorMessage = error.response.data.non_field_errors.join(' ');
    }
    throw new Error(errorMessage);
  }
};

export const verifyToken = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return false;
    
    const response = await api.get('/dj-rest-auth/user/');
    return !!response.data.pk; // Verifica se tem primary key do usuário
  } catch (error) {
    console.error('Token verification failed:', error);
    return false;
  }
};

export const logoutUser = async () => {
  try {
    await api.post('/dj-rest-auth/logout/');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
