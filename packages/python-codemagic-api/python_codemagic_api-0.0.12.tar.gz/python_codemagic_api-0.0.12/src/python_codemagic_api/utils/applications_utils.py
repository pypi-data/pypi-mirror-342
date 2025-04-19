from python_codemagic_api.base_endpoint import BaseEndpoint

class ApplicationsUtils:

    def __init__(self, applications_endpoint):
        self.applications_endpoint = applications_endpoint

    def add_or_update_environment_variable(self, key, value, group, workflow_id=None, is_secure=True):
        environment_variables = self.applications_endpoint.get_all_environment_variables().json()
        found_environment_variable = None
        for environment_variable in environment_variables:
            if environment_variable['key'] == key and environment_variable['group'] == group:
                found_environment_variable = environment_variable
        
        if found_environment_variable == None:
            a = self.applications_endpoint.create_env_var(key, value, group, workflow_id, is_secure)
        else:
            environment_variable_id = found_environment_variable['id']
            self.applications_endpoint.update_env_var(environment_variable_id, value, is_secure)

    def delete_all_environment_variables_for_app(self, app_id):
        environment_variables = self.applications_endpoint.get_all_environment_variables().json()
        
        for environment_variable in environment_variables:
            self.applications_endpoint.delete_env_var(app_id, environment_variable["id"])
            