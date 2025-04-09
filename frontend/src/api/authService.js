import api from './api';


export const registerUser = async (userData) => {
  try {
    console.log('📤 Dados enviados para registro:', userData);

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
      aceitou_termos: userData.aceitou_termos,
    });

    console.log('✅ Registro bem-sucedido:', response.data);

    return {
      success: true,
      token: response.data.access_token || response.data.access,
      refreshToken: response.data.refresh_token || response.data.refresh,
      user: response.data.user,
    };
  } catch (error) {
    const errorData = error.response?.data;
    console.error('❌ Erro ao registrar usuário:', errorData);

    // Captura erros conhecidos do backend
    if (errorData) {
      if (errorData.email?.length) {
        return { success: false, error: 'Email já cadastrado.' };
      }
      if (errorData.cpf?.length) {
        return { success: false, error: 'CPF já cadastrado.' };
      }
      if (errorData.telefone?.length) {
        return { success: false, error: 'Telefone já cadastrado.' };
      }
      if (errorData.password1?.length) {
        return { success: false, error: errorData.password1.join(' ') };
      }
      if (errorData.non_field_errors?.length) {
        return { success: false, error: errorData.non_field_errors.join(' ') };
      }
    }

    return {
      success: false,
      error: 'Erro desconhecido. Verifique o console ou tente novamente mais tarde.',
    };
  }
};

export const loginUser = async (email, password) => {
  try {
    const response = await api.post('/dj-rest-auth/login/', {
      email,
      password,
    });

    const { access, refresh } = response.data;

    // Armazena token
    localStorage.setItem("token", access);
    api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

    const userRes = await api.get('/dj-rest-auth/user/');

    return {
      token: access,
      refreshToken: refresh,
      user: userRes.data,
    };
  } catch (error) {
    const errorData = error.response?.data;
    console.error('❌ Erro ao fazer login:', errorData);

    if (errorData?.non_field_errors) {
      return { success: false, error: errorData.non_field_errors.join(' ') };
    }

    return { success: false, error: 'Erro ao fazer login. Verifique seus dados.' };
  }
};

export const logoutUser = async () => {
  try {
    await api.post('/dj-rest-auth/logout/');
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  } catch (error) {
    console.error('⚠️ Erro ao fazer logout:', error);
  }
};
