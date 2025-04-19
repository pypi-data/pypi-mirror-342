# benchmark.py
"""
A simple benchmark for measuring ingest_urls and query_knowledge performance.
"""
import time
from rag_server.server import ingest_urls, query_knowledge


def benchmark_ingest(urls, repeats: int = 3):
    """Benchmark the ingest_urls function."""
    times = []
    for i in range(repeats):
        start = time.perf_counter()
        sid = ingest_urls(urls)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"Run {i+1}/{repeats} ingest: {elapsed:.3f}s (session_id={sid})")
    avg = sum(times) / len(times)
    print(f"Average ingest time: {avg:.3f}s\n")
    return sid


def benchmark_query(session_id, question: str, repeats: int = 3):
    """Benchmark the query_knowledge function."""
    times = []
    for i in range(repeats):
        start = time.perf_counter()
        resp = query_knowledge(session_id, question)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"Run {i+1}/{repeats} query: {elapsed:.3f}s (response length={len(resp)})")
    avg = sum(times) / len(times)
    print(f"Average query time: {avg:.3f}s\n")


def main():
    # Sample URLs to benchmark (adjust as needed)
    sample_urls = ["https://b.zmtcdn.com/investor-relations/681c57ac651e6e8f54c263ffbfc1e0b9_1737369246.pdf"] * 2
    print("--- Benchmarking ingest_urls ---")
    sid = benchmark_ingest(sample_urls, repeats=5)
    print("--- Benchmarking query_knowledge ---")
    benchmark_query(sid, "What is this document about?", repeats=5)


if __name__ == "__main__":
    main() 