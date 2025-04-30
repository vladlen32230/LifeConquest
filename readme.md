Example of deploying application with kubernetes:

How to run:

1. Install minikube and kubectl for local deployment.
2. Create docker images (nginx server and fastapi backend)
    ```bash
    docker build -t lifeconquest/lifeconquest-server:latest api/v1/docker/server
    docker build -t lifeconquest/lifeconquest-backend:latest -f api/v1/docker/backend/Dockerfile api/v1
    ```
3. Install images into minikube environment
    ```bash
    minikube image load lifeconquest/lifeconquest-server:latest
    minikube image load lifeconquest/lifeconquest-backend:latest
    ```
4. Create postgresql cluster:
    ```bash
    helm repo add postgres-operator https://opensource.zalando.com/postgres-operator/charts/postgres-operator/
    helm install postgres-operator postgres-operator/postgres-operator
    ```
5. Run kubernetes resources:
    ```bash
    kubectl apply -f k8s/
    ```
6. Expose load balancer ip address:
    ```bash
    minikube tunnel
    ```
7. Get public ip address from 
    ```bash
    kubectl get services
    ``` 

    of a loadbalancer. Then paste this ip into /etc/hosts file:

    ```bash
    <ip> lifeconquest.ru
    ```
    
8. Go to http://lifeconquest.ru