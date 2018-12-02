# Infrastructure-as-a-Service (IaaS) Demo

This is a demo IaaS deployment created for a *Cloud Basics* presentation to the [Roanoke InfoSec Exchange](https://roanokeinfosec.com "RISE Blog"). It contains an Azure template to deploy a Ubuntu 18 image and perform the followoing actions via cloud-init script:

* update all packages
* install `python3-pip`
* perform `pip install flask`
* write out a simple Python Flask app to file
* start the dev Flask web server

The template was made for a specific demonstration and therefore doesn't necessarily follow best templating practices.

## Pre-requisites

Prior to deploying the template you must have the following:

* Azure subscription (free account eligible)
* SSH key pair
* *(optional)* Azure CLI

### Azure subscription

If you do not have an Azure subscription, you can sign up [here](https://azure.microsoft.com/en-us/free/ "Azure free account sign-up"). All demo templates were designed to limit cost - *I'm paying out-of-pocket myself*! The Azure free account will suffice to deploy the demonstration templates.

### SSH key pair

If you don't have an SSH key pair already, follow instructions below based on your OS.

[Windows SSH key pair generation using PuttyGen](https://www.ssh.com/ssh/putty/windows/puttygen "ssh.com")

[Linux SSH key pair generation](https://www.ssh.com/ssh/keygen/ "ssh.com")

### Azure CLI

I use the Azure CLI to deploy the templates in the demonstration, but they can also be deployed via the Azure Portal. If desired you can install the Azure CLI using [these instructions](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest "Microsoft Docs").

## Usage

The template deploys a small-instance (Standard B1) with Ubuntu Linux 18.04. The default user name should be left as *riseuser*. The simple Flask application included in the template is written to the home directory of *riseuser*. The template also assumes that the resource group **rg_rise-demo** has been created.

### Azure CLI Deployment

* [Sign in](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest "Microsoft Docs") to your Azure account

* Create the resource group for deployment

`az group create -l eastus2 -g rg_rise-demo`

*The resource group can be created in any region. It does not need to match the region of VM deployment, though this example uses East US 2.*

* Deploy the template; Replace *PUBLIC_KEY* with the contents of your SSH **public** key

`az group deployment create -g rg_rise-demo --template-uri https://raw.githubusercontent.com/edwinsummers/rise-cloud-basics/master/iaas/tem_iaas-demo.json --parameters "$(curl https://raw.githubusercontent.com/edwinsummers/rise-cloud-basics/master/iaas/parameters_iaas-demo.json)" --parameters adminPublicKey="$SSH_PUBLIC_KEY"`

*(Alternately, you can download the parameters file to your local disk, edit it as desired, and reference it by changing the parameters section as follows: `--parameters @parameters_iaas-demo.json`)*

Once deployment has completed, you can find the Public IP address using the following Azure CLI command. If you have multiple Public IP resources, look for the one named *riseiaasdemo-ip*.

`az network public-ip list --query "[].{name: name, address: ipAddress}"`

### Post-Deployment Testing / Usage

The deployment will take a few minutes to complete. The Azure CLI will return to prompt once the VM has been deployed. However, it will take a couple more minutes after the Azure CLI returns to prompt for the cloud-init script to finish running on the VM. This is because it updates all packages on the VM prior to installing and running the Flask app. You can view the cloud-init script logs by logging into the VM and running the following:

`sudo tail -f /var/log/cloud-init-output.log`

* Test the app

Once deployment is completed, you can test the simple Flask app by browsing to the VM's public IP, port 5000.

`http://<public_ip>:5000/`

Any string after the path `/foo/` will be repeated as text in the page body. Example:

`http://<public_ip>:5000/foo/try_this_text`

## Clean-Up

Upon completion of your testing, delete the resources to save costs. This can be done via the Azure Portal, or the Azure CLI using the following:

`az group delete -g rg_rise-demo`
