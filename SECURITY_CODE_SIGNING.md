# Code Signing Implementation Guide

## Overview

This document provides guidelines and implementation details for code signing certificates within the AI Platform project. Code signing ensures the authenticity and integrity of software releases.

## 1. Code Signing Fundamentals

### What is Code Signing?
Code signing is a security technology that uses cryptographic signatures to verify the authenticity and integrity of software. It provides:
- **Authentication**: Verifies the publisher's identity
- **Integrity**: Ensures code hasn't been tampered with
- **Non-repudiation**: Prevents publishers from denying code release

### Benefits for AI Platform
- Secure distribution of SDK packages
- Verified container images
- Trusted plugin installations
- Protected model artifacts

## 2. Certificate Authority Options

### Public CAs
| Provider | Cost | Features | Integration |
|----------|------|----------|------------|
| DigiCert | $$$ | Enterprise features | API, CLI |
| Sectigo | $$ | Wide browser support | API, CLI |
| GlobalSign | $$$ | Advanced validation | API, CLI |
| Let's Encrypt | Free | Basic code signing | ACME protocol |

### Private CAs
| Solution | Deployment | Management | Cost |
|----------|------------|------------|------|
| HashiCorp Vault | On-prem/Cloud | Automated | $$$ |
| AWS Private CA | Cloud | Managed | $$ |
| Azure Private CA | Cloud | Managed | $$ |
| Self-hosted OpenSSL | On-prem | Manual | Free |

## 3. Implementation Strategy

### Certificate Hierarchy
```
Root CA (Offline)
├── Code Signing CA (Online)
│   ├── Development Certificates
│   ├── Production Certificates
│   └── Release Certificates
└── Timestamping CA (Online)
    └── Timestamping Service
```

### Key Management
- **Key Storage**: Hardware Security Modules (HSM) or cloud KMS
- **Key Rotation**: Annual for CA keys, 3-year for end-entity
- **Backup**: Encrypted offline storage with M of N scheme
- **Access Control**: Role-based with approval workflows

## 4. Python Package Signing

### Sigstore Integration
```bash
# Install sigstore tools
pip install sigstore

# Sign Python package
python -m sigstore sign \
    --identity-token $GITHUB_TOKEN \
    --oidc-issuer https://token.actions.githubusercontent.com \
    dist/aiplatform-*.whl

# Verify signature
python -m sigstore verify \
    --certificate dist/aiplatform-*.whl.crt \
    --signature dist/aiplatform-*.whl.sig \
    dist/aiplatform-*.whl
```

### GitHub Actions Integration
```yaml
# .github/workflows/sign-release.yml
name: Sign Release

on:
  release:
    types: [published]

jobs:
  sign:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install sigstore build
      
      - name: Build package
        run: python -m build
      
      - name: Sign packages
        run: |
          for file in dist/*.whl dist/*.tar.gz; do
            python -m sigstore sign \
              --identity-token ${{ secrets.GITHUB_TOKEN }} \
              --oidc-issuer https://token.actions.githubusercontent.com \
              $file
          done
      
      - name: Upload signatures
        run: |
          gh release upload ${{ github.ref_name }} dist/*.sig dist/*.crt
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Verification in Installation
```python
# setup.py or installation script
import subprocess
import sys
from pathlib import Path

