# -*- coding: utf-8 -*-
from odoo import http

# class /home/odoo/devs/addons/dtsReports(http.Controller):
#     @http.route('//home/odoo/devs/addons/dts_reports//home/odoo/devs/addons/dts_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/odoo/devs/addons/dts_reports//home/odoo/devs/addons/dts_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/odoo/devs/addons/dts_reports.listing', {
#             'root': '//home/odoo/devs/addons/dts_reports//home/odoo/devs/addons/dts_reports',
#             'objects': http.request.env['/home/odoo/devs/addons/dts_reports./home/odoo/devs/addons/dts_reports'].search([]),
#         })

#     @http.route('//home/odoo/devs/addons/dts_reports//home/odoo/devs/addons/dts_reports/objects/<model("/home/odoo/devs/addons/dts_reports./home/odoo/devs/addons/dts_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/odoo/devs/addons/dts_reports.object', {
#             'object': obj
#         })

#