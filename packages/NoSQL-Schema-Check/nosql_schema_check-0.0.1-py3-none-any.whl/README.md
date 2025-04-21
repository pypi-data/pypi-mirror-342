# NoSQL-Schema-Check

from nosql_schema_check.model import Model

class Model_Class(Model):

&nbsp;&nbsp;&nbsp;&nbsp;Schema={field: value}

&nbsp;&nbsp;&nbsp;&nbsp;Validations={field: function -> True/False}

&nbsp;&nbsp;&nbsp;&nbsp;Default={field: function -> Default value}

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

&nbsp;&nbsp;&nbsp;check_data

&nbsp;&nbsp;&nbsp;print_schema

&nbsp;&nbsp;&nbsp;compare_records

&nbsp;&nbsp;&nbsp;compare_record

&nbsp;&nbsp;&nbsp;update_records

&nbsp;&nbsp;&nbsp;update_record

---
