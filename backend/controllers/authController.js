// backend/controllers/authController.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const sendEmail = require('../utils/email');

// Função para enviar email de recuperação
exports.forgotPassword = async (req, res) => {
  try {
    const { email } = req.body;
    const user = await User.findOne({ email });
    
    if (!user) {
      return res.status(404).json({ message: 'Usuário não encontrado' });
    }

    // Criar token de reset (expira em 1h)
    const resetToken = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    // URL de reset (ajuste para seu frontend)
    const resetUrl = `${process.env.FRONTEND_URL}/reset-password/${resetToken}`;

    // Enviar email
    await sendEmail({
      email: user.email,
      subject: 'Recuperação de Senha - NeuralSync',
      message: `Para redefinir sua senha, clique no link: ${resetUrl}`
    });

    res.status(200).json({ 
      message: 'Email de recuperação enviado' 
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Função para resetar a senha
exports.resetPassword = async (req, res) => {
  try {
    const { token, newPassword } = req.body;
    
    // Verificar token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.id);
    
    if (!user) {
      return res.status(404).json({ message: 'Usuário não encontrado' });
    }

    // Atualizar senha
    user.password = newPassword;
    await user.save();

    res.status(200).json({ 
      message: 'Senha alterada com sucesso' 
    });
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(400).json({ message: 'Token expirado' });
    }
    res.status(400).json({ message: 'Token inválido' });
  }
};