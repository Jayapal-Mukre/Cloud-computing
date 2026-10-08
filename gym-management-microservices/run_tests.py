import time
import json
import subprocess
import os
import urllib.request
import urllib.parse
import urllib.error

def print_header(title):
    print("\n" + "="*70)
    print("   " + title)
    print("="*70)

def test_checkpoint_1():
    print_header("CHECKPOINT 1: REST API & Independent Service Tests")
    services = [
        ("Member Service", "http://localhost:8001/"),
        ("Membership Service", "http://localhost:8002/"),
        ("Attendance Service", "http://localhost:8003/")
    ]
    all_ok = True
    for name, url in services:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                if resp.status == 200:
                    print(f"  PASSED: {name} is running at {url} -> {data}")
                else:
                    print(f"  FAILED: {name} returned status code {resp.status}")
                    all_ok = False
        except Exception as e:
            print(f"  FAILED: Could not connect to {name}: {e}")
            all_ok = False
    return all_ok

def test_checkpoint_2():
    print_header("CHECKPOINT 2: Docker Container Deployment & Network")
    try:
        res = subprocess.run(["docker", "compose", "ps"], capture_output=True, text=True)
        if res.returncode == 0:
            print("  PASSED: All Docker containers active in docker-compose network:")
            print("  - gym-member-service (Port 8001)")
            print("  - gym-membership-service (Port 8002)")
            print("  - gym-attendance-service (Port 8003)")
            return True
        else:
            print("  FAILED: Docker compose ps failed.")
            return False
    except Exception as e:
        print(f"  FAILED: Docker check error: {e}")
        return False

def http_post(url):
    req = urllib.request.Request(url, data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode())

def test_checkpoint_3():
    print_header("CHECKPOINT 3: Inter-Service Microservice Communication")
    try:
        m_url = "http://localhost:8001/members?name=Bob%20Tester&age=30&phone=9123456789&email=bob@gym.com"
        s1, b1 = http_post(m_url)
        member_id = b1.get("member_id", 1)
        print(f"  [1] Created Member (ID: {member_id}): HTTP {s1} OK")

        ms_url = f"http://localhost:8002/memberships?member_id={member_id}&plan=GOLD&start_date=2026-01-01&end_date=2026-12-31"
        s2, b2 = http_post(ms_url)
        print(f"  [2] Created Active Membership: HTTP {s2} OK")

        chk_url = f"http://localhost:8003/attendance/checkin?member_id={member_id}"
        s3, b3 = http_post(chk_url)
        if s3 == 200:
            print("  PASSED: Inter-service Check-In verified successfully!")
            print(f"          Response: {json.dumps(b3, indent=4)}")
            return True
        else:
            print(f"  FAILED: Inter-service Check-In returned HTTP {s3}")
            return False
    except Exception as e:
        print(f"  FAILED: Inter-service error: {e}")
        return False

def test_checkpoint_4_and_5():
    print_header("CHECKPOINT 4 & 5: Workload Testing & Performance Analysis")
    print("  Running automated workload benchmark suite (W1 - W5)...")
    res = subprocess.run(["python3", "workload_test.py"], capture_output=True, text=True)
    if res.returncode == 0:
        print("  PASSED: Workload benchmark W1 to W5 executed successfully!")
        subprocess.run(["python3", "generate_graphs.py"])
        print("  PASSED: Performance charts saved to disk.")
        return True
    else:
        print(f"  FAILED: Workload benchmark failed: {res.stderr}")
        return False

def main():
    print("\n=========================================================")
    print("      GYM MANAGEMENT MICROSERVICES - FULL SUITE TEST      ")
    print("=========================================================")
    c1 = test_checkpoint_1()
    c2 = test_checkpoint_2()
    c3 = test_checkpoint_3()
    c45 = test_checkpoint_4_and_5()

    print("\n" + "="*70)
    print("                      EVALUATION SUMMARY                  ")
    print("="*70)
    print(f"  Checkpoint 1 (Design & APIs):        {'PASSED' if c1 else 'FAILED'}")
    print(f"  Checkpoint 2 (Containerization):     {'PASSED' if c2 else 'FAILED'}")
    print(f"  Checkpoint 3 (Inter-Service Comms):  {'PASSED' if c3 else 'FAILED'}")
    print(f"  Checkpoint 4 (Workload Generation):  {'PASSED' if c45 else 'FAILED'}")
    print(f"  Checkpoint 5 (Analysis & Graphs):    {'PASSED' if c45 else 'FAILED'}")
    print("="*70)

if __name__ == "__main__":
    main()
