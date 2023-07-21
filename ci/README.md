# CI check for data retention project

[Design Doc](https://docs.google.com/document/d/1dvAIoaQ-OOYhSLUHVdfLbYFcqQOYTPswzo0m9O3CNek/edit)

[Specification for a unified dbt metadata tagging framework](https://docs.google.com/document/d/1mOTgiVXHO-8KuOHSrMTLBMygzEIhMJu89YzwCnGfdcc/edit)


## Template

```yml
version: 2

models:
  - name: <model-name>                        # required
    config:
      meta:
        canva:
          retention:
            has_retention_policy: true | false    # required
            ## ?? did we miss something here
            ## e.g. retention_ploicy:
            - policy_ref: <string>                # required
              policy_enabled: true | false        # required
              deletion_exception: true | false    # optional
              time_column: <string>               # optional

              # Policy specific parameters. The below would be required based on the policy set via policy_ref. 
              # These specify the columns in the table that will be used to check if deletion needs to occur. 

              policy_params:                  # optional (required based on policy) 

                # 1.1 - no policy specific params
              
                # 2.1 - no policy specific params

                # 2.2
                user_country: <string>                # required
                tax_date: <string>                    # required
                accounting_date: <string>             # required

                # 3.1
                candidate_country: <string>           # required
                outcome: <string>                     # required

                # 3.2
                outcome: <string>                     # required

                # 3.3
                end_date: <string>                    # required
                outcome: <string>                     # required

                # 3.4
                location: <string>                    # required
                outcome: <string>                     # required

                # 3.5
                end_date: <string>                    # required
              
                # 3.6 - no policy specific params
              
                # 3.7
                end_date: <string>                    # required

                # 3.8
                end_date: <string>                    # required
                cause: <string>                       # required

                # 4.1
                interest_expiration_date: <string>    # required
                financial_year_end_date: <string>     # required

                # 4.2 - no policy specific params
              
                # 4.3
                location: <string>                    # required
              
                # 4.4 - no policy specific params
              
                # 4.5 - no policy specific params

                # 4.6 
                account_closure_date: <string>        # required
              
                # 4.7 - no policy specific params

                # 4.8
                termination_date: <string>            # required
              
                # 4.9
                termination_date: <string>            # required
              
                # 4.10
                termination_date: <string>            # required
              
                # 4.11 - no policy specific params
              
                # 4.12 - no policy specific params

                # 5.1 
                user_type: <string>                   # required
                account_status: <string>              # required

                # 5.2
                user_type: <string>                   # required
                account_status: <string>              # required
                account_type: <string>                # required
                last_login: <string>                  # required
                notice_sent: <string>                 # required
                notice_sent_date: <string>            # required
            
            - policy_ref: ...
```

Explanation:

- meta.canva.retention
  - has_retention_policy - Whether the table falls under a retention policy.
  - policy_ref - Policy ref number prefixed with “ret_”.
  - policy_enabled - Whether the policy is enabled. 
  - deletion_exception - Whether there is an exception on this table for deletion.  
  - time_column - Time column used to determine if row is within the retention period. For some policies, policy specific columns may be used instead.
  - <identifier> - Zero or more policy specific parameters that specify the columns in the table that will be used to check if deletion needs to occur based on the retention conditions.

### Example


```yml
version: 2

models:
  - name: financial_records
    config:
      meta:
        canva:
          retention:
            has_retention_policy: true
            - policy_ref: “ret_2_2”
              policy_enabled: true
              policy_params:
                user_country: “tax_region”                   
                tax_date: “tax_period”                   
                accounting_date: “accounting_period”
```
