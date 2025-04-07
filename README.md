# 🧠 NeuralSync - Sistema de Gestão e Telemedicina

Sistema completo Django + React voltado para clínicas médicas, com foco em neurologia e telemedicina. Inspirado em "Project Hospital", com funcionalidades administrativas e clínicas integradas.

---

## 🚀 Início Rápido

### Backend (Django)
```bash
cd backend/core
python manage.py runserver
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

---

## 📦 Estrutura de Pastas
```
backend/
├── core/                  # settings.py, urls.py
├── users/                 # modelo de usuário, registro, login
├── consultas/             # agendamento, cancelamento, relatório, PDF
├── financeiro/            # conciliação, repasse
├── epione/                # sintomas, doenças, IA médica
└── templates/relatorio/   # HTMLs dos PDFs
```

frontend/
├── src/
│   ├── pages/             # Telas principais
│   ├── components/        # Componentes reutilizáveis
│   └── lib/axios.js       # Integração centralizada com backend
```

---

## 🔐 Autenticação
- Login por email (dj-rest-auth + allauth + JWT)
- Suporte a login social (Google, Facebook) [em breve]
- Toda requisição protegida com `JWT + Cookie`

---

## 📡 Axios Centralizado

### Caminho:
```frontend/src/lib/axios.js```

### Conteúdo:
```js
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  withCredentials: true,
});

export default api;
```

### Uso:
```js
import api from "@/lib/axios";

const response = await api.get("consultas/paciente/");
```

---

## 🧾 Relatórios em PDF
- Gerados via `WeasyPrint`
- Templates em `core/templates/relatorio/relatorio_pdf.html`
- Acesso via endpoint:
```
GET /api/consultas/medico/consulta/<id>/relatorio/pdf/
```

---

## 🎥 Telemedicina
- Geração automática de link do Jitsi Meet
- Regras: consulta marcada, com médico definido, e futura
- Link salvo no campo `link_telemedicina`

---

## 💼 Grupos e Permissões
- Criados via script: `configurar_grupos.py`
- Cada usuário pertence a um grupo (paciente, médico, colaborador, admin)
- Permissões refinadas para cada endpoint e model

---

## 📈 Relatórios Administrativos
- Visualização de atendimentos, cancelamentos, desempenho
- Exportação PDF/Excel por período
- Filtros por sexo, idade, tipo de consulta, médico, etc

---

## 📅 Agendamento
- Tipos: Particular, Convênio, Retorno
- Confirmações via painel colaborador
- Geração automática de retorno entre 7 e 30 dias
- Cancelamento com regras de multa, reembolso, histórico

---

## 📊 Conciliação e Repasse
- Toda consulta gera:
  - Ticket de conciliação financeira
  - Repasse ao médico (percentual + ajustes)
- Histórico e logs das alterações

---

## 🧠 IA Médica (Dra. Epione)
- Em planejamento
- Sugestão automática de hipóteses diagnósticas e tratamento
- Análise do histórico do paciente + sintomas + exames

---

## ✅ Finalizando Consulta
- Médico conclui e gera relatório
- Consulta é marcada como "realizada"
- Sistema registra comparecimento, repasse, conciliação, notificação
- Relatório PDF disponível para impressão ou compartilhamento

---

## 💻 Contato
Desenvolvido por Wilson Nóbrega.
Para dúvidas ou contribuições, entre em contato via GitHub ou e-mail.

