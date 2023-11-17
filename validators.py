import re, jsonschema
import jsonschema



class RequiredValidator(object):
    id = 'required'
    name = 'Required'
    description = 'Require that the user fill out this field. Internal fields are not required.'
    uses_options = False
    @staticmethod
    def validate(validator, value, instance, schema):
        print('RequiredValidator.validate', instance)
        print(validator, value, instance, schema)
        # return jsonschema.exceptions.ValidationError("This field is required!!!!!!", instance=instance, validator_value=value)
        # raise Exception('validating required')
        if instance is None or instance == '':
            return jsonschema.exceptions.ValidationError("This field is required!!!!!!", instance=instance, validator_value=value)
    def validate_old(self, variable, value, schema={}, data=[], row=[]):
        if schema['properties'].get(variable,{}).get('internal', False):
            return
        if value is None or value == '':
            raise self.validation_class(variable, value,"This field is required.",skip_other_exceptions=True)

_VALIDATOR_CLASSES = [RequiredValidator]
_VALIDATORS = {v.id: v for v in _VALIDATOR_CLASSES}

def validators_validator(validator, value, instance, schema):
    """ 'validators' property will contain a list/array of objects, each with at a minumum an id property such as: {'id': 'SomeUniqueValidatorID', ...}
    validator, value, instance, and schema parameters will be passed onto the matching 
    """
    if schema.get('validators'):
        # print('VALIDATORS!!!!!')
        # print(schema.get('validators'))
        # print(instance)
        validators = schema.get('validators', [])
        # TODO: aggregate ValidationErros from list of registered validators
        errors = []
        for v in validators:
            id = v.get('id')
            Validator = _VALIDATORS.get(id)
            print('VALIDATOR_{}'.format(id), Validator)
            if Validator:
                print('VALIDATING....'+id, Validator.validate)
                # yield jsonschema.exceptions.ValidationError("This field is required", instance=instance, validator_value=value) 
                error = Validator.validate(validator, value, instance, schema)
                if error:
                    errors.append(error)
        return errors
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