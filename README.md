(Copy everything from To: Tushar Awasthi down to the bottom)Markdown# 🚀 VIS_APP — Vision Intelligence System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green) ![Docker](https://img.shields.io/badge/Docker-Container-blue) ![AWS](https://img.shields.io/badge/Cloud-AWS-orange) ![MLOps](https://img.shields.io/badge/Focus-MLOps-purple)

**VIS_APP** is a cloud-native, production-oriented MLOps platform designed to manage the entire lifecycle of computer vision model training—from dataset ingestion to cloud deployment.

Unlike consumer-facing applications, VIS_APP is an **internal ML platform** engineered to demonstrate real-world system design. It facilitates dataset upload, validation, preprocessing (XML → YOLO), asynchronous training, experiment tracking, and artifact management via a stateless, containerized architecture.

---

## 🏗 System Architecture

VIS_APP follows a linear MLOps pipeline designed for reproducibility and scalability:

```mermaid
graph TD
    A["User Upload ZIP"] -->|API Request| B["FastAPI Service"]
    B --> C{"Data Validation"}
    C -->|Pass| D["Transformation XML to YOLO"]
    D --> E["Metadata and Fingerprinting"]
    E --> F["Async YOLO Training"]
    F --> G["Experiment Tracking MLflow"]
    G --> H["Artifact Storage AWS S3"]
    H --> I["Model Versioning"]
    I --> J["Docker Container"]
    J --> K["Deployment AWS ECR to EC2"]
🔑 Key Capabilities1. Data Engineering PipelineJob Isolation: Unique job_id generation for every upload to ensure data isolation.Validation & Integrity: Automated checks for corrupt files, empty images, and XML schema validation.Transformation: Automated conversion of Pascal VOC (XML) annotations to YOLO format with bounding box normalization.Data Lineage: Generation of immutable dataset_metadata.json (class distribution, resolution stats, and dataset hash).2. Machine Learning Operations (MLOps)Asynchronous Training: Non-blocking YOLO model training via background tasks.Experiment Tracking: Integration with MLflow to log parameters, metrics, and artifacts.Model Versioning: Automatic version control (v1, v2, v3...) to prevent overwrites and enable rollback.Cloud Artifact Storage: All artifacts (best.pt, metrics.json, data.yaml) are stored securely in AWS S3.3. DevOps & Cloud InfrastructureContainerization: Fully Dockerized application with explicit OpenCV runtime dependencies.CI/CD: Automated pipeline via GitHub Actions to build and push images to AWS ECR.Cloud Deployment: Stateless deployment on AWS EC2 using IAM Roles for secure access (no hardcoded credentials).🛠 Tech StackFramework: FastAPI (Python)Computer Vision: OpenCV, YOLOv8 (Ultralytics)Tracking & Logging: MLflowContainerization: DockerCI/CD: GitHub ActionsCloud Provider: AWS (S3, ECR, EC2, IAM)📂 Project StructureBashVIS_APP/
├── app/
│   └── main.py                # FastAPI Entrypoint & Routes
├── src/
│   ├── components/
│   │   ├── data_validation.py # Integrity checks & Schema validation
│   │   ├── data_transformation.py # XML to YOLO conversion
│   │   └── model_trainer.py   # Async YOLO training logic
│   ├── utils/
│   │   ├── dataset_metadata.py # Statistics & Fingerprinting
│   │   └── s3_utils.py        # AWS S3 Interactions
│   └── constants.py           # Centralized Configuration
├── data/
│   └── uploads/               # Local Job-isolated temporary storage
├── .github/workflows/
│   └── ecr.yml                # CI/CD Pipeline Configuration
├── Dockerfile                 # Container definition
└── requirements.txt           # Python dependencies
🔁 Complete MLOps LifecycleVIS_APP demonstrates an end-to-end implementation across 14 distinct phases:Foundation: Modular, config-driven code structure.Ingestion: API-based ZIP upload with job isolation.Validation: Integrity checks to prevent silent model degradation.Transformation: Normalizing bounding boxes and generating data.yaml.Metadata: Calculating class statistics and hashing for lineage.Async Training: Configurable epochs, batch size, and image size.Tracking: MLflow integration for reproducibility.Versioning: Safe experimentation with distinct version IDs.Storage: S3 as the single source of truth for artifacts.Serving: APIs to download trained models and metadata.Containerization: Environment consistency via Docker.CI/CD: Automated build/push to AWS ECR.Deployment: Stateless execution on AWS EC2.Verification: Runtime validation of APIs and S3 connectivity.🔌 API ReferenceThe platform is designed to be consumed programmatically. Below are the primary endpoints:MethodEndpointDescriptionPOST/upload-datasetUploads dataset (ZIP), validates, transforms, and returns job_id.POST/train-async/{job_id}Triggers asynchronous YOLO training for a specific job.GET/download/model/{job_id}Retrieves the latest trained model (best.pt) from S3.GET/dataset/metadata/{job_id}Fetches dataset statistics and lineage info.🔐 Security & Best PracticesIAM Roles: Used instead of hardcoded AWS keys to manage permissions securely.Statelessness: The container does not rely on local storage for persistence; it relies on S3.Immutability: Dataset metadata and trained model versions are immutable to ensure historical accuracy.🎯 Project GoalVIS_APP is not a tutorial project. It is a demonstration of Systems Engineering applied to AI. It highlights the ability to:Design modular, maintainable software architecture.Implement robust data pipelines (Data Engineering).Manage cloud infrastructure and deployments (DevOps).Oversee the full lifecycle of a machine learning model (MLOps).📌 AuthorTushar AwasthiAI/ML Engineer | Computer Vision SpecialistFocused on building production-grade ML systems, scalable MLOps pipelines, and industrial automation solutions.