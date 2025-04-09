import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import { registerUser } from '@/api/authService';
import { getEstados, getCidadesPorEstado } from '@/api/ibgeService';
import { Etapa1DadosPessoais, Etapa2Endereco, Etapa3Acesso, ProgressBar } from '.';
import Base from "@/layouts/Base";
import './CadastroUsuario.css';

export default function CadastroUsuario() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [estados, setEstados] = useState([]);
  const [cidades, setCidades] = useState([]);
  const [ufSelecionado, setUfSelecionado] = useState("");
  const [lockAutoFields, setLockAutoFields] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [shake, setShake] = useState({ field: null, active: false });

  const [form, setForm] = useState({
    nome: "",
    sexo: "",
    data_nascimento: "",
    telefone: "",
    cpf: "",
    cep: "",
    logradouro: "",
    numero: "",
    complemento: "",
    bairro: "",
    cidade: "",
    estado: "",
    email: "",
    password: "",
    password2: "",
    grupo: "paciente",
    aceitou_termos: false,
  });

  const [errors, setErrors] = useState({
    nome: false,
    sexo: false,
    data_nascimento: false,
    telefone: false,
    cpf: false,
    cep: false,
    logradouro: false,
    numero: false,
    bairro: false,
    cidade: false,
    estado: false,
    email: false,
    password: false,
    password2: false,
    aceitou_termos: false
  });

  const [errorMessages, setErrorMessages] = useState({
    nome: "",
    sexo: "",
    data_nascimento: "",
    telefone: "",
    cpf: "",
    cep: "",
    logradouro: "",
    numero: "",
    bairro: "",
    cidade: "",
    estado: "",
    email: "",
    password: "",
    password2: "",
    aceitou_termos: ""
  });

  // Carrega estados ao montar o componente
  useEffect(() => {
    getEstados().then(estados => {
      const formatados = estados.map(e => ({
        sigla: e.sigla,
        nome: e.nome.charAt(0).toUpperCase() + e.nome.slice(1).toLowerCase()
      }));
      setEstados(formatados);
    });
  }, []);

  // Carrega cidades quando UF é selecionada
  useEffect(() => {
    if (ufSelecionado) {
      getCidadesPorEstado(ufSelecionado)
        .then(cidades => {
          setCidades(cidades);
        })
        .catch(error => {
          console.error("Erro ao carregar cidades:", error);
          setCidades([]);
        });
    } else {
      setCidades([]);
    }
  }, [ufSelecionado]);

  // Auto-preenchimento por CEP
  useEffect(() => {
    const cepLimpo = form.cep.replace(/\D/g, "");
    if (cepLimpo.length === 8) {
      setLockAutoFields(true);
      axios.get(`https://viacep.com.br/ws/${cepLimpo}/json/`)
        .then(({ data }) => {
          if (!data.erro) {
            const estadoEncontrado = estados.find(e => e.sigla === data.uf);
            
            setForm(prev => ({
              ...prev,
              logradouro: data.logradouro || "",
              bairro: data.bairro || "",
              cidade: data.localidade || "",
              estado: estadoEncontrado?.nome || ""
            }));

            if (data.uf) {
              setUfSelecionado(data.uf);
            }
          }
        })
        .catch(error => {
          console.error("Erro ao buscar CEP:", error);
        })
        .finally(() => {
          setTimeout(() => setLockAutoFields(false), 3000);
        });
    }
  }, [form.cep, estados]);

  // Funções de validação
  const validarCPF = (cpf) => {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11) return false;
    
    // Validação de dígitos verificadores
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
      soma = soma + parseInt(cpf.substring(i-1, i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
      soma = soma + parseInt(cpf.substring(i-1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
  };

  const validarDataNascimento = (dataStr) => {
    const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    if (!regex.test(dataStr)) return false;
    
    const [dia, mes, ano] = dataStr.split('/').map(Number);
    const dataObj = new Date(ano, mes - 1, dia);
    const hoje = new Date();
    
    // Verifica se a data é válida (evita 31/02, etc)
    const dataValida = (
      dataObj.getDate() === dia &&
      dataObj.getMonth() === mes - 1 &&
      dataObj.getFullYear() === ano
    );
    
    if (!dataValida) return false;
    
    // Verifica se não é data futura
    if (dataObj > hoje) return false;
    
    // Verifica se tem pelo menos 18 anos
    const idadeMinima = new Date(
      hoje.getFullYear() - 18,
      hoje.getMonth(),
      hoje.getDate()
    );
    
    return dataObj <= idadeMinima;
  };

  const validarSenha = (senha) => {
    return senha.length >= 8 && /[a-zA-Z]/.test(senha) && /[0-9]/.test(senha);
  };

  const triggerError = (field, message) => {
    setErrors(prev => ({ ...prev, [field]: true }));
    setErrorMessages(prev => ({ ...prev, [field]: message }));
    setShake({ field, active: true });
    setTimeout(() => setShake({ field, active: false }), 500);
  };

  const handleChange = (name, value) => {
    if (name === 'nome') {
      value = value
        .replace(/[^a-zA-ZÀ-ÿçÇ\s\-´`~¨]/g, '')
        .toLowerCase()
        .split(' ')
        .map(palavra =>
          palavra
            .split('-')
            .map(parte =>
              parte.charAt(0).toUpperCase() + parte.slice(1)
            )
            .join('-')
        )
        .join(' ');
    }
    
    if (['logradouro', 'bairro', 'complemento'].includes(name)) {
      value = value
        .toLowerCase()
        .replace(/[^a-zA-ZÀ-ÿçÇ0-9\s\-\/ºª.]/g, '')
        .split(' ')
        .map(palavra =>
          palavra
            .split('-')
            .map(parte => parte.charAt(0).toUpperCase() + parte.slice(1))
            .join('-')
        )
        .join(' ');
    }
    
    if (name === 'numero') {
      value = value.replace(/[^a-zA-Z0-9\-\/.]/g, '');
    }
  
    if (name === 'email') {
      value = value
        .toLowerCase()
        .replace(/[^a-z0-9@._\-]/g, '');
    }
  
    if (name === 'telefone') {
      if (!value.startsWith('+55')) {
        value = '+55' + value.replace(/^(\+)?(55)?/, '');
      }
    }
  
    if (name === 'data_nascimento') {
      const onlyNums = value.replace(/\D/g, '');
      let formattedValue = '';
      
      for (let i = 0; i < onlyNums.length; i++) {
        if (i === 0 && onlyNums[i] > 3) continue;
        
        if (i === 1) {
          const day = parseInt(onlyNums[0] + onlyNums[1]);
          if (day > 31) continue;
        }
        
        if (i === 2 && onlyNums[i] > 1) continue;
        
        if (i === 3) {
          const month = parseInt(onlyNums[2] + onlyNums[3]);
          if (month > 12) continue;
        }
        
        if (i === 2 || i === 4) formattedValue += '/';
        formattedValue += onlyNums[i];
      }
      
      value = formattedValue;
    }
    
    if (name === 'aceitou_termos') {
      setForm(prev => ({ ...prev, [name]: value }));
      setErrors(prev => ({ ...prev, [name]: false }));
      return;
    }
  
    setForm(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: false }));
  
    switch (name) {
      case 'cpf':
        if (value.replace(/\D/g, '').length === 11 && !validarCPF(value)) {
          triggerError('cpf', 'CPF inválido');
        }
        break;
      case 'data_nascimento':
        if (value.length === 10 && !validarDataNascimento(value)) {
          triggerError('data_nascimento', 'Data inválida');
        }
        break;
      case 'password':
        if (value && !validarSenha(value)) {
          setErrorMessages(prev => ({
            ...prev,
            password: 'Mínimo 8 caracteres com letras e números'
          }));
        }
        break;
      case 'password2':
        if (value && value !== form.password) {
          triggerError('password2', 'As senhas não coincidem');
        }
        break;
      case 'estado':
        const sigla = estados.find(e => e.nome === value)?.sigla;
        setUfSelecionado(sigla);
        break;
    }
  };

  const validateStep = (step) => {
    let isValid = true;
    const newErrors = { ...errors };
    const newErrorMessages = { ...errorMessages };

    if (step === 1) {
      if (!form.nome.trim()) {
        newErrors.nome = true;
        newErrorMessages.nome = 'Nome é obrigatório';
        isValid = false;
      }
      if (!form.sexo) {
        newErrors.sexo = true;
        newErrorMessages.sexo = 'Sexo é obrigatório';
        isValid = false;
      }
      if (!form.data_nascimento) {
        newErrors.data_nascimento = true;
        newErrorMessages.data_nascimento = 'Data de nascimento é obrigatória';
        isValid = false;
      } else if (!validarDataNascimento(form.data_nascimento)) {
        newErrors.data_nascimento = true;
        const [dia, mes, ano] = form.data_nascimento.split('/').map(Number);
        const dataNasc = new Date(ano, mes - 1, dia);
        const hoje = new Date();
        const idadeMinima = new Date(hoje.getFullYear() - 18, hoje.getMonth(), hoje.getDate());
        
        if (dataNasc > idadeMinima) {
          newErrorMessages.data_nascimento = 'Cadastro permitido apenas para maiores de 18 anos (Art. 2º da Lei nº 10.406/2002)';
        } else {
          newErrorMessages.data_nascimento = 'Data inválida. Por favor, digite uma data válida no formato DD/MM/AAAA';
        }
        isValid = false;
      }

      if (!form.telefone.replace(/\D/g, '')) {
        newErrors.telefone = true;
        newErrorMessages.telefone = 'Telefone é obrigatório';
        isValid = false;
      }
      if (!form.cpf.replace(/\D/g, '')) {
        newErrors.cpf = true;
        newErrorMessages.cpf = 'CPF é obrigatório';
        isValid = false;
      } else if (!validarCPF(form.cpf)) {
        newErrors.cpf = true;
        newErrorMessages.cpf = 'CPF inválido';
        isValid = false;
      }
    } else if (step === 2) {
      if (!form.cep.replace(/\D/g, '')) {
        newErrors.cep = true;
        newErrorMessages.cep = 'CEP é obrigatório';
        isValid = false;
      }
      if (!form.logradouro.trim()) {
        newErrors.logradouro = true;
        newErrorMessages.logradouro = 'Logradouro é obrigatório';
        isValid = false;
      }
      if (!form.numero.trim()) {
        newErrors.numero = true;
        newErrorMessages.numero = 'Número é obrigatório';
        isValid = false;
      }
      if (!form.bairro.trim()) {
        newErrors.bairro = true;
        newErrorMessages.bairro = 'Bairro é obrigatório';
        isValid = false;
      }
      if (!form.cidade.trim()) {
        newErrors.cidade = true;
        newErrorMessages.cidade = 'Cidade é obrigatória';
        isValid = false;
      }
      if (!form.estado.trim()) {
        newErrors.estado = true;
        newErrorMessages.estado = 'Estado é obrigatório';
        isValid = false;
      }
    } else if (step === 3) {
      if (!form.email.trim()) {
        newErrors.email = true;
        newErrorMessages.email = 'Email é obrigatório';
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(form.email)) {
        newErrors.email = true;
        newErrorMessages.email = 'Email inválido';
        isValid = false;
      }
      if (!form.password) {
        newErrors.password = true;
        newErrorMessages.password = 'Senha é obrigatória';
        isValid = false;
      } else if (!validarSenha(form.password)) {
        newErrors.password = true;
        newErrorMessages.password = 'Mínimo 8 caracteres com letras e números';
        isValid = false;
      }
      if (!form.password2) {
        newErrors.password2 = true;
        newErrorMessages.password2 = 'Confirme sua senha';
        isValid = false;
      } else if (form.password2 !== form.password) {
        newErrors.password2 = true;
        newErrorMessages.password2 = 'As senhas não coincidem';
        isValid = false;
      }
      if (!form.aceitou_termos) {
        newErrors.aceitou_termos = true;
        newErrorMessages.aceitou_termos = 'Você precisa aceitar os Termos';
        isValid = false;
      }
    }

    setErrors(newErrors);
    setErrorMessages(newErrorMessages);
    return isValid;
  };

  const formatarDataParaBackend = (dataStr) => {
    const [dia, mes, ano] = dataStr.split('/');
    return `${ano}-${mes}-${dia}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    if (!validateStep(step)) {
      setIsSubmitting(false);
      return;
    }

    if (step < 3) {
      setStep(step + 1);
      setIsSubmitting(false);
      return;
    }

    try {
      const res = await registerUser({
        ...form,
        password1: form.password,
        password2: form.password2,
        estado: estados.find(e => e.nome === form.estado)?.sigla,
        data_nascimento: formatarDataParaBackend(form.data_nascimento),
        cpf: form.cpf.replace(/\D/g, ''),
        telefone: form.telefone.replace(/\D/g, '')
      });

      if (res.success) {
        toast.success('Cadastro realizado com sucesso!');
        setTimeout(() => navigate('/auth/login'), 2000);
      } else if (typeof res.error === 'object') {
        const campoErro = Object.keys(res.error)[0];
        const mensagem = res.error[campoErro]?.[0] || 'Erro desconhecido.';
        toast.error(`Erro no campo "${campoErro}": ${mensagem}`);
      } else {
        toast.error(res.error || 'Erro inesperado no cadastro.');
      }

    } catch (error) {
      toast.error('Erro ao cadastrar usuário.');
      console.error('❌ Erro inesperado:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePrevious = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="form-container">
      <ToastContainer />
      <h1 className="form-title">Crie sua conta</h1>
      
      <ProgressBar step={step} />
      
      <form onSubmit={handleSubmit} className="card">
        {step === 1 && (
          <Etapa1DadosPessoais 
            form={form}
            errors={errors}
            errorMessages={errorMessages}
            handleChange={handleChange}
            shake={shake}
          />
        )}

        {step === 2 && (
          <Etapa2Endereco 
            form={form}
            errors={errors}
            errorMessages={errorMessages}
            handleChange={handleChange}
            estados={estados}
            cidades={cidades}
            ufSelecionado={ufSelecionado}
            lockAutoFields={lockAutoFields}
            setUfSelecionado={setUfSelecionado}
            setCidades={setCidades}
            shake={shake}
          />
        )}

        {step === 3 && (
          <Etapa3Acesso 
            form={form}
            errors={errors}
            errorMessages={errorMessages}
            handleChange={handleChange}
            shake={shake}
          />
        )}

        <div className="button-wrapper">
          {step > 1 && (
            <button type="button" className="btn-gray" onClick={handlePrevious}>
              Voltar
            </button>
          )}
          
          <button type="submit" className="btn-blue" disabled={isSubmitting}>
            {isSubmitting ? 'Processando...' : step === 3 ? 'Finalizar Cadastro' : 'Próximo'}
          </button>
        </div>
      </form>
    </div>
  );
}