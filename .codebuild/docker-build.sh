#!/usr/bin/env bash

# Create Dockerfiles for components
for file in config_web
do
  cp Dockerfile .codebuild/$file.app
done

# Build Docker images
for file in .codebuild/*.app
do
  tag=$(basename -- "$file" ".${file##*.}")
  docker build -t $tag -f $file .
done

