import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import ModalTermoPrivacidade from '@/components/modals/ModalTermoPrivacidade';

const Etapa3Acesso = ({ form, errors, errorMessages, handleChange }) => {
  const [senhasVisiveis, setSenhasVisiveis] = useState(false);

  const toggleVisibilidadeSenhas = () => {
    setSenhasVisiveis(prev => !prev);
  };

  const [mostrarModal, setMostrarModal] = useState(false);


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
   <div className={`field-group senha-group ${errors.password ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          type={senhasVisiveis ? "text" : "password"}
          value={form.password}
          onChange={(e) => handleChange('password', e.target.value)}
        />
        <span className="floating-label">Senha *</span>
        <span className="eye-inside" onClick={toggleVisibilidadeSenhas}>
          {senhasVisiveis ? <EyeOff size={20} /> : <Eye size={20} />}
        </span>
        {errors.password && <span className="error-message">{errorMessages.password}</span>}
      </div>

      {/* Confirmar Senha */}
      <div className={`field-group senha-group ${errors.password2 ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          type={senhasVisiveis ? "text" : "password"}
          value={form.password2}
          onChange={(e) => handleChange('password2', e.target.value)}
        />
        <span className="floating-label">Confirmar Senha *</span>
        <span className="eye-inside" onClick={toggleVisibilidadeSenhas}>
          {senhasVisiveis ? <EyeOff size={20} /> : <Eye size={20} />}
        </span>
        {errors.password2 && <span className="error-message">{errorMessages.password2}</span>}
      </div>


{/* Checkbox de termos */}
<div className={`field-group checkbox-group ${errors.aceitou_termos ? 'input-error' : ''}`}>
  <label className="checkbox-label">
    <input
      type="checkbox"
      checked={form.aceitou_termos}
      onChange={(e) => handleChange('aceitou_termos', e.target.checked)}
    />
    <span className="checkbox-text">
      Declaro que li e aceito os{' '}
      <button
        type="button"
        className="link-termo"
        onClick={() => setMostrarModal(true)}
      >
        Termos
      </button>
    </span>
  </label>

  {errors.aceitou_termos && (
    <span className="error-message">{errorMessages.aceitou_termos}</span>
  )}
</div>

<ModalTermoPrivacidade isOpen={mostrarModal} onClose={() => setMostrarModal(false)} />

    </>
  );
};

export default Etapa3Acesso;
