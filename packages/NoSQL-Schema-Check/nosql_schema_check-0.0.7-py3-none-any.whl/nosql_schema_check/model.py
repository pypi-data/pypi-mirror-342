from bson.objectid import ObjectId

_Models = {}

class Type:
    def __init__(self, type, validation):
        self.__type = type
        self.__validation = validation
    @property
    def type(self):return self.__type;
    @property
    def validation(self):return self.__validation;

    def __str__(self):
        return "{}".format(self.__type)

class NP_Type:
    def __init__(self, type, value, validation, required=None):
        self.__type = type
        self.__value = value
        self.__validation = validation
        if self.__type == 'dict':
            self.__required = required
    @property
    def type(self):return self.__type;
    @property
    def value(self):return self.__value;
    @property
    def validation(self):return self.__validation;
    @property
    def required(self):return self.__required if self.__type == 'dict' else None;


class Model:
    __Model_Schema = None

    name=""
    Schema={}
    Validations={}
    Default={}
    Required=["_id",]

    @staticmethod
    def __get_type(item) -> str:return item.__class__.__name__
    
    @classmethod
    def __get_record_type(cls, schema: any, required:list[str] | None, *args, **kwargs) -> NP_Type | bool:
        try:
            '''
                type = dict, contains key, value pairs.
            '''
            if (type:=cls.__get_type(schema)) == 'dict':
                args_dict = args
                schema_keys = schema.keys();
                required_fields_dict = []
                if required:
                    for i in required:
                        if cls.__get_type(i) == 'tuple':
                            i = i[0]
                        if i not in schema_keys:raise Exception("Required field '{}' not present in Schema".format(i))
                        required_fields_dict.append(i)
                ret = {}
                kwargs_keys = kwargs.keys()
                for i in schema_keys:
                    required_fields = []
                    for j in required:
                        if cls.__get_type(j) == 'tuple' and j[0] == i:
                            required_fields = j[1]
                    if i not in kwargs_keys:
                        kwargs[i] = None
                        print("Validation for '{}' field does not exist.".format(i))
                    validation = None
                    '''
                        kwargs[i] = (function, something)
                    '''
                    # print(kwargs[i], "kwargs...", schema[i], i)
                    if (type:=cls.__get_type(data:=schema[i])) == 'tuple':
                        '''
                            data = (type), kwargs[i] = validation
                            data = ('list', type), kwargs[i] = validation
                            data = ('list', dict), kwargs[i] = dict
                            data = ('list', tuple), kwargs[i] = with something
                        '''
                        # print(required_fields, data, "???", kwargs[i])
                        if cls.__get_type(kwargs[i]) == 'tuple':
                            ret[i] = cls.__get_record_type(data, required_fields, *(kwargs[i][0], (kwargs[i][1],) if len(kwargs[i]) > 1 else (None,)))
                        else:
                            ret[i] = cls.__get_record_type(data, required_fields, *(kwargs[i],))
                    elif type == 'dict':
                        '''
                            data = dict, kwargs[i] = (validation, dict)
                        '''
                        print("dict after dict", kwargs[i], args, data)
                        if kwargs[i] == None:kwargs[i] = {}
                        if cls.__get_type(kwargs[i]) == 'tuple':
                            args = (kwargs[i][0],)
                            kwargs[i] = kwargs[i][1]
                            ret[i] = cls.__get_record_type(data, required_fields, *args, **kwargs[i])
                        else:
                            ret[i] = cls.__get_record_type(data, required_fields, None, **kwargs[i])
                    else:
                        '''
                            data = type, kwargs[i] = validation
                        '''
                        # print(data, kwargs)
                        ret[i] = Type(data, kwargs[i])
                    if ret[i] == False:
                        raise Exception()
                return NP_Type('dict', ret, args_dict[0], required_fields_dict)
            elif type == 'tuple':
                if schema[0] == 'list':
                    data = None
                    validation = None
                    '''
                        args = (function, something) or (something)
                    '''
                    if len(args) > 1 and cls.__get_type(args[0]) == 'function':validation = args[0];args=args[1];
                    if (type:=cls.__get_type(data:=schema[1])) == 'dict':
                        '''
                            data = dict, args = (dict) or ((validation, dict),) or None
                        '''
                        if cls.__get_type(args[0]) == 'tuple':
                            data = cls.__get_record_type(data, required, *(args[0][0],), **args[0][1])
                        else:
                            if args[0] == None:
                                args = ({},)
                            data = cls.__get_record_type(data, required, None, **args[0])
                    elif type == 'tuple':
                        '''
                            data = tuple, args = (with something)
                        '''
                        data = cls.__get_record_type(data, required, *args)
                    else:
                        '''
                            data = type, args = (validation)
                        '''
                        if len(args) == 0:args = (None,)
                        data = Type(data, args[0])
                    # else:
                    #     '''
                    #         data = (type), args = (validation)
                    #     '''
                    #     if len(args) == 0:args = (None,)
                    #     data = cls.__get_record_type(data, *args)
                    if data == False:
                        raise Exception()
                    # print(data)
                    return NP_Type('list', data, validation)
                else:
                    '''
                        schema = (type), args = (validation)
                    '''
                    if len(args) == 0:args = (None,)
                    # print(schema, args, "???")
                    return Type(schema[0], args[0])
        except Exception as e:
            print(e)
            return False
        
    @staticmethod
    def __validate(data, validation):
        try:
            if validation:
                return validation(data)
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def __check_data(cls, schema: NP_Type | Type, allow_extra=False, *data, **dict_data):
        try:
            def __check_dict(schema: dict, dic: dict):
                try:
                    schema_keys = list(schema.keys())
                    dic_keys = list(dic.keys())
                    # if len(schema_keys) > len(dic_keys):raise Exception("fields {} not present in data.".format([i for i in schema_keys if i not in dic_keys]))
                    if not allow_extra:
                        if len(schema_keys) < len(dic_keys):raise Exception("fields {} not present in schema.".format([i for i in dic_keys if i not in schema_keys]))
                    for i in dic_keys:
                        if (type:=cls.__get_type(dic[i])) == 'dict':
                                cls.__check_data(schema[i], allow_extra, **dic[i])
                        elif type == "list":
                            cls.__check_data(schema[i], allow_extra, *dic[i])
                        else:
                            cls.__check_data(schema[i], allow_extra, *(dic[i],))
                except Exception as e:
                    raise Exception(e)
            def __check_list(schema, list: list[any]):
                try:
                    for i in list:
                        # print(i, schema.type, schema.value)
                        if schema.type != (type:=cls.__get_type(i)):raise Exception(error(type, schema.type))
                        else:
                            if type == 'dict':
                                cls.__check_data(schema, allow_extra, **i)
                            elif type == 'list':
                                cls.__check_data(schema, allow_extra, *i)
                            else:
                                cls.__check_data(schema, allow_extra, *(i,))
                except Exception as e:
                    raise Exception(e)
            def error(s1, s2):return "got type {}, expected {}".format(s1, s2)
            if (type:=cls.__get_type(schema)) == 'NP_Type':
                if schema.type == 'dict' and len(dict_data) != 0:
                    if not cls.__validate(dict_data, schema.validation):
                        raise Exception("Validation for value '{}' failed.".format(dict_data))
                    if schema.required:
                        for i in dict_data.keys():
                            if i not in schema.required:raise Exception("Field '{}' not present in {}".format(i, list(schema.value.keys())))
                    __check_dict(schema.value, dict_data)
                elif schema.type == 'list' and len(data) != 0:
                    if not cls.__validate(data, schema.validation):
                        raise Exception("Vaidation for value '{}' failed".format(list(data)))
                    __check_list(schema.value, data)
                else:
                    raise Exception(error('dict' if len(dict_data) > 0 else 'list', schema.type))
            elif type == 'Type':
                for i in data:
                    if (type:=cls.__get_type(i)) != schema.type:
                        raise Exception(error(type, schema.type))
                    if not cls.__validate(i, schema.validation):
                        raise Exception("Validation for value '{}' failed.".format(i))
            else:
                raise Exception("{} is not a valid type".format(type))
            return True
        except Exception as e:
            raise Exception(e)
            

    @classmethod
    def check_data(cls, data: dict, allow_extra=False):
        '''
            data: dict of record

            "DOES NOT ADD DEFAULT VALUES"
        '''
        i:str = None
        try:
            if "_id" not in data.keys():
                data["_id"]=ObjectId()
            schema_keys = list(cls.__Model_Schema.value.keys())
            dic_keys = list(data.keys())
            if len(cls.__Model_Schema.required) > len(dic_keys):raise Exception("fields {} not present in data.".format([i for i in schema_keys if i not in dic_keys]))
            '''
                check if required fields present
            '''
            for i in cls.__Model_Schema.required:
                if i not in dic_keys:raise Exception("Required field {} is not present.".format(i))
            for i in data.keys():
                try:
                    if (type:=cls.__Model_Schema.value[i].type) == 'dict':
                        try:
                            if cls.__get_type(data[i]) != 'dict':
                                print("dict type expected.")
                                raise Exception()
                            cls.__check_data(cls.__Model_Schema.value[i], allow_extra, **data[i])
                        except Exception as e:
                            raise Exception(e)
                    elif type == 'list':
                        try:
                            if cls.__get_type(data[i]) != 'list':
                                print("list type expected.")
                                raise Exception()
                            cls.__check_data(cls.__Model_Schema.value[i], allow_extra, *data[i])
                        except Exception as e:
                            raise Exception(e)
                    else:
                        cls.__check_data(cls.__Model_Schema.value[i], allow_extra, *(data[i],))
                except Exception as e:
                    try:
                        if allow_extra and not cls.__Model_Schema.value[i]:continue;
                        else:raise Exception(e)
                    except:
                        print(e)
                        raise Exception("type/validation Error.")
            return data
        except Exception as e:
            print((" In field: {}\n{} FIELD's SCHEMA:".format(i, i) if i is not None else ""))
            cls.print_schema(cls.__Model_Schema.value[i])
            print(str(e))
            raise Exception("Incorrect Fields.")

    @classmethod
    def generate(cls):
        '''
            generate the Schema Type object (NP_Type) for model
        '''
        def __generate_schema_object(model_name: str, Schema: dict, Validations: dict, Required: list[str]=None):
            try:
                if "_id" not in Schema.keys():
                    # raise Exception("field '_id' is not present.")
                    Schema["_id"]='ObjectId'
                    Validations["_id"]=None
                type_dict = None
                if type(Schema) == dict and type(Validations) == dict:
                    type_dict = cls.__get_record_type(Schema, Required, None, **Validations)
                else:
                    raise Exception("Model_Class.Schema and Model_Class.Validations must have type dict.")
                if not type_dict:raise Exception("Object creation failed.")
                _Models[name:=model_name.capitalize()] = type_dict
                print("model {} generated successfully.".format(name))
                # print(type_dict.value)
                return type_dict
            except Exception as e:
                print("Error generating model {}".format(model_name.capitalize()))
                print(e)
                exit(1)
        if len(cls.Schema) > 0 and cls.name != "":
            cls.__Model_Schema = __generate_schema_object(cls.name, cls.Schema, cls.Validations, cls.Required)
        else:
            print("Model_Class must have variables 'Schema' and 'name'.")
            exit(1)
    
    @classmethod
    def print_schema(cls, schema:NP_Type | Type=None, tab=0):
        '''
            Print the schema for model.
        '''
        start = False
        if schema == None:schema = cls.__Model_Schema;start=True;
        if schema.type == 'dict':
            for _ in range(tab):print("  ", end="")
            print("{")
            for i, j in schema.value.items():
                for _ in range(tab+1 if start else tab+2):print("  ", end="")
                print("FIELD",i, end=" TYPE ");cls.print_schema(j)
            if not start:
                for _ in range(tab+1):print("  ", end="")
                print("},")
            else:print("}")
        elif schema.type == 'list':
            print("[")
            for _ in range(tab+1):print("  ", end="")
            cls.print_schema(schema.value, tab+1)
            for _ in range(tab+1):print("  ", end="")
            print("],")
        else:
            print(str(schema)+",")
    
    @classmethod
    def __add_defaults(cls, data: dict):
        try:
            key_list = [i for i in cls.Default.keys() if i not in list(data.keys())]
            for i in key_list:
                data[i] = cls.Default[i]();
            return data
        except Exception as e:
            raise Exception(e);

    @classmethod
    def compare_records(cls, *records: dict, allow_extra=False):
        '''
            *records: dicts of records

            allow_extra: allow extra fields.
        '''
        try:
            return [cls.check_data(cls.__add_defaults(i), allow_extra) for i in records];
        except Exception as e:print(e);raise Exception(e);
    
    @classmethod
    def compare_record(cls, record: dict, allow_extra=False):
        '''
            data: dict of record

            allow_extra: allow extra fields.
        '''
        try:return cls.check_data(cls.__add_defaults(record), allow_extra);
        except Exception as e:
            print(e);
            raise Exception(e);

    @classmethod
    def update_record(cls, fields: dict, record: dict, allow_extra=False):
        '''
            fields: dict of updated field data

            records: dict of record

            allow_extra: allow extra fields.
        '''
        try:
            for i, j in fields.keys():record[i] = j;
            return cls.check_data(cls.__add_defaults(record), allow_extra);
        except Exception as e:print(e);raise Exception(e);

    @classmethod
    def update_records(cls, fields: dict, *records: dict, allow_extra=False):
        '''
            fields: dict of updated field data

            *records: dicts of records

            allow_extra: allow extra fields.
        '''
        try:
            for i in records:
                for j, k in fields.keys():i[j] = k;
            return [cls.check_data(cls.__add_defaults(i), allow_extra) for i in records];
        except Exception as e:raise Exception(e);


