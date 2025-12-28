# Enhanced Load Testing Guide

## Apache JMeter & Locust Configuration

---

## 1. Apache JMeter Setup & Execution

### 1.1 Installation

**Windows:**
```bash
# Download JMeter 5.5+
# https://jmeter.apache.org/download_jmeter.cgi

# Add to PATH
setx JMETER_HOME "C:\apache-jmeter-5.5"
setx PATH "%PATH%;%JMETER_HOME%\bin"

# Verify installation
jmeter --version
```

**Linux/Mac:**
```bash
# Using Homebrew (Mac)
brew install jmeter

# Or download manually
wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz
tar -xzf apache-jmeter-5.5.tgz
export PATH=$PATH:$(pwd)/apache-jmeter-5.5/bin

# Verify
jmeter -v
```

### 1.2 Running Load Tests

**Run JMeter test plan non-GUI mode (recommended for load testing):**

```bash
# Basic execution with enhanced test plan
jmeter -n -t ai_platform_load_test_enhanced.jmx \
        -l results_enhanced.jtl \
        -j jmeter_enhanced.log

# With custom parameters
jmeter -n -t ai_platform_load_test_enhanced.jmx \
        -l results_enhanced.jtl \
        -j jmeter_enhanced.log \
        -Jnum_threads=200 \
        -Jramp_up_time=120 \
        -Jloop_count=50 \
        -Jduration=600

# Generate HTML report
jmeter -n -t ai_platform_load_test_enhanced.jmx \
        -l results_enhanced.jtl \
        -o results_html_report_enhanced \
        -Jjmeter.reportgenerator.agg_prefix=results_enhanced_ \
        -Jjmeter.reportgenerator.overall_granularity=1000
```

**Parameters explained:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| -n | Non-GUI mode (faster) | |
| -t | Test plan file | ai_platform_load_test_enhanced.jmx |
| -l | Results file (JTL) | results_enhanced.jtl |
| -j | Log file | jmeter_enhanced.log |
| -J | Define variable | -Jnum_threads=200 |
| -o | Output directory for HTML report | results_html_report_enhanced |

### 1.3 Understanding JTL Results

**Sample results.jtl format:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testResults version="1.2">
  <httpSample t="234" it="0" ct="0" lt="234" 
              ct="1024" s="true" lb="GET /health" 
              rc="200" rm="OK" ts="1704067200000" 
              hn="localhost" by="1024" eby="0"/>
  <httpSample t="567" it="0" ct="0" lt="567" 
              ct="2048" s="true" lb="POST /optimize" 
              rc="202" rm="ACCEPTED" ts="1704067201000" 
              hn="localhost" by="2048" eby="0"/>
</testResults>
```

**Key fields:**

| Field | Meaning |
|-------|---------|
| t | Total response time (ms) |
| lt | Latency (time to first byte) |
| ct | Connect time |
| s | Success (true/false) |
| rc | Response code (200, 202, etc) |
| rm | Response message |
| by | Response bytes |
| eby | Response error bytes |

### 1.4 Analyzing Results

**Extract metrics from JTL:**

```bash
# Convert JTL to CSV
python3 << 'EOF'
import xml.etree.ElementTree as ET
import csv

tree = ET.parse('results_enhanced.jtl')
root = tree.getroot()

