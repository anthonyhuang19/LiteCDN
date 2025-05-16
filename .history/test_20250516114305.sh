#!/bin/bash

echo "Running pytest tests..."

pytest tests/test_cache_api.py -v

if [ $? -eq 0 ]; then
  echo "All tests PASSED 🎉"
else
  echo "Some tests FAILED ❌"
fi