# class Test(Model):
#     Schema={
#         "integer": "int",
#         "string": "str",
#         "list": ('list', "int"),
#         "dict": {
#             "key": "int", 
#             "key1": ('list', {
#                 "integer": "int", 
#                 "list": ('list', 'str')
#             })
#         },
#         "list_in_list": ('list', ('list', "str")),
#         "dict_in_dict": {
#             "a": 'int',
#             "b": {
#                 "a": 'str'
#             }
#         }
#     }
#     Validations={
#         "integer": lambda i: i < 10,
#         "string": lambda s: len(s) < 10,
#         "list": (lambda l: len(l) < 4, lambda i: i < 10),
#         "dict":(lambda d: len(d) < 3,
#             {
#                 "key": lambda i: i < 10,
#                 "key1": (lambda l: len(l) < 2,)
#             }),
#         "list_in_list": lambda s: len(s) < 10,
#         "dict_in_dict": {
#             "b": {
#                 "a": lambda s: len(s) < 20,
#             },
#             "a":lambda i: i < 20
#         }
#     }
#     Required=["integer", "list", ('dict', ["key", ("key1", ["integer"])])]
#     Default={"string":lambda:"Default_String"[:9]}
#     name="test"

# Test.generate()

# try:
#     print(Test.compare_record({"integer": 9, "list": [2, 3, 5], "dict": {"key": 9, "key1": [{"integer": 30}]}, "list_in_list": [["string1", "string2", "string3"]]}))
# except:
#     pass

