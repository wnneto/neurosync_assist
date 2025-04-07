import React from 'react';

const Etapa3Acesso = ({ form, errors, errorMessages, handleChange }) => {
  return (
    <>
      {/* Email */}
      <div className={`field-group ${errors.email ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          type="email"
          value={form.email}
          onChange={(e) => handleChange('email', e.target.value)}
        />
        <span className="floating-label">Email *</span>
        {errors.email && (
          <span className="error-message">{errorMessages.email}</span>
        )}
      </div>

      {/* Senha */}
      <div className={`field-group ${errors.password ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          type="password"
          value={form.password}
          onChange={(e) => handleChange('password', e.target.value)}
        />
        <span className="floating-label">Senha *</span>
        {errors.password && (
          <span className="error-message">{errorMessages.password}</span>
        )}
        <div className="password-rules">
          <small>A senha deve conter:</small>
          <ul>
            <li className={form.password.length >= 8 ? 'strong' : 'weak'}>
              Mínimo 8 caracteres
            </li>
            <li className={/[a-zA-Z]/.test(form.password) && /[0-9]/.test(form.password) ? 'strong' : 'weak'}>
              Letras e números
            </li>
            <li className={/[!@#$%^&*]/.test(form.password) ? 'strong' : 'weak'}>
              Caracteres especiais (opcional)
            </li>
          </ul>
        </div>
      </div>

      {/* Confirmação de Senha */}
      <div className={`field-group ${errors.password2 ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          type="password"
          value={form.password2}
          onChange={(e) => handleChange('password2', e.target.value)}
        />
        <span className="floating-label">Confirme sua senha *</span>
        {errors.password2 && (
          <span className="error-message">{errorMessages.password2}</span>
        )}
      </div>
    </>
  );
};

export default Etapa3Acesso;