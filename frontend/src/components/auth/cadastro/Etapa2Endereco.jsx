import React, { useEffect } from 'react';
import { IMaskInput } from 'react-imask';

const Etapa2Endereco = ({
  form,
  errors,
  errorMessages,
  handleChange,
  estados,
  cidades,
  ufSelecionado,
  lockAutoFields,
  setUfSelecionado,
  setCidades
}) => {
  // Atualiza UF selecionada quando o estado muda
  useEffect(() => {
    if (form.estado) {
      const sigla = estados.find(e => e.nome === form.estado)?.sigla;
      setUfSelecionado(sigla);
    }
  }, [form.estado, estados]);

  return (
    <>
      {/* CEP */}
      <div className={`field-group ${errors.cep ? 'input-error' : ''}`}>
        <IMaskInput
          className="input"
          placeholder=" "
          mask="00000-000"
          value={form.cep}
          onAccept={(value) => handleChange('cep', value)}
        />
        <span className="floating-label">CEP *</span>
        {errors.cep && <span className="error-message">{errorMessages.cep}</span>}
      </div>

      {/* Logradouro */}
      <div className={`field-group ${errors.logradouro ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          value={form.logradouro}
          onChange={(e) => handleChange('logradouro', e.target.value)}
          disabled={lockAutoFields}
        />
        <span className="floating-label">Logradouro *</span>
        {errors.logradouro && (
          <span className="error-message">{errorMessages.logradouro}</span>
        )}
      </div>

      {/* Número e Complemento */}
      <div className="form-grid">
        <div className={`field-group ${errors.numero ? 'input-error' : ''}`}>
          <input
            className="input"
            placeholder=" "
            value={form.numero}
            onChange={(e) => handleChange('numero', e.target.value)}
          />
          <span className="floating-label">Número *</span>
          {errors.numero && (
            <span className="error-message">{errorMessages.numero}</span>
          )}
        </div>

        <div className="field-group">
          <input
            className="input"
            placeholder=" "
            value={form.complemento}
            onChange={(e) => handleChange('complemento', e.target.value)}
          />
          <span className="floating-label">Complemento</span>
        </div>
      </div>

      {/* Bairro */}
      <div className={`field-group ${errors.bairro ? 'input-error' : ''}`}>
        <input
          className="input"
          placeholder=" "
          value={form.bairro}
          onChange={(e) => handleChange('bairro', e.target.value)}
          disabled={lockAutoFields}
        />
        <span className="floating-label">Bairro *</span>
        {errors.bairro && (
          <span className="error-message">{errorMessages.bairro}</span>
        )}
      </div>

      {/* Cidade e Estado */}
      <div className="form-grid">
        <div className={`field-group ${errors.cidade ? 'input-error' : ''}`}>
          <select
            className="input"
            value={form.cidade}
            onChange={(e) => handleChange('cidade', e.target.value)}
            disabled={!ufSelecionado || lockAutoFields}
          >
            <option value="">Selecione a Cidade *</option>
            {cidades.map((cidade) => (
              <option key={cidade.id} value={cidade.nome}>
                {cidade.nome}
              </option>
            ))}
          </select>
          {errors.cidade && (
            <span className="error-message">{errorMessages.cidade}</span>
          )}
        </div>

        <div className={`field-group ${errors.estado ? 'input-error' : ''}`}>
          <select
            className="input"
            value={form.estado}
            onChange={(e) => handleChange('estado', e.target.value)}
            disabled={lockAutoFields}
          >
            <option value="">Selecione o Estado *</option>
            {estados.map(estado => (
              <option key={estado.sigla} value={estado.nome}>
                {estado.nome}
              </option>
            ))}
          </select>
          {errors.estado && (
            <span className="error-message">{errorMessages.estado}</span>
          )}
        </div>
      </div>
    </>
  );
};

export default Etapa2Endereco;