import jsonschema

def validators_validator(validator, value, instance, schema):
    """ 'validators' property will contain a list/array of objects, each with at a minumum an id property such as: {'id': 'SomeUniqueValidatorID', ...}
    validator, value, instance, and schema parameters will be passed onto the matching 
    """
    if schema.get('validators'):
        print('VALIDATORS!!!!!')
        print(schema.get('validators'))
        print(instance)
        # TODO: aggregate ValidationErros from list of registered validators
        return []
        # return [jsonschema.exceptions.ValidationError("validators error", instance=instance, validator_value=value)]
    return []

def create_validator(schema=jsonschema.Draft202012Validator):
    return jsonschema.validators.extend(
        schema,
        {
            'validators': validators_validator
        }
    )

ExtendedDraft202012Validator = create_validator(schema=jsonschema.Draft202012Validator)
