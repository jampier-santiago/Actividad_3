# k8s-demo — Microservicio FastAPI con K8s, Helm, ArgoCD y GitHub Actions

Microservicio en Python (FastAPI) desplegado en Kubernetes local con Minikube, gestionado con Helm y ArgoCD, y automatizado con un pipeline CI/CD en GitHub Actions.

---

## Stack

- **Python 3.11 + FastAPI** — microservicio
- **Docker** — contenedorización
- **Minikube** — clúster Kubernetes local
- **Helm** — gestión de manifests de K8s
- **ArgoCD** — despliegue GitOps
- **GitHub Actions** — pipeline CI/CD
- **Docker Hub** — registry de imágenes

---

## Estructura del proyecto

```
.
├── app/
│   ├── main.py               # Código del microservicio
│   └── requirements.txt      # Dependencias Python
├── Dockerfile                # Imagen del microservicio
├── helm/
│   └── microservicio/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           └── service.yaml
├── argocd/
│   └── application.yaml      # Definición de la app en ArgoCD
└── .github/
    └── workflows/
        └── ci.yml            # Pipeline CI/CD
```

---

## Prerrequisitos

Instalar las siguientes herramientas antes de continuar:

```bash
brew install minikube kubectl helm argocd
```

También necesitas tener instalado **Docker Desktop** y que esté corriendo.

---

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/jampier-santiago/Actividad_3.git
cd Actividad_3
```

### 2. Crear entorno virtual de Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

### 3. Levantar Minikube

```bash
minikube start --driver=docker
```

Verificar que esté corriendo:

```bash
minikube status
```

---

## Correr el microservicio localmente

```bash
docker build -t k8s-demo:local .
docker run -p 8000:8000 k8s-demo:local
```

Abrir en el browser: `http://localhost:8000/docs`

---

## Instalar ArgoCD en Minikube

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Esperar a que los pods estén listos
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s
```

Obtener la contraseña inicial de ArgoCD:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Acceder a la UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Abrir `https://localhost:8080` — usuario: `admin`, contraseña: la del paso anterior.

---

## Desplegar la aplicación con ArgoCD

```bash
kubectl apply -f argocd/application.yaml
```

ArgoCD detectará automáticamente los Helm charts del repo y desplegará el microservicio en Minikube. Verificar en la UI que el estado sea **Healthy** y **Synced**.

---

## Verificar el despliegue

```bash
kubectl get pods -n default
```

Exponer el servicio localmente:

```bash
kubectl port-forward svc/k8s-demo 8888:8000 -n default
```

Abrir en el browser: `http://localhost:8888/docs`

---

## Pipeline CI/CD (GitHub Actions)

El pipeline se dispara automáticamente con cada push a `master`. Realiza los siguientes pasos:

1. Build de la imagen Docker
2. Push a Docker Hub con dos tags: `latest` y el hash del commit
3. Actualiza el tag de la imagen en `helm/microservicio/values.yaml`
4. ArgoCD detecta el cambio y redespliegue automáticamente

## Endpoints del microservicio

| Método | Ruta      | Descripción       |
| ------ | --------- | ----------------- |
| GET    | `/`       | Hello world       |
| GET    | `/health` | Health check      |
| GET    | `/info`   | Info del servicio |
| GET    | `/docs`   | Swagger UI        |


# PRUEBAS
Este es un cambio para probar