# Olliemeow

Olliemeow: Kubernetes namespace change reporter

## Operation

Olliemeow is prepared to be installed via Helm Chart directly into a kubernetes cluster.

Chart includes templates to create necessary access rights.

```
helm install olliemeow chart/olliemeow -n [namespace_name] --set configMap.slack_url=[slack_hook_url]
```
