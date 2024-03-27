#!/bin/bash

echo -e "================================================="
echo -e "### Service Deployment : Datadrift Test Model ###"
echo -e "=================================================\n\n"

files=($HOME/.kube/*)
echo "Please select number from the cluster name list"
cluster_indices=()
cluster_index=0

for i in "${!files[@]}"; do
  if [[ ! "${files[$i]}" == *"/cache" ]]; then
    echo "$cluster_index. $(basename ${files[$i]})"
    cluster_indices+=("$i")
    ((cluster_index++))
  fi
done

while true; do
  read -p "> " choice

  if [ "$choice" -ge 0 ] && [ "$choice" -lt ${#cluster_indices[@]} ]; then
    selected_file=${files[ ${cluster_indices[$choice]} ]}
    selected_cluster_name=$(basename $selected_file)
    echo -e "[Selected Cluster]: $selected_cluster_name\n"
    export KUBECONFIG=$HOME/.kube/"$selected_cluster_name"
    break
  else
    echo -e "[Wrong Input]: Please try again\n"
  fi
done

read -p "base image path ( dockerhub ) : " BASE_IMAGE_PATH
read -p "target cpu arch ( arm64 / amd64 ) : " CPU_ARCH

while true; do
  read -p "Number of replicas: " count_replicas
  if [ -z "$count_replicas" ]; then
    count_replicas=1
    break
  elif [[ "$count_replicas" =~ ^[0-9]+$ ]] && ! [[ "$count_replicas" -le 0 ]]; then
    break
  else
    echo "(Wrong Input. Please try again.)"
  fi
done

cat << EOF > /tmp/manifest.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datadrift-deployment-$CPU_ARCH
  labels:
    app: datadrift-pod-$CPU_ARCH
spec:
  replicas: $count_replicas
  selector:
    matchLabels:
      app: datadrift-pod-$CPU_ARCH
  template:
    metadata:
      labels:
        app: datadrift-pod-$CPU_ARCH
    spec:
      containers:
      - name: datadrift-test
        image: $BASE_IMAGE_PATH
        imagePullPolicy: IfNotPresent
        command: ["python", "app.py"]
        ports:
        - containerPort: 7860
      nodeSelector:
        kubernetes.io/arch: $CPU_ARCH
---
apiVersion: v1
kind: Service
metadata:
  name: datadrift-app-$CPU_ARCH
  labels:
    app: datadrift-pod-$CPU_ARCH
spec:
  type: LoadBalancer
  ports:
  - port: 7860
  selector:
    app: datadrift-pod-$CPU_ARCH

EOF

kubectl apply -f /tmp/manifest.yaml