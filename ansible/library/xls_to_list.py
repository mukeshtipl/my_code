#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Mukesh Gupta'
}

DOCUMENTATION = '''
---
module: xls_to_list

short_description: This module will read xls/xlsx/csv file and will return back list of rows.

version_added: "1.0"

description:
    - "This module will read xls/xlsx file and will return back list of rows. Headers can be set on/off. Sheet Name can be specified"

options:
    path:
        description:
            - path value, path of xls/xlsx file.
        required: True
    to_csv:
        description:
            - path value, path of output csv file. If not passed, output won't be saved in csv file.
        required: False
    to_xlsx:
        description:
            - path value, path of output xlsx file. If not passed, output won't be saved in xlsx file.
        required: False
    input_type:
        description:
            - string value, type of input file (xls/xlsx/csv), if not passed default will be 'xls'.
        required: False
    sheet_name:
        description:
            - string value, name of sheet, if not passed default will be Sheet1.
        required: False
    
    headers:
        description:
            - boolean value, if true, headers will be part of list. By default it will be true.
        required: False
    output_quoted:
        description:
            - boolean value, if true, output in csv file will be quoted. By default it will be true.
        required: False
    skiprows:
        description:
            - int value, Number of rows to skip. By default it will be 0.
        required: False
    select_columns:
        description:
            - list of integer indices of columns (starts from 0) , will be part of list. By default it will be all columns .
        required: False
    new_column_names:
        description:
            - list, new name of columns (count should match with 'select_columns') ,it will override column names given in sheet. By default it will be names given in sheet.
        required: False
    
    

#extends_documentation_fragment: 

author:
    - Mukesh Gupta 
'''

EXAMPLES = '''
# Pass in xls/xlsx/csv file path, sheet_name ,headers(true/false), input_type(xlsx/xls/csv)

- name: Read xlsx File on Server
  xls_to_list: 
    input_type: xlsx
    path: "/tmp/sample.xlsx"
    sheet_name: "Sheet1"
    headers: false
    skiprows:5
    to_csv: "/tmp/samlpe.csv"
    output_quoted: no
  register: result
- debug: var=result
    


'''

RETURN = '''

rows:
    description: Comma separated list of rows.
    type: list
row_count:
    description: Count of rows.
    type: int
message:
    description: The result summary of xls_to_list.
    type: str
ansible_facts:
    description: Multiple set of data values, 1. data_csv 2. data_dict 3. data_rows  
    type: dict
'''


import os
import sys
import io
import csv
import pandas as pd
#import yaml

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        path=dict(type='path', required=True),
        to_csv=dict(type='path', required=False,default=None),
        to_xlsx=dict(type='path', required=False,default=None),
        sheet_name=dict(type='str', required=False),
        headers=dict(type='bool', required=False, default=True),
        skiprows=dict(type='int', required=False, default=0),
        select_columns=dict(type='list',required=False,default=None),
        new_column_names=dict(type='list',required=False,default=None),
        output_quoted=dict(type='bool', required=False, default=True),
        input_type=dict(type='str',required=False,default="xls")
    )

    #result = {"ansible_facts":{}}
    result = dict(
        changed=False,
        rows=[],
        row_count=0,
        message='',
        ansible_facts={}
    )

   
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    
    if module.check_mode:
        return result
    #module.exit_json(**result)

    try:
        file_path=os.path.expanduser(module.params['path'])
        
        sheet_name=module.params['sheet_name']
        headers=module.params['headers']
        output_quoted=module.params['output_quoted']

        if sheet_name==None:
            sheet_name=0
        select_columns=module.params['select_columns']
        new_column_names=module.params['new_column_names']
        skiprows=module.params['skiprows']
        
        input_type=module.params['input_type']
        
        if input_type.lower() not in ['xls','xlsx','csv']:
            result['fail_args']={'reason':"invalid value of parameter 'input_type', valid valuse are 'xls'/'xlsx'/'csv'",'input_type':input_type}
            result['msg']="invalid value of parameter 'input_type'"
            module.fail_json(**result)

        
        to_csv=module.params['to_csv']

        csv_path=None
        if to_csv!=None:
            csv_path=os.path.expanduser(module.params['to_csv'])

        to_xlsx=module.params['to_xlsx']

        xlsx_path=None
        if to_xlsx!=None:
            xlsx_path=os.path.expanduser(module.params['to_xlsx'])

        rows=[]
        if input_type.lower() =='csv':
            data = pd.read_csv(file_path, skiprows=skiprows, na_filter=False,usecols=select_columns,names=new_column_names,dtype=str)
        else:
            data = pd.read_excel(file_path, skiprows=skiprows, sheet_name = sheet_name,na_filter=False,usecols=select_columns,names=new_column_names,dtype=str)
        #print(data.head())
        if(headers):
            
            rows=data.values.tolist()
           
            rows.insert(0,list(data.columns))            
        else:
            rows=data.values.tolist()
            
        data_csv=[",".join(list(map(str,data_row))) for data_row in rows]
        if csv_path!=None:
            if output_quoted:
                data.to_csv(csv_path,index=False,quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            else:
                data.to_csv(csv_path,index=False)
            result['changed']=True
        if xlsx_path!=None:
            xlxs_writer=pd.ExcelWriter(xlsx_path)
            data.to_excel(xlxs_writer,sheet_name,index=False)
            xlxs_writer.save()
            result['changed']=True
    
        
        result['rows']=rows
        result['row_count']=len(rows)
        result['message']= "Found " + str(len(rows)) + " rows in " + file_path
        result['ansible_facts']={"data_csv":data_csv,"data_rows":rows,"data_dict":data.to_dict(orient='records')}
        
        
        


        module.exit_json(**result)
    except Exception as e:
        #result['message']="Error : " 
        result['fail_args']={'reason':e.args,'path':file_path}
        result['msg']='Error in xsl_to_list'
        module.fail_json(**result)

def main():
    run_module()

from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()