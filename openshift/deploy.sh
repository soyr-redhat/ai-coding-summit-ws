#!/bin/bash
# Deploy PyTorch MNIST Workshop to OpenShift

set -e

NAMESPACE="ai-coding-summit-neural-nets"

echo "=================================="
echo "PyTorch MNIST Workshop Deployment"
echo "=================================="
echo ""

# Apply ImageStream
echo "Creating ImageStream..."
oc apply -f imagestream-pytorch.yaml

# Apply BuildConfig
echo "Creating BuildConfig..."
oc apply -f buildconfig-pytorch.yaml

echo ""
echo "Starting build..."
oc start-build workshop-pytorch-mnist -n ${NAMESPACE} --follow

echo ""
echo "=================================="
echo "Build complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Go to RHOAI Dashboard → Settings → Notebook Images"
echo "2. Import new image:"
echo "   image-registry.openshift-image-registry.svc:5000/${NAMESPACE}/workshop-pytorch-mnist:latest"
echo "3. Create a workbench using the new image"
echo ""
