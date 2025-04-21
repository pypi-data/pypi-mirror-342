# NoSQL-Schema-Check

## pip install NoSQL_Schema_Check

from nosql_schema_check.model import Model

class Model_Class(Model):

&nbsp;&nbsp;&nbsp;&nbsp;Schema={field: value}

&nbsp;&nbsp;&nbsp;&nbsp;Validations={field: function -> True/False}

&nbsp;&nbsp;&nbsp;&nbsp;Default={field: function -> Default value}

&nbsp;&nbsp;Optional variable -

&nbsp;&nbsp;&nbsp;&nbsp;collection=Collection object.

Model_Class.generate()

---

Schema = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": 'type', -> change 'type' with type string.
    
&nbsp;&nbsp;&nbsp;&nbsp;"key1": {key: value, ...},
    
&nbsp;&nbsp;&nbsp;&nbsp;"key2": ('list', 'type') -> change 'type' with type string. ([value1, value2, ...])

}

---

Validations = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": validate function for value,
    
&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;validation for 'type' only.

}

---

Default = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": function that returns default value,

&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;default value for field only.

}

---

functions - 

&nbsp;&nbsp;&nbsp;Model_Class.check_data

&nbsp;&nbsp;&nbsp;Model_Class.print_schema

&nbsp;&nbsp;&nbsp;Model_Class.compare_records

&nbsp;&nbsp;&nbsp;Model_Class.compare_record

&nbsp;&nbsp;&nbsp;Model_Class.update_records

&nbsp;&nbsp;&nbsp;Model_Class.update_record

&nbsp;&nbsp;&nbsp;Model_Class.collection

---
