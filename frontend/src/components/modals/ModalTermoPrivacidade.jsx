// ModalTermoPrivacidade.jsx
import React from 'react';
import './ModalTermoPrivacidade.css';

const ModalTermoPrivacidade = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Política de Privacidade - NeuralSync</h2>
          <button className="close-button" onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24">
              <path fill="#444" d="M18.3 5.71a1 1 0 0 0-1.41 0L12 10.59 7.11 5.7a1 1 0 1 0-1.41 1.42L10.59 12l-4.89 4.89a1 1 0 0 0 1.41 1.41L12 13.41l4.89 4.89a1 1 0 0 0 1.41-1.41L13.41 12l4.89-4.89a1 1 0 0 0 0-1.4z" />
            </svg>
          </button>
        </div>
        <div className="modal-body">
          <p><strong>Política de Privacidade de Dados</strong></p>
          <p>No NeuralSync, sua privacidade é levada a sério...</p>
          <p><strong>📌 Destaques:</strong></p>
          <ul>
            <li><strong>Controladora:</strong> NeuralSync</li>
            <li><strong>Finalidade:</strong> Atendimento médico, segurança, etc.</li>
            <li><strong>Base legal:</strong> LGPD - Lei nº 13.709/2018</li>
            <li><strong>Compartilhamento:</strong> Profissionais e terceiros autorizados</li>
            <li><strong>Seus direitos:</strong> Acesso, correção, exclusão, etc.</li>
          </ul>
          <p><strong>📞 Dúvidas?</strong> <a href="mailto:privacidade@neuralsync.com.br">privacidade@neuralsync.com.br</a></p>
          <p>Ao aceitar, você concorda com esta política.</p>
        </div>
      </div>
    </div>
  );
};

export default ModalTermoPrivacidade;
