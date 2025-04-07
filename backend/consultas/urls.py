from django.urls import path
from consultas.views.colaborador.atribuir_medico_view import AtribuirMedicoView
from consultas.views.medico.relatorio_pdf_view import GerarPDFRelatorioConsultaView
from consultas.views.medico.repasse_export_view import ExportarRepassesMedicoExcelView, ExportarRepassesMedicoPDFView
from consultas.views.paciente.recibo_view import EmitirReciboConsultaView
from consultas.views.colaborador.agenda_geral_view import AgendaGeralView
from consultas.views.colaborador.conciliacao_view import EditarConciliacaoView, ListaTicketsConsolidacaoView
from consultas.views.colaborador.confirmacoes_view import AtualizarConfirmacaoConsultaView, ConfirmacoesPendentesView
from consultas.views.paciente.agendamento_view import AgendarConsultaView, CancelarConsultaView, MinhasConsultasView
from consultas.views.colaborador.reembolso_view import ListaTicketsReembolsoView, AprovarReembolsoView
from consultas.views.medico.agenda_view import AgendaMedicoView
from consultas.views.medico.atendimento_view import DetalhesConsultaView, HistoricoAtendimentosView
from consultas.views.medico.finalizar_consulta_view import FinalizarAtendimentoView, FinalizarConsultaView
from consultas.views.atividades.link_telemedicina_view import GerarLinksTelemedicinaView
from consultas.views.medico.receita_view import CriarReceitaMedicaView




urlpatterns = [
    path('atividades/gerar-links-telemedicina/', GerarLinksTelemedicinaView.as_view(), name='gerar-links-telemedicina'),    
    path('paciente/', MinhasConsultasView.as_view(), name='minhas-consultas'),
    path('paciente/agendar/', AgendarConsultaView.as_view(), name='agendar-consulta'),
    path('paciente/<int:consulta_id>/cancelar/', CancelarConsultaView.as_view(), name='cancelar-consulta'),
    path('paciente/consulta/<int:consulta_id>/recibo/', EmitirReciboConsultaView.as_view(), name='emitir-recibo'),
    path('colaborador/tickets/', ListaTicketsReembolsoView.as_view(), name='listar-tickets'),
    path('colaborador/tickets/<int:ticket_id>/decisao/', AprovarReembolsoView.as_view(), name='decisao-ticket'),
    path('colaborador/agenda/', AgendaGeralView.as_view(), name='agenda-geral'),
    path('colaborador/pendencias/', ConfirmacoesPendentesView.as_view(), name='confirmacoes-pendentes'),
    path('colaborador/pendencias/<int:consulta_id>/atualizar/', AtualizarConfirmacaoConsultaView.as_view(), name='atualizar-confirmacao'),
    path('colaborador/conciliacoes/', ListaTicketsConsolidacaoView.as_view(), name='listar-conciliacoes'),
    path('colaborador/conciliacoes/<int:ticket_id>/editar/', EditarConciliacaoView.as_view(), name='editar-conciliacao'),
    path('consulta/medico/consulta/<int:consulta_id>/', CriarReceitaMedicaView.as_view()),
    path('colaborador/consulta/<int:consulta_id>/atribuir-medico/', AtribuirMedicoView.as_view(), name='atribuir-medico'),
    path('medico/agenda/', AgendaMedicoView.as_view(), name='agenda-medico'),
    path('medico/consulta/<int:consulta_id>/', DetalhesConsultaView.as_view(), name='detalhes-consulta'),
    path('medico/consulta/<int:consulta_id>/finalizar/', FinalizarConsultaView.as_view(), name='finalizar-consulta'),
    path('medico/historico/', HistoricoAtendimentosView.as_view(), name='historico-atendimentos'),
    path('medico/repasses/exportar/excel/', ExportarRepassesMedicoExcelView.as_view(), name='exportar-repasses-excel'),
    path('medico/repasses/exportar/pdf/', ExportarRepassesMedicoPDFView.as_view(), name='exportar-repasses-pdf'),
    path('medico/consulta/<int:consulta_id>/finalizar/', FinalizarAtendimentoView.as_view(), name='finalizar-consulta'),
    path('medico/consulta/<int:consulta_id>/relatorio/pdf/', GerarPDFRelatorioConsultaView.as_view(), name='gerar-pdf-consulta'),
    


    







]
