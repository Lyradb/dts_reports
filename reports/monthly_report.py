from odoo import api, fields, models
from datetime import date
import calendar

class MonthlyReportHandler(models.TransientModel):
    _name = 'monthlyreport.handler'

    def _get_first(self):
        curdate = date.today()

        today = curdate.strftime('%Y-%m-01')

        return today
    def _get_second(self):
        curdate = date.today()

        today = date(date.today().year, date.today().month,
                        calendar.monthrange(date.today().year, date.today().month)[1])

        return today

    tracking_type = fields.Selection(string="Tracking Type",
                                     selection=[
                                         ('incoming', 'Incoming'),
                                         ('outgoing', 'Outgoing'),
                                     ], default='incoming')
    outgoing_state = fields.Selection(string="Status",
                             selection=[
                                 ('draft', 'Draft'),
                                 ('send', 'Sent'),
                             ], default='draft')
    incoming_state = fields.Selection(string="Status",
                             selection=[
                                 ('unread', 'Unread'),
                                 ('read', 'Read Message'),
                                 ('view', 'Viewed Documents'),
                                 ('receive', 'Accepted'),
                             ], default='unread')

    department_id = fields.Many2one('hr.department', string="Department")
    document_type_id = fields.Many2one('dts.document.type', string="Document Type")
    date_from = fields.Date(string="Date From" ,default=_get_first)
    date_to = fields.Date(string="Date To" ,default=_get_second)

    @api.multi
    def print_monthly_report(self, data):
        data = {}
        data['form'] = self.read(['tracking_type','outgoing_state','incoming_state','document_type_id','department_id','date_from','date_to'])[0]

        return self.env['report'].get_action(self, 'dts_reports.monthly_report_templates', data=data)

class MonthlyReportRender(models.AbstractModel):
    _name = 'report.dts_reports.monthly_report_templates'

    def get_monthly_report_list(self,docs):
        date_f = docs.date_from
        date_t = docs.date_to
        tracking_type = docs.tracking_type
        dept_id = docs.department_id
        doc_type_id = docs.document_type_id
        out_state = docs.outgoing_state
        in_state = docs.incoming_state
        result = None

        if tracking_type == 'incoming':
                result = self.env['dts.employee.documents'].sudo().search([('receiver_office_id','=',dept_id.id),
                                                                       ('state', '=', in_state),
                                                                        ('document_type_id', '=', doc_type_id.id),
                                                                       ('send_date', '>=', date_f),
                                                                       ('send_date', '<=', date_t)])


        if tracking_type == 'outgoing':
            # for department in dept_id:

                result = self.env['dts.document'].sudo().search([('sender_office_id', '=', dept_id.id),
                                                                ('state', '=', out_state),
                                                                ('document_type_id', '=', doc_type_id.id),
                                                                ('transaction_date', '>=', date_f),
                                                                ('transaction_date', '<=', date_t)])
        return result

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        dts_line = self.get_monthly_report_list(docs)

        period = None
        if docs.date_from and docs.date_to:
            period = "From " + str(docs.date_from) + " To " + str(docs.date_to)
        elif docs.date_from:
            period = "From " + str(docs.date_from)
        elif docs.date_from:
            period = " To " + str(docs.date_to)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'department': docs.department_id.name,
            'period': period,
            'dts': dts_line,
        }

        print 'docargs', docargs
        return self.env['report'].render('dts_reports.monthly_report_templates', docargs)

