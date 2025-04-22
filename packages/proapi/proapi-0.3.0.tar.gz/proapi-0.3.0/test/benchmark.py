"""
Benchmark script to compare ProAPI with FastAPI.

This script creates equivalent applications in both frameworks and measures their performance.
"""

import time
import json
import statistics
import subprocess
import requests
import sys
import os

# Add parent directory to path to import proapi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_proapi_app():
    """Create a ProAPI application for benchmarking."""
    from proapi import ProAPI
    
    app = ProAPI(debug=False)
    
    @app.get("/")
    def index(request):
        return {"message": "Hello, World!"}
    
    @app.get("/json")
    def json_endpoint(request):
        return {"message": "Hello, World!", "timestamp": time.time()}
    
    @app.get("/params/{id}")
    def params(id, request):
        return {"id": id, "query": request.query_params}
    
    @app.get("/heavy")
    def heavy(request):
        # Create a large JSON response
        items = []
        for i in range(1000):
            items.append({
                "id": i,
                "name": f"Item {i}",
                "value": i * 3.14
            })
        
        return {
            "count": len(items),
            "items": items
        }
    
    return app

def create_fastapi_app():
    """Create a FastAPI application for benchmarking."""
    try:
        from fastapi import FastAPI
        
        app = FastAPI()
        
        @app.get("/")
        def index():
            return {"message": "Hello, World!"}
        
        @app.get("/json")
        def json_endpoint():
            return {"message": "Hello, World!", "timestamp": time.time()}
        
        @app.get("/params/{id}")
        def params(id: str, q: str = None):
            return {"id": id, "query": {"q": q}}
        
        @app.get("/heavy")
        def heavy():
            # Create a large JSON response
            items = []
            for i in range(1000):
                items.append({
                    "id": i,
                    "name": f"Item {i}",
                    "value": i * 3.14
                })
            
            return {
                "count": len(items),
                "items": items
            }
        
        return app
    except ImportError:
        print("FastAPI not installed. Skipping FastAPI benchmark.")
        return None

def run_proapi_server(fast_mode=False):
    """Run a ProAPI server for benchmarking."""
    app = create_proapi_app()
    
    # Start the server in a separate process
    import multiprocessing
    
    def run_server():
        if fast_mode:
            app.run(host="127.0.0.1", port=8000, fast=True)
        else:
            app.run(host="127.0.0.1", port=8000)
    
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    
    # Wait for the server to start
    time.sleep(2)
    
    return server_process

def run_fastapi_server():
    """Run a FastAPI server for benchmarking."""
    try:
        import uvicorn
        app = create_fastapi_app()
        
        if app is None:
            return None
        
        # Start the server in a separate process
        import multiprocessing
        
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8000)
        
        server_process = multiprocessing.Process(target=run_server)
        server_process.start()
        
        # Wait for the server to start
        time.sleep(2)
        
        return server_process
    except ImportError:
        print("Uvicorn not installed. Skipping FastAPI benchmark.")
        return None

def benchmark_server(name, endpoints):
    """Benchmark a server."""
    results = {}
    
    for endpoint in endpoints:
        url = f"http://127.0.0.1:8000{endpoint}"
        
        # Warm up
        for _ in range(10):
            requests.get(url)
        
        # Benchmark
        times = []
        for _ in range(100):
            start = time.time()
            response = requests.get(url)
            end = time.time()
            times.append((end - start) * 1000)  # Convert to milliseconds
        
        # Calculate statistics
        avg = statistics.mean(times)
        median = statistics.median(times)
        p95 = sorted(times)[int(len(times) * 0.95)]
        
        results[endpoint] = {
            "avg": avg,
            "median": median,
            "p95": p95
        }
    
    return results

def print_results(name, results):
    """Print benchmark results."""
    print(f"=== {name} ===")
    for endpoint, stats in results.items():
        print(f"Endpoint: {endpoint}")
        print(f"  Average: {stats['avg']:.2f} ms")
        print(f"  Median: {stats['median']:.2f} ms")
        print(f"  P95: {stats['p95']:.2f} ms")
    print()

def main():
    """Run the benchmark."""
    endpoints = ["/", "/json", "/params/123?q=test", "/heavy"]
    
    # Benchmark ProAPI (standard mode)
    print("Starting ProAPI (standard mode) benchmark...")
    proapi_server = run_proapi_server(fast_mode=False)
    proapi_results = benchmark_server("ProAPI (standard mode)", endpoints)
    proapi_server.terminate()
    proapi_server.join()
    
    # Benchmark ProAPI (fast mode)
    print("Starting ProAPI (fast mode) benchmark...")
    proapi_fast_server = run_proapi_server(fast_mode=True)
    proapi_fast_results = benchmark_server("ProAPI (fast mode)", endpoints)
    proapi_fast_server.terminate()
    proapi_fast_server.join()
    
    # Benchmark FastAPI
    fastapi_results = None
    fastapi_server = run_fastapi_server()
    if fastapi_server:
        print("Starting FastAPI benchmark...")
        fastapi_results = benchmark_server("FastAPI", endpoints)
        fastapi_server.terminate()
        fastapi_server.join()
    
    # Print results
    print("\n=== BENCHMARK RESULTS ===\n")
    print_results("ProAPI (standard mode)", proapi_results)
    print_results("ProAPI (fast mode)", proapi_fast_results)
    if fastapi_results:
        print_results("FastAPI", fastapi_results)
    
    # Compare results
    print("=== COMPARISON ===")
    for endpoint in endpoints:
        print(f"Endpoint: {endpoint}")
        proapi_time = proapi_results[endpoint]["avg"]
        proapi_fast_time = proapi_fast_results[endpoint]["avg"]
        
        print(f"  ProAPI (standard): {proapi_time:.2f} ms")
        print(f"  ProAPI (fast): {proapi_fast_time:.2f} ms")
        
        if fastapi_results:
            fastapi_time = fastapi_results[endpoint]["avg"]
            print(f"  FastAPI: {fastapi_time:.2f} ms")
            
            # Calculate speedup
            proapi_vs_fastapi = (fastapi_time / proapi_time - 1) * 100
            proapi_fast_vs_fastapi = (fastapi_time / proapi_fast_time - 1) * 100
            
            print(f"  ProAPI (standard) vs FastAPI: {proapi_vs_fastapi:.2f}%")
            print(f"  ProAPI (fast) vs FastAPI: {proapi_fast_vs_fastapi:.2f}%")
        
        print()

if __name__ == "__main__":
    main()
