#!/bin/bash

helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install --create-namespace --wait grafana grafana/grafana --namespace=monitoring --values manifests/grafana-values.yaml



# NAME: grafana
# LAST DEPLOYED: Sun Jul 13 12:00:38 2025
# NAMESPACE: monitoring
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None
# NOTES:
# 1. Get your 'admin' user password by running:

#    kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


# 2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

#    grafana.monitoring.svc.cluster.local

#    Get the Grafana URL to visit by running these commands in the same shell:
#      export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
#      kubectl --namespace monitoring port-forward $POD_NAME 3000

# 3. Login with the password from step 1 and the username: admin