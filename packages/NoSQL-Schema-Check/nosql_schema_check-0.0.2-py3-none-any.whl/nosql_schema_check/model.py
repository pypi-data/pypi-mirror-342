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
    def __init__(self, type, value):
        self.__type = type
        self.__value = value
    @property
    def type(self):return self.__type;
    @property
    def value(self):return self.__value;


class Model:
    __Model_Schema = None

    @staticmethod
    def __get_type(item) -> str:return item.__class__.__name__
    
    @classmethod
    def __get_record_type(cls, schema: any, *args, **kwargs) -> NP_Type | bool:
        try:
            if (type:=cls.__get_type(schema)) == 'dict':
                ret = {}
                kwargs_keys = kwargs.keys()
                for i in schema.keys():
                    if i not in kwargs_keys:
                        kwargs[i] = None
                        print("validation for '{}' field does not exist.".format(i))
                    if (type:=cls.__get_type(data:=schema[i])) == 'tuple':
                        '''
                            data = (type), kwargs[i] = validation
                            data = ('list', type), kwargs[i] = validation
                            data = ('list', dict), kwargs[i] = dict
                            data = ('list', tuple), kwargs[i] = with something
                        '''
                        ret[i] = cls.__get_record_type(data, *(kwargs[i],))
                    elif type == 'dict':
                        '''
                            data = dict, kwargs[i] = dict
                        '''
                        if kwargs[i] == None:kwargs[i] = {}
                        ret[i] = cls.__get_record_type(data, **kwargs[i])
                    else:
                        '''
                            data = type, kwargs[i] = validation
                        '''
                        # print(data, kwargs)
                        ret[i] = Type(data, kwargs[i])
                    if ret[i] == False:
                        raise Exception()
                return NP_Type('dict', ret)
            elif type == 'tuple':
                if schema[0] == 'list':
                    data = None
                    if (type:=cls.__get_type(data:=schema[1])) == 'dict':
                        '''
                            data = dict, args = (dict)
                        '''
                        data = cls.__get_record_type(data, **args[0])
                    elif type == 'tuple':
                        if (data[0]) == 'list':
                            if (type:=cls.__get_type(data[1])) == 'dict':
                                '''
                                    data[1] = dict, args = (dict)
                                '''
                                data = cls.__get_record_type(data[1], **args)
                            elif type == 'tuple':
                                '''
                                    data[1] = tuple, args = (with something)
                                '''
                                data = cls.__get_record_type(data[1], *args)
                            else:
                                '''
                                    data[1] = type, args = (validation)
                                '''
                                if len(args) == 0:args = (None,)
                                data = Type(data[1], args[0])
                        else:
                            '''
                                data = (type), args = (validation)
                            '''
                            if len(args) == 0:args = (None,)
                            data = cls.__get_record_type(data, *args)
                    else:
                        '''
                            data = type args = (validation)
                        '''
                        if len(args) == 0:args = (None,)
                        data = Type(data, args[0])
                    if data == False:
                        raise Exception()
                    return NP_Type('list', data)
                else:
                    '''
                        schema = (type), args = (validation)
                    '''
                    if len(args) == 0:args = (None,)
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
                    if len(schema_keys) > len(dic_keys):raise Exception("fields {} not present in data.".format([i for i in schema_keys if i not in dic_keys]))
                    if not allow_extra:
                        if len(schema_keys) < len(dic_keys):raise Exception("fields {} not present in schema.".format([i for i in dic_keys if i not in schema_keys]))
                    for i in schema.keys():
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
                        if schema.type != (type:=cls.__get_type(i)):raise Exception(error(type, schema.type))
                        else:
                            if type == 'dict':
                                cls.__check_data(schema.value, allow_extra, **i)
                            elif type == 'list':
                                cls.__check_data(schema.value, allow_extra, *i)
                            else:
                                cls.__check_data(schema, allow_extra, *(i,))
                except Exception as e:
                    raise Exception(e)
            def error(s1, s2):return "got type {}, expected {}".format(s1, s2)
            if (type:=cls.__get_type(schema)) == 'NP_Type':
                if schema.type == 'dict' and len(dict_data) != 0:
                    __check_dict(schema.value, dict_data)
                elif schema.type == 'list' and len(data) != 0:
                    __check_list(schema.value, data)
                else:
                    raise Exception(error('different', 'dict or list'))
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
        '''
        i:str = None
        try:
            if "_id" not in data.keys():
                data["_id"]=ObjectId()
            schema_keys = list(cls.__Model_Schema.value.keys())
            dic_keys = list(data.keys())
            if len(schema_keys) > len(dic_keys):raise Exception("fields {} not present in data.".format([i for i in schema_keys if i not in dic_keys]))
            if not allow_extra:
                if len(schema_keys) < len(dic_keys):raise Exception("fields {} not present in schema.".format([i for i in dic_keys if i not in schema_keys]))
            for i in cls.__Model_Schema.value.keys():
                if (type:=cls.__Model_Schema.value[i].type) == 'dict':
                    try:
                        if cls.__get_type(data[i]) != 'dict':
                            raise Exception("dict type expected")
                        cls.__check_data(cls.__Model_Schema.value[i], allow_extra, **data[i])
                    except:
                        raise Exception("got type {}, expected dict".format(cls.__get_type(data[i])))
                elif type == 'list':
                    try:
                        if cls.__get_type(data[i]) != 'list':
                            raise Exception("list type expected")
                        cls.__check_data(cls.__Model_Schema.value[i], allow_extra, *data[i])
                    except:
                        raise Exception("got type {}, expected list".format(cls.__get_type(data[i])))
                else:
                    cls.__check_data(cls.__Model_Schema.value[i], allow_extra, *(data[i],))
            return data
        except Exception as e:
            print(str(e)+(" In field: {}\n{} FIELD's SCHEMA:".format(i, i) if i is not None else ""))
            cls.print_schema(cls.__Model_Schema.value[i])
            return None

    @classmethod
    def generate(cls):
        '''
            generate the Schema Type object (NP_Type) for model
        '''
        def __generate_schema_object(model_name: str, Schema: dict, Validations: dict):
            try:
                if "_id" not in Schema.keys():
                    # raise Exception("field '_id' is not present.")
                    Schema["_id"]='ObjectId'
                    Validations["_id"]=None
                type_dict = None
                if type(Schema) == dict and type(Validations) == dict:
                    type_dict = cls.__get_record_type(Schema, **Validations)
                else:
                    raise Exception("Blog.Schema and Blog.Validations must have type dict.")
                if not type_dict:raise Exception("Object creation failed.")
                _Models[name:=model_name.capitalize()] = type_dict
                print("model {} generated successfully.".format(name))
                # print(type_dict.value)
                return type_dict
            except Exception as e:
                print("Error generating model {}".format(model_name.capitalize()))
                print(e)
                return None
        cls.__Model_Schema = __generate_schema_object(cls.name, cls.Schema, cls.Validations)
    
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
            print(e)
            return None

    @classmethod
    def compare_records(cls, *records: dict, allow_extra=False):
        '''
            *records: dicts of records

            allow_extra: allow extra fields.
        '''
        try:
            return [cls.check_data(cls.__add_defaults(i), allow_extra) for i in records];
        except Exception as e:print(e);return None;
    
    @classmethod
    def compare_record(cls, data: dict, allow_extra=False):
        '''
            data: dict of record

            allow_extra: allow extra fields.
        '''
        try:return cls.check_data(cls.__add_defaults(data), allow_extra);
        except Exception as e:print(e);return None;

    @classmethod
    def update_record(cls, fields: dict, data: dict, allow_extra=False):
        '''
            fields: dict of updated field data

            records: dict of record

            allow_extra: allow extra fields.
        '''
        try:
            for i, j in fields.keys():data[i] = j;
            return cls.check_data(cls.__add_defaults(data), allow_extra);
        except Exception as e:print(e);return None;

    @classmethod
    def update_records(cls, fields: dict, *data: dict, allow_extra=False):
        '''
            fields: dict of updated field data

            *records: dicts of records

            allow_extra: allow extra fields.
        '''
        try:
            for i in data:
                for j, k in fields.keys():i[j] = k;
            return [cls.check_data(cls.__add_defaults(i), allow_extra) for i in data];
        except Exception as e:print(e);return None;




