#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Mukesh Gupta'
}

DOCUMENTATION = '''
---
module: mod2

short_description: This module will echo message.

version_added: "1.0"

description:
    - "This module will echo message"

options:
    message:
        description:
            - string value,message.
        required: True
   
    

#extends_documentation_fragment: 

author:
    - Mukesh Gupta 
'''

EXAMPLES = '''
# Pass message

- name: Echo Message
  mod2: 
    message: "hello world"
  register: result
- debug: var=result
    


'''

RETURN = '''


'''

import os
import sys
import io
import csv

#import yaml


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(message=dict(type='str', required=True))

    #result = {"ansible_facts":{}}
    result = dict(changed=False, message='', ansible_facts={})

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        return result
    #module.exit_json(**result)

    try:

        message = module.params['message']

        if message is None:
            result['fail_args'] = {
                'reason': "missing value of parameter 'message'",
                'message': message
            }
            result['msg'] = "missing value of parameter 'message'"
            module.fail_json(**result)

        my_helper = MyRoleHelper()
        new_message = my_helper.lcase(message)
        result['msg'] = new_message
        result['message'] = new_message + " custom"

        module.exit_json(**result)
    except Exception as e:
        #result['message']="Error : "
        result['fail_args'] = {'reason': e.args, 'message': message}
        result['msg'] = 'Error in mod2'
        module.fail_json(**result)


def main():
    run_module()


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.my_role_utils import MyRoleHelper
#from module_utils.my_role_utils import MyRoleHelper
if __name__ == '__main__':
    main()