with open('results_enhanced.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'response_time', 'status', 'endpoint'])
    
    for sample in root.findall('httpSample'):
        writer.writerow([
            sample.get('ts'),
            sample.get('t'),
            sample.get('rc'),
            sample.get('lb')
        ])
EOF

# Analyze with Python
python3 << 'EOF'
import pandas as pd
import statistics

df = pd.read_csv('results_enhanced.csv')

# Overall statistics
print("=== Load Test Results ===")
print(f"Total requests: {len(df)}")
print(f"Successful: {(df['status'] == 200).sum() + (df['status'] == 202).sum()}")
print(f"Failed: {(df['status'] >= 400).sum()}")

# Response time analysis
response_times = df['response_time'].astype(float)
print(f"\nResponse Time (ms):")
print(f"  Min: {response_times.min():.2f}")
print(f"  Max: {response_times.max():.2f}")
print(f"  Mean: {response_times.mean():.2f}")
print(f"  Median: {response_times.median():.2f}")
print(f"  P95: {response_times.quantile(0.95):.2f}")
print(f"  P99: {response_times.quantile(0.99):.2f}")

# By endpoint
print("\n=== Results by Endpoint ===")
for endpoint in df['endpoint'].unique():
    times = df[df['endpoint'] == endpoint]['response_time'].astype(float)
    print(f"{endpoint}: {times.mean():.2f}ms (P95: {times.quantile(0.95):.2f}ms)")
EOF
```

### 1.5 Test Plan Customization

**Modify JMeter test plan via script:**

```bash
# Edit variables in test plan
sed -i 's/NUM_THREADS=100/NUM_THREADS=300/' ai_platform_load_test_enhanced.jmx
sed -i 's/RAMP_UP_TIME=120/RAMP_UP_TIME=180/' ai_platform_load_test_enhanced.jmx
sed -i 's/LOOP_COUNT=50/LOOP_COUNT=100/' ai_platform_load_test_enhanced.jmx

# Or use property files
cat > test_enhanced.properties << EOF
num_threads=300
ramp_up_time=180
loop_count=100
duration=900
base_url=http://prod-api.aiplatform.io
api_token=Bearer prod_token_xyz
EOF

jmeter -n -t ai_platform_load_test_enhanced.jmx \
        -q test_enhanced.properties \
        -l results_enhanced.jtl
```

---

## 2. Locust Setup & Execution

### 2.1 Installation

```bash
# Install Locust
pip install locust

# Install additional dependencies
pip install requests pandas matplotlib

# Verify installation
locust --version
```

### 2.2 Running Locust Tests

**Command-line execution:**

```bash
# Run with GUI using enhanced test file
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 100 \
        --spawn-rate 10 \
        --run-time 10m

# Run headless (non-GUI) with enhanced test file
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 200 \
        --spawn-rate 20 \
        --run-time 15m \
        --headless

# CSV output
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 150 \
        --spawn-rate 15 \
        --run-time 10m \
        --headless \
        --csv=load_test_results_enhanced

# HTML report
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 100 \
        --spawn-rate 10 \
        --run-time 5m \
        --headless \
        --html=report_enhanced.html
```

**Parameters explained:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| -f | Locust file | locustfile_enhanced.py |
| --host | Target API URL | http://localhost:8000 |
| --users | Number of concurrent users | 200 |
| --spawn-rate | Users per second | 20 |
| --run-time | Test duration | 10m, 1h, etc |
| --headless | Non-interactive mode | |
| --csv | Output CSV results | results_enhanced.csv |
| --html | Output HTML report | report_enhanced.html |

### 2.3 Distributed Load Testing with Locust

**Master-Slave setup for scaling:**

```bash
# Terminal 1: Start Locust master
locust -f locustfile_enhanced.py \
        --master \
        --host=http://api.aiplatform.io \
        --expect-workers=4

# Terminal 2-5: Start Locust workers (on different machines)
locust -f locustfile_enhanced.py \
        --worker \
        --master-host=master_ip:5557

# Access web UI on http://master_ip:8089
```

### 2.4 Custom Test Scenarios

**Create scenario-based test file:**

```python
# scenario_load_test_enhanced.py
import os
from locust import HttpUser, task, between, SequentialTaskSet
from random import choice, randint

class QuickScenario(SequentialTaskSet):
    """Fast scenario: health checks + quick status"""
    tasks = [
        ("health_check", 10),
        ("status_check", 1),
    ]

class StandardScenario(SequentialTaskSet):
    """Standard scenario: typical user behavior"""
    tasks = {
        "health_check": 5,
        "list_projects": 3,
        "submit_optimization": 1,
        "list_models": 2,
    }

class StressScenario(SequentialTaskSet):
    """Stress scenario: heavy load"""
    tasks = [
        ("rapid_requests", 20),
        ("large_payload", 1),
    ]

class TestUser(HttpUser):
    wait_time = between(0.5, 2)
    scenario = choice([QuickScenario, StandardScenario, StressScenario])
    
    @task
    def health_check(self):
        self.client.get("/api/v1/health")
```

### 2.5 Analyzing Locust Results

**CSV output format:**

```
Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,Min Response Time,Max Response Time,Average Content Size,Requests/s
GET,/api/v1/health,2000,0,50,55.2,20,500,512,40
POST,/api/v1/optimize,1000,2,200,215.4,150,800,2048,20
```

**Parse and visualize:**

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv('load_test_results_enhanced_stats.csv')

# Failure rate
df['Failure Rate %'] = (df['Failure Count'] / df['Request Count'] * 100).round(2)

# Plot response times
plt.figure(figsize=(15, 6))
plt.subplot(1, 3, 1)
plt.bar(df['Name'], df['Average Response Time'])
plt.title('Average Response Time by Endpoint')
plt.ylabel('Time (ms)')
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
plt.bar(df['Name'], df['Failure Rate %'], color='red')
plt.title('Failure Rate by Endpoint')
plt.ylabel('Failure Rate %')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
plt.bar(df['Name'], df['Requests/s'])
plt.title('Requests per Second by Endpoint')
plt.ylabel('RPS')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('load_test_results_enhanced.png')
```

---

## 3. Performance Baselines

### 3.1 Expected Performance Metrics

**Health Check Endpoint:**
- Target P95: < 50ms
- Target P99: < 100ms
- Error rate: < 0.01%

**Optimization Submission:**
- Target P95: < 300ms
- Target P99: < 600ms
- Error rate: < 0.1%

**GraphQL Queries:**
- Target P95: < 200ms
- Target P99: < 400ms
- Error rate: < 0.05%

**Vision Analysis:**
- Target P95: < 800ms (image processing)
- Target P99: < 1500ms
- Error rate: < 0.5%

**Inference Requests:**
- Target P95: < 150ms
- Target P99: < 300ms
- Error rate: < 0.1%

### 3.2 Capacity Planning

```python
# Calculate capacity from load test results
current_rps = 2000  # requests per second at P95 < 300ms
current_users = 200

# Target: 20,000 RPS with same P95
target_rps = 20000
required_servers = (target_rps / current_rps) * 1.5  # 50% safety margin

print(f"Current capacity: {current_rps} RPS with {current_users} users")
print(f"Required servers for {target_rps} RPS: {int(required_servers)}")
```

---

## 4. Continuous Load Testing

### 4.1 Scheduled Testing

```bash
#!/bin/bash
# daily_load_test_enhanced.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="load_test_results_enhanced_$TIMESTAMP"

mkdir -p $RESULTS_DIR

# Run daily baseline test with enhanced scenarios
locust -f locustfile_enhanced.py \
        --host=http://api.aiplatform.io \
        --users 500 \
        --spawn-rate 50 \
        --run-time 30m \
        --headless \
        --csv=$RESULTS_DIR/results_enhanced \
        --html=$RESULTS_DIR/report_enhanced.html

# Archive results
tar -czf $RESULTS_DIR.tar.gz $RESULTS_DIR/
gsutil cp $RESULTS_DIR.tar.gz gs://aiplatform-test-results/

# Cleanup
rm -rf $RESULTS_DIR
```

**Schedule with cron:**

```cron
# Run load test daily at 2 AM
0 2 * * * /home/ci/daily_load_test_enhanced.sh >> /var/log/load_test_enhanced.log 2>&1
```

### 4.2 GitHub Actions Integration

```yaml
name: Weekly Enhanced Load Test

on:
  schedule:
    - cron: '0 2 * * 0'  # Sunday 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install locust requests pandas
          # Install JMeter if needed
          wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz
          tar -xzf apache-jmeter-5.5.tgz
          echo "JMETER_HOME=$(pwd)/apache-jmeter-5.5" >> $GITHUB_ENV
          echo "$(pwd)/apache-jmeter-5.5/bin" >> $GITHUB_PATH
      
      - name: Run enhanced Locust load test
        run: |
          locust -f tests/load_testing/locustfile_enhanced.py \
                  --host=https://api.aiplatform.io \
                  --users 300 \
                  --spawn-rate 30 \
                  --run-time 20m \
                  --headless \
                  --csv=results_enhanced
      
      - name: Run enhanced JMeter load test
        run: |
          jmeter -n -t tests/load_testing/ai_platform_load_test_enhanced.jmx \
                  -l results_jmeter_enhanced.jtl \
                  -Jnum_threads=150 \
                  -Jduration=1200
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: enhanced-load-test-results
          path: |
            results_enhanced*
            results_jmeter_enhanced*
            report_enhanced.html
```

---

## 5. Advanced Testing Scenarios

### 5.1 Spike Testing

```bash
# Spike test with 1000 users in 30 seconds
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 1000 \
        --spawn-rate 33 \
        --run-time 5m \
        --headless \
        --csv=spike_test_results
```

### 5.2 Soak Testing

```bash
# Soak test for 8 hours with 50 users
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 50 \
        --spawn-rate 1 \
        --run-time 8h \
        --headless \
        --csv=soak_test_results
```

### 5.3 Stress Testing

```bash
# Stress test with increasing load
locust -f locustfile_enhanced.py \
        --host=http://localhost:8000 \
        --users 1000 \
        --spawn-rate 100 \
        --run-time 10m \
        --headless \
        --csv=stress_test_results
```

---

## 6. Monitoring and Metrics

### 6.1 Real-time Monitoring

```python
# monitor_load_test.py
import time
import requests
from datetime import datetime

def monitor_load_test(locust_stats_url="http://localhost:8089/stats/requests"):
    """Monitor load test in real-time"""
    while True:
        try:
            response = requests.get(locust_stats_url)
            stats = response.json()
            
            total_rps = stats['total_rps']
            failures = stats['failures']
            avg_response_time = stats['avg_response_time']
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] RPS: {total_rps:.2f}, Failures: {failures}, Avg RT: {avg_response_time:.2f}ms")
            
            # Alert if performance degrades
            if avg_response_time > 1000:
                print("⚠️  WARNING: Average response time > 1000ms")
            if failures > 10:
                print("⚠️  WARNING: High failure count")
                
        except Exception as e:
            print(f"Error monitoring: {e}")
            
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    monitor_load_test()
```

### 6.2 Integration with Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'locust'
    static_configs:
      - targets: ['localhost:8089']
    metrics_path: '/metrics'
```

---

## 7. Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify API is running and accessible |
| High failure rate | Check API logs for errors |
| Slow response times | Check server resources (CPU, memory) |
| Rate limit errors | Adjust spawn rate or user count |
| Memory issues in JMeter | Increase heap: `export JVM_ARGS="-Xmx4g"` |
| Locust workers not connecting | Check network connectivity and firewall |
| High error rates | Check authentication tokens and permissions |

---

## Conclusion

The enhanced load testing setup provides comprehensive coverage of the AI Platform API with realistic scenarios and advanced monitoring capabilities. Regular load testing ensures the API remains performant and reliable under various load conditions.

**Last Updated**: December 2025