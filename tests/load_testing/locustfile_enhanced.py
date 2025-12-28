"""
Enhanced Locust Load Testing Suite for AI Platform API
Tests various endpoints under load to identify performance bottlenecks
"""

import os
import json
import time
import random
from locust import HttpUser, task, between, events, FastHttpUser
from locust.clients import ResponseContextManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_TOKEN = os.getenv('API_TOKEN', 'test_token')
TEST_MODE = os.getenv('TEST_MODE', 'advanced')  # basic, intermediate, advanced

# Test data
OPTIMIZATION_PROBLEMS = [
    {
        "problem_type": "TSP",
        "problem_data": {
            "cities": 10,
            "coordinates": [[i, i+1] for i in range(10)]
        },
        "parameters": {
            "optimizer": "VQE",
            "iterations": 500
        }
    },
    {
        "problem_type": "MAXCUT",
        "problem_data": {
            "graph_size": 20,
            "edges": [[i, (i+1) % 20] for i in range(20)]
        },
        "parameters": {
            "optimizer": "QAOA",
            "iterations": 300
        }
    },
    {
        "problem_type": "QUBO",
        "problem_data": {
            "matrix_size": 15,
            "qubo_matrix": [[random.random() for _ in range(15)] for _ in range(15)]
        },
        "parameters": {
            "optimizer": "Annealing",
            "iterations": 1000
        }
    }
]

VISION_ANALYSIS_TYPES = ["DETECTION", "CLASSIFICATION", "SEGMENTATION"]
VISION_MODELS = ["yolo", "resnet", "vit", "efficientnet"]

PROJECT_NAMES = [f"Project_{i}" for i in range(1000)]
MODEL_NAMES = ["bert-base", "gpt2", "vit-base", "resnet50", "efficientnet-b0"]


class BaseUser(FastHttpUser):
    """Base user class with common setup"""
    
    wait_time = between(1, 3)
    abstract = True
    
    def on_start(self):
        """Initialize test user"""
        self.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.user_id = f"test_user_{random.randint(10000, 99999)}"
        self.project_ids = []
        self.optimization_job_ids = []
        self.vision_job_ids = []
        self.session_token = None
        
        # Authenticate user
        self.authenticate()
        
    def authenticate(self):
        """Authenticate user and get session token"""
        # In a real implementation, this would authenticate with the API
        self.session_token = f"session_token_{self.user_id}"
        self.headers['Authorization'] = f'Bearer {self.session_token}'
        
    def on_stop(self):
        """Cleanup after test"""
        logger.info(f"Test user {self.user_id} finished")
        
        # Clean up created resources
        for project_id in self.project_ids:
            try:
                self.client.delete(f'/api/v1/projects/{project_id}', headers=self.headers)
            except:
                pass  # Ignore cleanup errors


