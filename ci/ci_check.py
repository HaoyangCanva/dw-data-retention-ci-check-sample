import yaml
from schema import Schema, And, Use, Optional, SchemaError

## Step 0: Check whether YAML file is valid
## Step 1: All required fields should exist
##   Step 1.1: meta.canva.retention block exists
##   Step 1.2: has_retention_policy exists and data type is Boolean
##   Step 1.3: if has_retention_policy = True, policy_ref and policy_enabled should exist
##   Step 1.4: if policy_params exists, there should be some param under it and the type of value should be string
## Step 2: the retention policy is defined as per the format defined in Data Tagging Capability.
##   Step 2.1: Required field should not be missing, policy_ref and columns in policy_params
##   Step 2.2: All fields should be pre-designed ones (can be a warning)
##   Step 2.3: Each field’s data type should be correct (string, boolean …)
## Step 3: the retention policy being defined
##   Step 3.1: Check the policy Id / name exist
##   Step 3.2: Check whether policy can be applied to the model/column, there should be some mapping exist


## Step 1
def ci_check(data):
    ## Step 1.1
    # Check if the YAML file has a 'version' key
    if 'version' not in data:
        print("version info missed.")
        return False

    # Check if the 'models' key exists
    if 'models' not in data:
        print("model info missed.")
        return False

    for model in data['models']:
        # Check if 'name' key exists for each model
        if 'name' not in model:
            print("name info missed.")
            return False
        
        # Check if 'config' key exists for each model
        if 'config' not in model:
            print("config info missed.")
            return False
        
        config = model['config']

        # Check if 'meta' key exists in the 'config'
        if 'meta' not in config:
            return False
        
        meta = config['meta']

        # Check if 'canva' key exists in the 'meta'
        if 'canva' not in meta:
            print("config.canva info missed.")
            return False
        
        canva = meta['canva']

        # Check if 'retention' key exists in the 'canva'
        if 'retention' not in canva:
            print("config.canva.retention info missed.")
            return False
        
        retention = canva['retention']

        ## Step 1.2
        # Check if 'has_retention_policy' key exists in the 'retention'
        if 'has_retention_policy' not in retention:
            print("has_retention_policy info missed.")
            return False

        # Check if 'has_retention_policy' value is either 'true' or 'false'
        if retention['has_retention_policy'] not in [True, False]:
            print(f"has_retention_policy is not Boolean {retention['has_retention_policy']}")
            return False

        ## Step 1.3
        if retention['has_retention_policy'] == True:
            retention_policies = retention['retention_policy']
            

            for retention_policy in retention_policies:
                ## Step 2.1
                # Check if 'policy_ref' is correct
                check_policy_ref(retention_policy)

                # Check if 'ploicy_enabled' is correct
                check_ploicy_enabled(retention_policy)

                # Check if 'policy_params' is correct
                check_policy_params(retention_policy)

                # Step 2.2 and Step 2.3
                valid_schema(retention_policy)

                # Step 3.1 and Step 3.2
                verify_validate_policies(retention_policy)

    return True

def check_policy_ref(retention_policy):
    if 'policy_ref' not in retention_policy:
        print("policy_ref info missed.")
        return False
    
    policy_ref = retention_policy['policy_ref']
    if not isinstance(policy_ref, str):
        print(f"policy_ref data type error. Type: {type(policy_ref)}")
        return False
    
    ## exmaple: policy_ref = "ret_2_2"
    if policy_ref[0:4] != 'ret_':
        print(f"policy_ref:{policy_ref} format error.")
        return False

def check_ploicy_enabled(retention_policy):
    # Check if 'policy_enabled' key exists in the 'retention'
    if 'policy_enabled' not in retention_policy:
        print("policy_enabled info missed.")
        return False

    # Check if 'policy_enabled' value is either 'true' or 'false'
    if retention_policy['policy_enabled'] not in [True, False]:
        print(f"policy_enabled is not Boolean {retention_policy['policy_enabled']}")
        return False

def check_policy_params(retention_policy):
    # Check if 'policy_params' key exists in the 'retention'
    if 'policy_params' in retention_policy:
        policy_params = retention_policy['policy_params']

        # Check if policy_params' values are all string
        for key, value in policy_params.items():
            if not isinstance(value, str):
                print(f'Key {key} should have a string value, but actual value is {value}, whose type is {type(value)}')
                return False

def valid_schema(retention):
    schema = Schema({'policy_ref': str,
                    'policy_enabled': bool,
                    'policy_params': dict})
    validated = schema.validate(retention)
    return validated

def verify_validate_policies(retention_policy):
    policy_ref_list = ['ret_2_2']
    plicy_apply_rules = {
        "user_country": "tax_region"
    }
    
    policy_ref = retention_policy['policy_ref']
    if policy_ref not in policy_ref_list:
        return False
    policy_params = retention_policy['policy_params']
    for key, value in policy_params.items():
        if key not in plicy_apply_rules or plicy_apply_rules[key] != value:
            return False

# Load YAML file
with open('example.yml', 'r') as file:
    try:
        data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        exit(1)

# Validate the YAML data
if ci_check(data):
    print("YAML file is valid.")
else:
    print("YAML file is invalid.")
