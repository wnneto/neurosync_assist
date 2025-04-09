// backend/utils/email.js
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST,
  port: process.env.EMAIL_PORT,
  auth: {
    user: process.env.EMAIL_USERNAME,
    pass: process.env.EMAIL_PASSWORD
  }
});

module.exports = async ({ email, subject, message }) => {
  const mailOptions = {
    from: 'NeuralSync <no-reply@neurosync.com>',
    to: email,
    subject,
    text: message
    // html: `<p>${message}</p>` // Para versão HTML
  };

  // Em ambiente de desenvolvimento, apenas logamos o email
  if (process.env.NODE_ENV === 'development') {
    console.log('Email enviado:', mailOptions);
    return Promise.resolve();
  }

  return transporter.sendMail(mailOptions);
};