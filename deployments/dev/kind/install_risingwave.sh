#!/bin/bash

helm repo add risingwavelabs https://risingwavelabs.github.io/helm-charts/ --force-update

helm repo update

helm upgrade --install --create-namespace --wait risingwave risingwavelabs/risingwave --namespace=risingwave -f manifests/risingwave-values.yaml 


#     kubectl -n risingwave get pods -l app.kubernetes.io/instance=risingwave

# Try accessing the SQL console with the following command:

#     kubectl -n risingwave port-forward svc/risingwave 4567:svc

# Keep the above command running and open a new terminal window to run the following command:

#     psql -h localhost -p 4567 -d dev -U root 

# For more advanced applications, refer to our documentation at: https://www.risingwave.dev

# IMPORTANT:
# The private key for the secret store is automatically generated and stored in a Kubernetes secret. Please back up the private key by running the following command:

#     kubectl -n risingwave get secret risingwave-secret-store -o jsonpath="{.data.privateKey}" | base64 --decode