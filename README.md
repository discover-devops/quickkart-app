# QuickKart App

Source code for the QuickKart microservices: product-service, user-service and order-service.

- Each service is a Python FastAPI app with its own Dockerfile and tests
- Jenkins builds, tests and pushes images to Amazon ECR
- Deployment is done by Argo CD from the quickkart-gitops repository