def verify_signature(package_path):
    """Verify package signature using sigstore"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'sigstore', 'verify',
            '--certificate', f'{package_path}.crt',
            '--signature', f'{package_path}.sig',
            package_path
        ], capture_output=True, text=True, check=True)
        
        print("Signature verification successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Signature verification failed: {e.stderr}")
        return False

# Usage in installation process
if __name__ == "__main__":
    package = sys.argv[1] if len(sys.argv) > 1 else "aiplatform-latest.whl"
    if verify_signature(package):
        # Proceed with installation
        subprocess.run([sys.executable, '-m', 'pip', 'install', package])
    else:
        print("Installation aborted due to signature verification failure")
        sys.exit(1)
```

## 5. Container Image Signing

### Cosign Integration
```bash
# Install cosign
go install github.com/sigstore/cosign/v2/cmd/cosign@latest

# Sign container image
cosign sign \
  --key env://COSIGN_PRIVATE_KEY \
  --tlog-upload=true \
  aiplatform/aiplatform:latest

# Verify signature
cosign verify \
  --key env://COSIGN_PUBLIC_KEY \
  aiplatform/aiplatform:latest
```

### Keyless Signing with GitHub Actions
```yaml
# .github/workflows/sign-container.yml
name: Sign Container

on:
  push:
    branches: [main]
    paths:
      - 'sdk/**'
      - 'Dockerfile'

jobs:
  sign:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
      
      - name: Sign container image
        run: |
          cosign sign \
            --yes \
            ghcr.io/${{ github.repository }}:latest
```

## 6. Docker Content Trust

### Enable DCT
```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1
export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="your-passphrase"

# Sign image
docker push aiplatform/aiplatform:latest

# Verify image
docker pull aiplatform/aiplatform:latest
```

### Repository Delegation
```bash
# Initialize repository
docker trust key generate aiplatform-root
docker trust signer add --key aiplatform-root.pub aiplatform-root aiplatform/aiplatform

# Add targets
docker trust repository generate aiplatform/aiplatform
docker trust signer add --key aiplatform-targets.pub aiplatform-targets aiplatform/aiplatform
```

## 7. Model Artifact Signing

### Model Signing Script
```python
# scripts/sign_model.py
import hashlib
import json
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class ModelSigner:
    def __init__(self, private_key_path):
        with open(private_key_path, 'rb') as key_file:
            self.private_key = load_pem_private_key(
                key_file.read(),
                password=None,
            )
    
    def calculate_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def sign_model(self, model_path, metadata=None):
        """Sign model file and create signature"""
        # Calculate model hash
        model_hash = self.calculate_hash(model_path)
        
        # Create signature data
        signature_data = {
            "model_hash": model_hash,
            "model_path": model_path,
            "timestamp": str(datetime.utcnow()),
            "metadata": metadata or {}
        }
        
        # Sign the hash
        signature = self.private_key.sign(
            model_hash.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Save signature
        signature_path = f"{model_path}.sig"
        with open(signature_path, 'wb') as f:
            f.write(signature)
        
        # Save metadata
        metadata_path = f"{model_path}.meta"
        with open(metadata_path, 'w') as f:
            json.dump(signature_data, f, indent=2)
        
        return signature_path, metadata_path

# Usage
if __name__ == "__main__":
    signer = ModelSigner("keys/model_signing_key.pem")
    signature_file, metadata_file = signer.sign_model(
        "models/quantum_ai_model.h5",
        {"version": "1.0.0", "framework": "tensorflow"}
    )
    print(f"Model signed: {signature_file}, {metadata_file}")
```

### Model Verification
```python
# scripts/verify_model.py
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

class ModelVerifier:
    def __init__(self, public_key_path):
        with open(public_key_path, 'rb') as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read())
    
    def calculate_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def verify_model(self, model_path, signature_path):
        """Verify model signature"""
        # Calculate model hash
        model_hash = self.calculate_hash(model_path)
        
        # Load signature
        with open(signature_path, 'rb') as f:
            signature = f.read()
        
        # Verify signature
        try:
            self.public_key.verify(
                signature,
                model_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

# Usage
if __name__ == "__main__":
    verifier = ModelVerifier("keys/model_verification_key.pem")
    is_valid = verifier.verify_model(
        "models/quantum_ai_model.h5",
        "models/quantum_ai_model.h5.sig"
    )
    print(f"Model verification: {'PASSED' if is_valid else 'FAILED'}")
```

## 8. Certificate Management

### Automated Renewal
```bash
# Certificate renewal script
#!/bin/bash
# renew_certificates.sh

# Check certificate expiration
openssl x509 -in certs/codesign.crt -noout -enddate

# Renew if expiring in 30 days
if openssl x509 -in certs/codesign.crt -noout -checkend 2592000; then
    echo "Certificate valid for more than 30 days"
else
    echo "Renewing certificate..."
    # Implementation depends on CA
fi
```

### Certificate Revocation
```python
# scripts/revoke_certificate.py
import requests
import json

def revoke_certificate(cert_serial, reason="keyCompromise"):
    """Revoke certificate via ACME protocol or CA API"""
    revoke_data = {
        "certificate": cert_serial,
        "reason": reason
    }
    
    response = requests.post(
        "https://ca.example.com/revoke",
        json=revoke_data,
        headers={"Authorization": "Bearer $CA_API_TOKEN"}
    )
    
    if response.status_code == 200:
        print(f"Certificate {cert_serial} revoked successfully")
        return True
    else:
        print(f"Failed to revoke certificate: {response.text}")
        return False
```

## 9. Security Best Practices

### Key Protection
- Store private keys in HSM or cloud KMS
- Use hardware tokens for highest security
- Implement key access logging
- Regular key rotation

### Signing Process
- Sign in secure environment
- Use automated signing pipelines
- Implement approval workflows
- Maintain signing logs

### Verification Requirements
- Always verify before execution
- Fail securely if verification fails
- Log verification attempts
- Alert on verification failures

## 10. Compliance and Auditing

### Audit Logging
```python
# security/audit_logger.py
import logging
import json
from datetime import datetime

class SigningAuditLogger:
    def __init__(self, log_file="signing_audit.log"):
        self.logger = logging.getLogger("signing_audit")
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_signing_event(self, artifact, signer, result, details=None):
        """Log signing event"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "signing",
            "artifact": artifact,
            "signer": signer,
            "result": result,
            "details": details or {}
        }
        self.logger.info(json.dumps(event))
    
    def log_verification_event(self, artifact, verifier, result, details=None):
        """Log verification event"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "verification",
            "artifact": artifact,
            "verifier": verifier,
            "result": result,
            "details": details or {}
        }
        self.logger.info(json.dumps(event))

# Usage
audit_logger = SigningAuditLogger()
audit_logger.log_signing_event(
    "models/quantum_ai_model.h5",
    "build-server-01",
    "success",
    {"hash": "a1b2c3d4..."}
)
```

### Compliance Reporting
```python
# security/compliance_report.py
import json
from datetime import datetime, timedelta

class ComplianceReporter:
    def __init__(self, audit_log="signing_audit.log"):
        self.audit_log = audit_log
    
    def generate_compliance_report(self, period_days=30):
        """Generate compliance report for specified period"""
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        events = []
        
        # Parse audit log
        with open(self.audit_log, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    event_time = datetime.fromisoformat(event['timestamp'])
                    if event_time > cutoff_date:
                        events.append(event)
                except json.JSONDecodeError:
                    continue
        
        # Generate report
        report = {
            "report_date": datetime.utcnow().isoformat(),
            "period_days": period_days,
            "total_events": len(events),
            "signing_events": len([e for e in events if e['event_type'] == 'signing']),
            "verification_events": len([e for e in events if e['event_type'] == 'verification']),
            "failed_verifications": len([e for e in events if e['event_type'] == 'verification' and e['result'] == 'failed']),
            "compliance_status": "PASS" if all(e['result'] == 'success' for e in events if 'result' in e) else "FAIL"
        }
        
        return report

# Generate and save report
reporter = ComplianceReporter()
report = reporter.generate_compliance_report()
with open("compliance_report.json", 'w') as f:
    json.dump(report, f, indent=2)
```

## 11. Integration with CI/CD

### GitHub Actions Workflow
```yaml
# .github/workflows/secure-build.yml
name: Secure Build and Sign

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-sign:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install sigstore build cryptography
      
      - name: Run security checks
        run: |
          # SAST scanning
          bandit -r sdk/
          # Dependency scanning
          pip-audit .
      
      - name: Build package
        run: python -m build
      
      - name: Sign packages with Sigstore
        run: |
          for file in dist/*; do
            python -m sigstore sign \
              --identity-token ${{ secrets.GITHUB_TOKEN }} \
              --oidc-issuer https://token.actions.githubusercontent.com \
              $file
          done
      
      - name: Verify signatures
        run: |
          for file in dist/*; do
            if [[ $file == *.whl ]] || [[ $file == *.tar.gz ]]; then
              python -m sigstore verify \
                --certificate ${file}.crt \
                --signature ${file}.sig \
                $file
            fi
          done
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: signed-packages
          path: |
            dist/*.whl
            dist/*.tar.gz
            dist/*.sig
            dist/*.crt
```

## 12. Monitoring and Alerting

### Signature Verification Monitoring
```python
# monitoring/signature_monitor.py
import time
import requests
from datetime import datetime

class SignatureMonitor:
    def __init__(self, alert_webhook=None):
        self.alert_webhook = alert_webhook
        self.verification_failures = 0
    
    def check_signature_endpoint(self, url):
        """Check signature verification endpoint"""
        try:
            response = requests.get(f"{url}/health/signature")
            data = response.json()
            
            if not data.get('signature_verification', True):
                self.verification_failures += 1
                self.alert_signature_failure(url, data)
            else:
                self.verification_failures = 0
                
        except Exception as e:
            self.verification_failures += 1
            self.alert_endpoint_failure(url, str(e))
    
    def alert_signature_failure(self, url, details):
        """Alert on signature verification failure"""
        if self.alert_webhook and self.verification_failures > 3:
            alert_data = {
                "alert": "Signature Verification Failed",
                "url": url,
                "details": details,
                "timestamp": datetime.utcnow().isoformat()
            }
            requests.post(self.alert_webhook, json=alert_data)
    
    def alert_endpoint_failure(self, url, error):
        """Alert on endpoint failure"""
        if self.alert_webhook:
            alert_data = {
                "alert": "Signature Endpoint Unreachable",
                "url": url,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            }
            requests.post(self.alert_webhook, json=alert_data)

# Run monitoring
if __name__ == "__main__":
    monitor = SignatureMonitor("https://alerts.example.com/webhook")
    while True:
        monitor.check_signature_endpoint("https://api.aiplatform.io")
        time.sleep(300)  # Check every 5 minutes
```

## Conclusion

This code signing implementation provides a comprehensive security framework for the AI Platform project. By following these guidelines, we ensure the authenticity and integrity of all software releases, from Python packages to container images and model artifacts.

Regular review and updates to this implementation will maintain its effectiveness against evolving security threats.