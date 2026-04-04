import requests
import socket
import time

def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((host, port)) == 0
    except:
        return False

def run_smoke_test():
    print("--- Running System Smoke Test (Sanity Check) ---")
    
    # 1. Check if Backend is up
    backend_up = check_port("localhost", 8000)
    if backend_up:
        print("[OK] Backend Port (8000) is OPEN")
        try:
            r = requests.get("http://localhost:8000/health", timeout=5)
            if r.status_code == 200:
                print("[OK] Backend API is RESPONDING and HEALTHY")
            else:
                print(f"[FAIL] Backend API responded with status: {r.status_code}")
        except Exception as e:
            print(f"[FAIL] Backend API Error: {e}")
    else:
        print("[FAIL] Backend Port (8000) is CLOSED. Is the backend server running?")

    # 2. Check if Frontend is up
    frontend_port = 3000
    frontend_up = check_port("localhost", frontend_port)
    if frontend_up:
        print(f"[OK] Frontend Port ({frontend_port}) is OPEN")
    else:
        # Check alternative common port 5173 (Vite default)
        if check_port("localhost", 5173):
            print("[OK] Frontend Port (5173/Vite) is OPEN")
        else:
            print(f"[FAIL] Frontend Port is CLOSED. Is the frontend server running?")

    print("\n--- Smoke Test Complete ---")

if __name__ == "__main__":
    run_smoke_test()
