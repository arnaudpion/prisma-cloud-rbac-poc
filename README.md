# prisma-cloud-rbac-poc
Python script leveraging Prisma Cloud REST API to create roles mapped to cloud accounts

### Prerequisites
First you need an Access Key in Prisma Cloud. Then you need to set up the following environment variables on your workstation :
 - **PC_PY_IDENTITY** : your Access Key in Prisma Cloud
 - **PC_PY_SECRET** : your Secret Key in Prisma Cloud
 - **PC_PY_URL** : Prisma Cloud API Endpoint - please refer to https://pan.dev/prisma-cloud/api/cspm/api-urls/

### Running the scripts
Please note that the scripts are provided 'as is' for testing/POC purpose, and are not production-grade.

**01_create_rbac_py**
 - Authenticates with Prisma Cloud
 - Lists Accounts onboarded in Prisma Cloud and starting with '*account_prefix*'
 - Creates a corresponding Account Group for each Account
 - Creates a Role with '*Account Group Admin*' permissions for each Account Group created
 - Outputs variables that you can use in *02_cleanup_rbac_py* to clean up

**02_cleanup_rbac_py**
 - You need to copy the output of *01_create_rbac_py* and paste it in this script
 - Authenticates with Prisma Cloud
 - Delete the Roles previously created 
 - Empty and delete the Account Groups previously created

### What next ?
Please feel free to check the Prisma Cloud Python SDK which offers more advanced scripts for production-grade automation : https://github.com/PaloAltoNetworks/prismacloud-api-python