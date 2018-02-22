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

    department_id = fields.Many2one('hr.department', string="Department")
    date_from = fields.Date(string="Date From" ,default=_get_first)
    date_to = fields.Date(string="Date To" ,default=_get_second)

    @api.multi
    def print_monthly_report(self,data):
        data = {}
        data['form'] = self.read(['department_id','date_from','date_to'])[0]

        return self.env['report'].get_action(self, 'dts_reports.monthlyreport_render', data=data)


class MonthlyReportRender(models.Model):
    _name = 'report.dts_reports.monthlyreport_render'

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
        }

        print 'docargs', docargs
        return self.env['report'].render('dts_reports.monthlyreport_render', docargs)