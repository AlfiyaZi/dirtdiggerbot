#!/bin/bash
docker run --rm --name=findthedirt -v $(pwd):/usr/src/app:Z findthedirt:latest
