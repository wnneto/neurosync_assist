import React from 'react';
import { IMaskInput } from 'react-imask';

const Etapa1DadosPessoais = ({ form, errors, errorMessages, handleChange }) => {
  return (
    <>
      {/* Nome Completo */}
      <div className={`field-group ${errors.nome ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          value={form.nome}
          onChange={(e) => handleChange('nome', e.target.value)}
        />
        <span className="floating-label">Nome completo *</span>
        {errors.nome && <span className="error-message">{errorMessages.nome}</span>}
      </div>

      {/* Sexo Biológico */}
      <div className={`field-group ${errors.sexo ? "input-error" : ""}`}>
        <select
          className={`input ${form.sexo ? "selected" : ""}`}
          value={form.sexo}
          onChange={(e) => handleChange("sexo", e.target.value)}
        >
          <option value="" disabled hidden>
            Selecione *
          </option>
          <option value="M">Masculino</option>
          <option value="F">Feminino</option>
        </select>
        <span className="floating-label">Sexo biológico *</span>
        {errors.sexo && <span className="error-message">{errorMessages.sexo}</span>}
      </div>

      {/* Data de Nascimento */}
      <div className={`field-group ${errors.data_nascimento ? 'input-error' : ''}`}>
        <IMaskInput
          className="input"
          placeholder=" "
          mask="00/00/0000"
          value={form.data_nascimento}
          onAccept={(value) => handleChange('data_nascimento', value)}
        />
        <span className="floating-label">Data de nascimento *</span>
        {errors.data_nascimento && (
          <span className="error-message">{errorMessages.data_nascimento}</span>
        )}
      </div>

      {/* Telefone */}
      <div className={`field-group ${errors.telefone ? 'input-error' : ''}`}>
        <IMaskInput
          className="input"
          placeholder=" "
          mask="(00) 00000-0000"
          value={form.telefone}
          onAccept={(value) => handleChange('telefone', value)}
        />
        <span className="floating-label">Telefone *</span>
        {errors.telefone && (
          <span className="error-message">{errorMessages.telefone}</span>
        )}
      </div>

      {/* CPF */}
      <div className={`field-group ${errors.cpf ? 'input-error' : ''}`}>
        <IMaskInput
          className="input"
          placeholder=" "
          mask="000.000.000-00"
          value={form.cpf}
          onAccept={(value) => handleChange('cpf', value)}
        />
        <span className="floating-label">CPF *</span>
        {errors.cpf && <span className="error-message">{errorMessages.cpf}</span>}
      </div>
    </>
  );
};

export default Etapa1DadosPessoais;