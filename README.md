# KEDA + Redis Worker Autoscaling Example

Este repositorio contiene un ejemplo completo de cómo implementar **KEDA (Kubernetes-based Event Driven Autoscaler)** para escalar automáticamente un **worker en Python** según la longitud de una lista en **Redis**.

## 📦 Componentes del ejemplo

- `redis-deployment.yaml`: despliega Redis y su servicio.
- `redis-worker-script-configmap.yaml`: define el script en Python que escucha la cola Redis.
- `redis-worker-deployment.yaml`: define el deployment del worker (escalado por KEDA).
- `keda-scaledobject.yaml`: define el `ScaledObject` de KEDA que vincula Redis con el worker.
- `namespaces.yaml`: crea el namespace `keda`.
- `kustomization.yaml`: orquesta los recursos.

## 🚀 Requisitos

- Kubernetes cluster (local o en la nube)
- `kubectl` configurado
- Acceso a internet para descargar manifiestos
- [KEDA instalado](https://keda.sh/docs/)

## 🛠 Instalación paso a paso

### 1. Instalar KEDA en tu clúster

```bash
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.17.2/keda-2.17.2.yaml
```

### 2. Aplicar los manifiestos del proyecto

```bash
kubectl apply -f namespaces.yaml
kubectl apply -f kustomization.yaml
kubectl apply -f redis.yaml
kubectl apply -f redis-worker.yaml
kubectl apply -f keda-scaledobject.yaml
```

> 📌 Asegúrate de estar en el contexto y namespace correctos si usas `kubens`.

## 💡 ¿Cómo funciona?

- Un **Deployment Redis** ejecuta una cola (`list`) llamada `myqueue`.
- El **worker en Python** (dentro de un contenedor) escucha tareas de esa cola.
- **KEDA** observa la longitud de la lista `myqueue` en Redis.
- Cuando hay más de 5 elementos en la cola, KEDA escalará el deployment `redis-worker` hasta 5 réplicas.
- Si la cola se vacía, las réplicas bajan nuevamente a 0.

## 🧪 Pruebas y validación

### Enviar tareas a Redis

Abre un shell en el pod de Redis:

```bash
kubectl exec -it deploy/redis -- sh
```

Y dentro, ejecuta este bucle para enviar tareas en lotes de 40:

```bash
i=1; while true; do echo "Enviando tareas del $i al $((i+39))"; for j in $(seq $i $((i+39))); do redis-cli -h redis rpush myqueue "task$j"; done; i=$((i+40)); sleep 10; done
```

### Ver los pods escalar

```bash
kubectl get pods
```

Deberías ver cómo el deployment `redis-worker` escala hacia arriba y luego hacia abajo automáticamente.

## 📂 Estructura del proyecto

```
.
├── charts/                          # (opcional, si usas Helm)
├── kustomization.yaml
├── namespaces.yaml
├── redis-deployment.yaml
├── redis-worker-deployment.yaml
├── redis-worker-script-configmap.yaml
├── keda-scaledobject.yaml
```

## 📖 Recursos útiles

- [KEDA Docs](https://keda.sh/)
- [Redis CLI](https://redis.io/docs/ui/cli/)
- [Kustomize](https://kustomize.io/)

---

Este ejemplo es ideal para entender cómo **KEDA puede escalar cargas de trabajo según eventos externos**, como la longitud de una lista en Redis. 🎯
