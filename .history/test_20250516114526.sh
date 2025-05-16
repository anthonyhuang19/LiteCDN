#!/bin/bash

echo "Running pytest tests..."

pytest test.py -v

if [ $? -eq 0 ]; then
  echo "All tests PASSED 🎉"
else
  echo "Some tests FAILED ❌"
fi
