from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    state = fields.Selection([
        ('01_in_progress', 'In Progress'),
        ('1_done', 'Done'),
        ('1_canceled', 'Canceled')
    ], default='01_in_progress')



    def write(self, vals):
        res = super(ProjectTask, self).write(vals)

        if 'stage_id' in vals:
            for record in self:

                if record.stage_id.name == "Done":
                    record.state = "1_done"

                elif record.stage_id.name in ["Cancel", "Cancelled"]:
                    record.state = "1_canceled"

                else:
                    record.state = "01_in_progress"

        return res