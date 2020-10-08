#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Mukesh Gupta'
}

DOCUMENTATION = '''
---
module: dict_to_xlsx

short_description: This module will create xlsx file from dictionary.

version_added: "1.2"

description:
    - "This module will create xlsx file from dictionary."

options:
    data:
        description:
            - dictionary of value for creation of xlsx file.
        required: True

    to_xlsx:
        description:
            - path value, path of output xlsx file. 
        required: True

    startrow:
        description:
            - int value, Number of rows to skip. By default it will be 0.
        required: False
    
    append:
        description:
            - boolean value, if true, new sheets will be added with existing sheets. By default it will be true.
        required: False
    
    
    

#extends_documentation_fragment: 

author:
    - Mukesh Gupta 
'''

EXAMPLES = '''
# Pass in input data as dictionary, output file path, starting row

- name: Create xlsx File on Server
  dict_to_xlsx: 
    data: "{{input_data}}
    startrow: 5
    to_xlsx: "/tmp/samlpe.xlsx"
    append: true
    
  register: result
- debug: var=result
    


'''

RETURN = '''


message:
    description: The result summary of dict_to_xlsx.
    type: str

'''

from ansible.module_utils.basic import AnsibleModule
import os
import sys
import io
import csv
import pandas as pd
from openpyxl import load_workbook
#import yaml


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(data=dict(type='dict', required=True),
                       to_xlsx=dict(type='path', required=False),
                       startrow=dict(type='int', required=False, default=0),
                       append=dict(type='bool', required=False, default=True))

    #result = {"ansible_facts":{}}
    result = dict(changed=False,
                  rows=[],
                  row_count=0,
                  message='',
                  ansible_facts={})

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        return result
    #module.exit_json(**result)

    try:

        data = module.params['data']
        to_xlsx = module.params['to_xlsx']
        startrow = module.params['startrow']
        append = module.params['append']

        xlsx_path = None
        if to_xlsx != None:
            xlsx_path = os.path.expanduser(module.params['to_xlsx'])
        sheets = data['sheets']

        if xlsx_path != None:
            if append == True:
                #xlxs_writer=pd.ExcelWriter(xlsx_path)
                book = load_workbook(xlsx_path)
                xlxs_writer = pd.ExcelWriter(xlsx_path, engine='openpyxl')
                xlxs_writer.book = book
            else:
                xlxs_writer = pd.ExcelWriter(xlsx_path)

        for sheet in sheets:
            sheet_name = sheet['name']
            headers = sheet['headers']
            data_rows = sheet['data_rows']
            df = pd.DataFrame(data_rows, columns=headers)

            df.to_excel(xlxs_writer,
                        sheet_name,
                        index=False,
                        startrow=startrow)
        xlxs_writer.save()
        result['changed'] = True

        #result['message']= "Saved  " + to_xlsx + "having " +  str(len(sheets)) + " sheets  "
        #result['ansible_facts']={"data_csv":data_csv,"data_rows":rows,"data_dict":data.to_dict(orient='records')}

        module.exit_json(**result)
    except Exception as e:
        #result['message']="Error : "
        result['fail_args'] = {'reason': e.args, 'path': to_xlsx}
        result['msg'] = 'Error in dict_to_xlsx'
        module.fail_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()