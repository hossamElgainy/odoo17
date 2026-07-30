# Change State Wizard – Implementation Plan

This file shows a practical example of how to create a change-state wizard in an Odoo module.

## 1. Create the wizard model
Create a new file named wizard/change_state_wizard.py with the following example:

```python
from odoo import models, fields, api


class ChangeStateWizard(models.TransientModel):
    _name = 'change.state.wizard'
    _description = 'Change State Wizard'

    new_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
    ], string='New State', required=True)

    notes = fields.Text(string='Notes')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            model = self.env.context.get('active_model')
            records = self.env[model].browse(active_ids)
            if records and 'state' in records[0]._fields:
                res['new_state'] = records[0].state
        return res

    def action_change_state(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return

        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.write({'state': self.new_state, 'notes': self.notes})
        return {'type': 'ir.actions.act_window_close'}
```

## 2. Create the wizard view
Create a view file named views/change_state_wizard_view.xml:

```xml
<odoo>
    <record id="view_change_state_wizard_form" model="ir.ui.view">
        <field name="name">change.state.wizard.form</field>
        <field name="model">change.state.wizard</field>
        <field name="arch" type="xml">
            <form string="Change State">
                <group>
                    <field name="new_state"/>
                    <field name="notes"/>
                </group>
                <footer>
                    <button name="action_change_state" string="Apply" type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>
</odoo>
```

## 3. Add the action from the main model
In the main model, add a method like this:

```python
def action_open_change_state_wizard(self):
    return {
        'name': 'Change State',
        'type': 'ir.actions.act_window',
        'res_model': 'change.state.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'default_active_ids': self.ids,
            'active_model': self._name,
            'active_ids': self.ids,
        },
    }
```

You can call this method from a button in the form or tree view.

## 4. Register the wizard in the module
Import the wizard in the module initialization file:

```python
from .wizard import change_state_wizard
```

## 5. Add the wizard to the manifest
Update the module manifest so the new view and Python file are loaded:

```python
{
    'name': 'App One',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/change_state_wizard_view.xml',
    ],
}
```

## 6. Add security access
If the wizard model is new, add access rights in security/ir.model.access.csv:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_change_state_wizard_user,access_change_state_wizard_user,model_change_state_wizard,base.group_user,1,1,1,1
```

## 7. Add the view to the module data
Make sure the XML view file is included in the module data list so it is loaded during installation or upgrade.

## 8. Test the flow
- Install or upgrade the module.
- Open the record list where the action is available.
- Click the button to open the wizard.
- Select a new state and apply it.
- Confirm that the selected records are updated.

## 9. Final check
- Make sure the wizard opens correctly.
- Confirm that the selected records change to the requested state.
- Check that the UI behaves as expected.

## Notes
- Replace the model and field names with the ones used in your module.
- This example is intended as a reference and can be adjusted to match your business logic.
