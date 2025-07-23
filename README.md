# ⚙️ KEDA + Redis Worker Autoscaling Example

Este repositorio contiene un ejemplo práctico de cómo utilizar **KEDA (Kubernetes-based Event Driven Autoscaler)** para escalar automáticamente un **worker en Python** según la cantidad de tareas pendientes en una cola Redis (`list`).

---

## 📦 Componentes incluidos

- `redis.yaml`: despliega una instancia de Redis y su servicio.
- `redis-worker.yaml`: despliega el `Deployment` del worker Python.
- `keda-scaledobject.yaml`: define el `ScaledObject` de KEDA que escala el worker en función de la longitud de la cola Redis.
- `namespaces.yaml`: crea el namespace `keda`.
- `kustomization.yaml`: orquesta todos los recursos con Kustomize.
- `Dockerfile`: construye la imagen del worker Python.
- `worker.py`: script Python que escucha tareas desde Redis.

---

## 🚀 Requisitos

- Un clúster de Kubernetes (local con Minikube o en la nube)
- `kubectl` configurado y apuntando al clúster
- Acceso a internet
- [KEDA instalado](https://keda.sh/docs/)
- Docker para construir la imagen del worker

---

## 🛠 Instalación paso a paso

### 1. Instalar KEDA

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda   --version 2.17.2   --namespace keda   --create-namespace
```

### 2. 🐳 (Opcional) Construir tu propia imagen del worker

Si deseas modificar el script del `worker.py` y construir tu propia imagen, puedes usar el `Dockerfile` incluido:

```bash
docker build -t <tu-usuario>/redis-worker:latest .
docker push <tu-usuario>/redis-worker:latest
```

Luego modifica `redis-worker.yaml` para usar tu imagen personalizada.

💡 Por defecto, ya puedes usar la imagen preconstruida desde Docker Hub publicada por el autor de este ejemplo.

### 3. Aplicar los manifiestos con Kustomize

```bash
kubectl apply -k .
```

---

## 💡 ¿Cómo funciona?

- El **script `worker.py`** escucha tareas de una lista Redis (`myqueue`) usando `redis-py`.
- **KEDA** monitorea la longitud de esa lista.
- Si hay más de 5 tareas en la cola, KEDA escalará el deployment del worker hasta 5 réplicas.
- Cuando la cola se vacía, reduce el número de réplicas automáticamente a 0.

---

## 🧪 Pruebas y validación

### Enviar tareas a Redis

Ejecuta un shell en el pod de Redis:

```bash
kubectl exec -it deploy/redis -- sh
```

Desde ahí, usa este script para empujar tareas:

```bash
i=1; while true; do echo "Enviando tareas del $i al $((i+39))"; for j in $(seq $i $((i+39))); do redis-cli -h redis rpush myqueue "task$j"; done; i=$((i+40)); sleep 10; done
```

### Observar el escalado

```bash
kubectl get pods -n keda
```

Deberías ver cómo los pods `redis-worker` aumentan o disminuyen según la carga.

---

## 📂 Estructura del proyecto

```
.
├── Dockerfile                         # Imagen del worker
├── keda-scaledobject.yaml            # ScaledObject de KEDA
├── kustomization.yaml                # Orquestador de recursos
├── namespaces.yaml                   # Namespace para KEDA
├── redis.yaml                        # Redis deployment + service
├── redis-worker.yaml                 # Worker deployment
├── redis-worker-script-configmap.yaml # Script del worker como ConfigMap
├── worker.py                         # Código Python del worker
└── README.md
```

---

## 📖 Recursos útiles

- [KEDA Documentation](https://keda.sh/)
- [Redis CLI](https://redis.io/docs/ui/cli/)
- [Kustomize](https://kustomize.io/)
- [Docker](https://docs.docker.com/)

---

Este ejemplo es perfecto para aprender cómo escalar automáticamente cargas de trabajo en Kubernetes usando eventos de mensajería, como una cola en Redis. También puedes extender este patrón a otros sistemas como Kafka, RabbitMQ, Azure Queue, entre otros. ⚡️