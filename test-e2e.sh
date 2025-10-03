#!/bin/bash
# End-to-end test script for Distributed Data Analysis Platform

echo "========================================="
echo "Distributed Data Analysis Platform - E2E Test"
echo "========================================="
echo ""

API_URL="http://localhost:8000"

echo "1. Testing API Server Root Endpoint..."
curl -s $API_URL | python3 -m json.tool
echo ""

echo "2. Creating Task with Operation Code 100..."
TASK1=$(curl -s -X POST $API_URL/task -H "Content-Type: application/json" -d '{"operation_code": 100, "params": {"test": "data"}}')
TASK1_ID=$(echo $TASK1 | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "Task created: $TASK1_ID"
echo ""

echo "3. Creating Task with Operation Code 200..."
TASK2=$(curl -s -X POST $API_URL/task -H "Content-Type: application/json" -d '{"operation_code": 200, "params": {}}')
TASK2_ID=$(echo $TASK2 | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "Task created: $TASK2_ID"
echo ""

echo "4. Waiting for runner to process tasks (10 seconds)..."
sleep 10
echo ""

echo "5. Getting result for Task 1 (code 100)..."
curl -s $API_URL/result/$TASK1_ID | python3 -m json.tool
echo ""

echo "6. Getting result for Task 2 (code 200)..."
curl -s $API_URL/result/$TASK2_ID | python3 -m json.tool
echo ""

echo "7. Getting all tasks..."
curl -s $API_URL/tasks/all | python3 -m json.tool
echo ""

echo "========================================="
echo "Test completed successfully!"
echo "========================================="
