# -*- encoding: utf-8 -*-

from openerp.osv import osv

class stock_picking (osv.Model):

    _inherit = "stock.picking"
    
    def action_invoice_create (self, cr, uid, ids, journal_id = False, group = False,
            type='out_invoice', context=None):
        """
        Add relationships between stock.picking and sale.order/account.invoice.
        The base code doesn't appear to be doing this? 
        """
        if not isinstance (ids, list):
            ids = [ids]
        res = super (stock_picking,self).action_invoice_create (cr, uid, ids, journal_id, group, type, context=context)
        if res:
            self.build_relationships (cr, uid, ids, res, context)
        return res

    def build_relationships (self, cr, uid, picking_ids, invoice_ids, context):

        sale_pool = self.pool.get ("sale.order")
        for picking_id, invoice_id in zip (picking_ids, invoice_ids):
            self.write (cr, uid, picking_id,
                {
                    "invoice_ids" : [(4, invoice_id)]
                }, context = context)
            
            # The relationship, sale.order.invoice_ids, needs to be populated as well
            picking = self.browse (cr, uid, picking_id, context = context)
            sale_ids = set ()
            for move in picking.move_lines:
                if move.sale_line_id:
                    sale_ids.add (move.sale_line_id.order_id.id)
            if sale_ids:
                sale_pool.write (cr, uid, list (sale_ids),
                    {
                        "invoice_ids": [(4, invoice_id)]
                    }, context = context)