class HealthCheckUser(BaseUser):
    """Users performing health check operations"""
    
    wait_time = between(0.1, 1)
    weight = 3
    
    @task(100)
    def health_check(self):
        """Health check endpoint - high frequency"""
        with self.client.get('/api/v1/health', headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(50)
    def status_check(self):
        """Status endpoint - medium frequency"""
        with self.client.get('/api/v1/status', headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'status' in data:
                        response.success()
                    else:
                        response.failure("Missing status field")
                except:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status: {response.status_code}")


class OptimizationUser(BaseUser):
    """Users submitting and monitoring optimization jobs"""
    
    wait_time = between(2, 5)
    weight = 2
    
    @task(40)
    def submit_optimization(self):
        """Submit optimization job"""
        problem = random.choice(OPTIMIZATION_PROBLEMS)
        
        with self.client.post(
            '/api/v1/optimize',
            json=problem,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 202:
                try:
                    data = response.json()
                    job_id = data.get('job_id')
                    if job_id:
                        self.optimization_job_ids.append(job_id)
                        response.success()
                    else:
                        response.failure("Missing job_id in response")
                except:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(30)
    def get_optimization_status(self):
        """Get optimization job status"""
        if not self.optimization_job_ids:
            return
            
        job_id = random.choice(self.optimization_job_ids)
        
        with self.client.get(
            f'/api/v1/optimize/{job_id}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Job completed and removed, remove from tracking
                if job_id in self.optimization_job_ids:
                    self.optimization_job_ids.remove(job_id)
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(10)
    def list_optimization_jobs(self):
        """List optimization jobs"""
        with self.client.get(
            '/api/v1/optimize?limit=50',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(5)
    def cancel_optimization(self):
        """Cancel optimization job"""
        if not self.optimization_job_ids:
            return
            
        job_id = self.optimization_job_ids.pop()
        
        with self.client.post(
            f'/api/v1/optimize/{job_id}/cancel',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 204, 404]:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")


class VisionUser(BaseUser):
    """Users submitting vision analysis jobs"""
    
    wait_time = between(3, 7)
    weight = 2
    
    @task(30)
    def submit_vision_analysis(self):
        """Submit vision analysis job"""
        # Use base64 encoded dummy image for testing
        dummy_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        payload = {
            "image": dummy_image,
            "analysis_type": random.choice(VISION_ANALYSIS_TYPES),
            "models": random.sample(VISION_MODELS, k=random.randint(1, 3))
        }
        
        with self.client.post(
            '/api/v1/vision/analyze',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 202:
                try:
                    data = response.json()
                    job_id = data.get('job_id')
                    if job_id:
                        self.vision_job_ids.append(job_id)
                        response.success()
                    else:
                        response.failure("Missing job_id in response")
                except:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(20)
    def get_vision_status(self):
        """Get vision analysis status"""
        if not self.vision_job_ids:
            return
            
        job_id = random.choice(self.vision_job_ids)
        
        with self.client.get(
            f'/api/v1/vision/analyze/{job_id}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Job completed and removed, remove from tracking
                if job_id in self.vision_job_ids:
                    self.vision_job_ids.remove(job_id)
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(5)
    def list_vision_jobs(self):
        """List vision analysis jobs"""
        with self.client.get(
            '/api/v1/vision/analyze?limit=50',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")


class ProjectManagementUser(BaseUser):
    """Users managing projects"""
    
    wait_time = between(2, 4)
    weight = 1
    
    @task(25)
    def list_projects(self):
        """List user projects"""
        with self.client.get(
            '/api/v1/projects?limit=20&offset=0',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'projects' in data:
                        response.success()
                    else:
                        response.failure("Missing projects field")
                except:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(20)
    def create_project(self):
        """Create new project"""
        payload = {
            "name": f"{random.choice(PROJECT_NAMES)}_{random.randint(100, 999)}",
            "description": "Load test project",
            "visibility": random.choice(["PRIVATE", "PUBLIC"])
        }
        
        with self.client.post(
            '/api/v1/projects',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                try:
                    data = response.json()
                    project_id = data.get('project_id')
                    if project_id:
                        self.project_ids.append(project_id)
                        response.success()
                    else:
                        response.failure("Missing project_id in response")
                except:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(15)
    def update_project(self):
        """Update project"""
        if not self.project_ids:
            return
            
        project_id = random.choice(self.project_ids)
        
        payload = {
            "name": f"Updated_{random.choice(PROJECT_NAMES)}_{random.randint(100, 999)}",
            "description": "Updated description"
        }
        
        with self.client.put(
            f'/api/v1/projects/{project_id}',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(5)
    def delete_project(self):
        """Delete project"""
        if not self.project_ids:
            return
            
        project_id = self.project_ids.pop()
        
        with self.client.delete(
            f'/api/v1/projects/{project_id}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 204, 404]:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")


class InferenceUser(BaseUser):
    """Users running inference"""
    
    wait_time = between(1, 3)
    weight = 3
    
    @task(35)
    def run_inference(self):
        """Run inference on model"""
        model = random.choice(MODEL_NAMES)
        
        payload = {
            "model": model,
            "input": {
                "text": f"This is a test input for inference {random.randint(1, 1000)}"
            }
        }
        
        with self.client.post(
            '/api/v1/infer/predict',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(25)
    def list_models(self):
        """List available models"""
        with self.client.get(
            '/api/v1/models',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(10)
    def get_model_info(self):
        """Get model information"""
        model = random.choice(MODEL_NAMES)
        
        with self.client.get(
            f'/api/v1/models/{model}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # Model not found is acceptable
            else:
                response.failure(f"Status: {response.status_code}")


class GraphQLUser(BaseUser):
    """Users making GraphQL queries"""
    
    wait_time = between(0.5, 2)
    weight = 4
    
    @task(50)
    def graphql_health_query(self):
        """GraphQL health query"""
        payload = {
            "query": "{ health { status uptime } }"
        }
        
        with self.client.post(
            '/graphql',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(30)
    def graphql_projects_query(self):
        """GraphQL projects query"""
        payload = {
            "query": """
                query {
                    projects(first: 10) {
                        edges {
                            node {
                                id
                                name
                                createdAt
                            }
                        }
                    }
                }
            """
        }
        
        with self.client.post(
            '/graphql',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(20)
    def graphql_optimization_query(self):
        """GraphQL optimization jobs query"""
        payload = {
            "query": """
                query {
                    optimizationJobs(first: 5) {
                        edges {
                            node {
                                id
                                status
                                createdAt
                                problemType
                            }
                        }
                    }
                }
            """
        }
        
        with self.client.post(
            '/graphql',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")


class StressTestUser(BaseUser):
    """User for stress testing - rapid requests"""
    
    wait_time = between(0.05, 0.2)
    weight = 1
    
    @task(100)
    def rapid_health_checks(self):
        """Rapid health checks for stress testing"""
        with self.client.get('/api/v1/health', headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(50)
    def rapid_status_checks(self):
        """Rapid status checks for stress testing"""
        with self.client.get('/api/v1/status', headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")


class MixedLoadUser(BaseUser):
    """User that performs mixed operations"""
    
    wait_time = between(1, 3)
    weight = 2
    
    @task(20)
    def mixed_workflow_1(self):
        """Mixed workflow: Create project, run optimization, check status"""
        # Create project
        project_id = self._create_project()
        if not project_id:
            return
            
        # Submit optimization job
        job_id = self._submit_optimization()
        if not job_id:
            return
            
        # Check job status multiple times
        for _ in range(3):
            self._check_optimization_status(job_id)
            time.sleep(0.5)
    
    @task(15)
    def mixed_workflow_2(self):
        """Mixed workflow: Create project, upload image, run analysis"""
        # Create project
        project_id = self._create_project()
        if not project_id:
            return
            
        # Submit vision analysis
        job_id = self._submit_vision_analysis()
        if not job_id:
            return
            
        # Check job status multiple times
        for _ in range(2):
            self._check_vision_status(job_id)
            time.sleep(1)
    
    @task(10)
    def mixed_workflow_3(self):
        """Mixed workflow: List projects, run inference, check health"""
        # List projects
        self._list_projects()
        
        # Run inference
        self._run_inference()
        
        # Check health
        self._check_health()
    
    def _create_project(self):
        """Helper to create a project"""
        payload = {
            "name": f"Workflow_Project_{random.randint(1000, 9999)}",
            "description": "Workflow test project",
            "visibility": "PRIVATE"
        }
        
        with self.client.post(
            '/api/v1/projects',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                try:
                    data = response.json()
                    project_id = data.get('project_id')
                    if project_id:
                        self.project_ids.append(project_id)
                        return project_id
                except:
                    pass
            return None
    
    def _submit_optimization(self):
        """Helper to submit optimization job"""
        problem = random.choice(OPTIMIZATION_PROBLEMS)
        
        with self.client.post(
            '/api/v1/optimize',
            json=problem,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 202:
                try:
                    data = response.json()
                    job_id = data.get('job_id')
                    if job_id:
                        self.optimization_job_ids.append(job_id)
                        return job_id
                except:
                    pass
            return None
    
    def _check_optimization_status(self, job_id):
        """Helper to check optimization job status"""
        with self.client.get(
            f'/api/v1/optimize/{job_id}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code not in [200, 404]:
                response.failure(f"Status: {response.status_code}")
    
    def _submit_vision_analysis(self):
        """Helper to submit vision analysis"""
        dummy_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        payload = {
            "image": dummy_image,
            "analysis_type": random.choice(VISION_ANALYSIS_TYPES),
            "models": random.sample(VISION_MODELS, k=2)
        }
        
        with self.client.post(
            '/api/v1/vision/analyze',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 202:
                try:
                    data = response.json()
                    job_id = data.get('job_id')
                    if job_id:
                        self.vision_job_ids.append(job_id)
                        return job_id
                except:
                    pass
            return None
    
    def _check_vision_status(self, job_id):
        """Helper to check vision analysis status"""
        with self.client.get(
            f'/api/v1/vision/analyze/{job_id}',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code not in [200, 404]:
                response.failure(f"Status: {response.status_code}")
    
    def _list_projects(self):
        """Helper to list projects"""
        with self.client.get(
            '/api/v1/projects?limit=10',
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status: {response.status_code}")
    
    def _run_inference(self):
        """Helper to run inference"""
        model = random.choice(MODEL_NAMES[:3])  # Use smaller models for mixed workflow
        
        payload = {
            "model": model,
            "input": {
                "text": f"Mixed workflow inference {random.randint(1, 100)}"
            }
        }
        
        with self.client.post(
            '/api/v1/infer/predict',
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status: {response.status_code}")
    
    def _check_health(self):
        """Helper to check health"""
        with self.client.get('/api/v1/health', headers=self.headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status: {response.status_code}")


# Event handlers for monitoring
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info(f"Load test started: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Load test finished")
    
    # Print statistics
    if hasattr(environment.stats, 'total'):
        logger.info(f"Total requests: {environment.stats.total.num_requests}")
        logger.info(f"Total failures: {environment.stats.total.num_failures}")
        logger.info(f"Average response time: {environment.stats.total.avg_response_time}ms")


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    logger.info("Test quitting")


# Default setup
if __name__ == "__main__":
    # Run with: locust -f locustfile_enhanced.py --host=http://localhost:8000
    pass