#!/bin/bash

# Define versions and URLs
GO_VERSION="1.21.0"
GO_TAR="go${GO_VERSION}.linux-arm64.tar.gz"
GO_URL="https://dl.google.com/go/${GO_TAR}"
BLOBFUSE2_REPO="https://github.com/Azure/azure-storage-fuse.git"

# Update and install necessary packages
sudo apt update
sudo apt install -y build-essential cmake libcurl4-openssl-dev libfuse3-dev libssl-dev uuid-dev wget git

# Download and install Go
echo "Downloading Go ${GO_VERSION}..."
wget "${GO_URL}"

echo "Removing old Go installation..."
sudo rm -rf /usr/local/go

echo "Installing Go ${GO_VERSION}..."
sudo tar -C /usr/local -xzf "${GO_TAR}"

# Update PATH for Go
echo "Updating PATH..."
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Verify Go installation
echo "Verifying Go installation..."
go version

# Clone the Blobfuse2 repository
echo "Cloning Blobfuse2 repository..."
git clone "${BLOBFUSE2_REPO}"
cd azure-storage-fuse

# Build Blobfuse2
echo "Building Blobfuse2..."
go build -o blobfuse2

# Move blobfuse2 to /usr/local/bin
echo "Moving blobfuse2 to /usr/local/bin..."
sudo mv blobfuse2 /usr/local/bin/

# Verify the blobfuse2 command
echo "Verifying Blobfuse2 installation..."
blobfuse2 --help

echo "Blobfuse2 installation complete."
