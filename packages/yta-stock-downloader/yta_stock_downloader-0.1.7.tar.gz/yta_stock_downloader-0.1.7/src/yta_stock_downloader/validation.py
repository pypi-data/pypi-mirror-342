from yta_general_utils.programming.validator.parameter import ParameterValidator


def validate_query(query: str):
    ParameterValidator.validate_mandatory_string('query', query, do_accept_empty = False)

def validate_ids_to_ignore(ids_to_ignore: list[str]):
    ParameterValidator.validate_list_of_instances
    # TODO: I'm not sure if the ids are strings or numbers 
    # and they can vary from one platform to another
    ParameterValidator.validate_list_of_string(ids_to_ignore)