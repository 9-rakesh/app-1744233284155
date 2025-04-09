import time
import logging
from typing import Callable, Dict, Any, Optional, List, Tuple
from pathlib import Path
import csv
import statistics
from functools import wraps
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class PerformanceUtils:
    @staticmethod
    def measure_latency(func: Callable) -> Callable:
        """Decorator to measure and log function execution time"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            logger.info(f"{func.__name__} executed in {elapsed:.4f}s")
            return result
        return wrapper

    @staticmethod
    def benchmark(test_func: Callable, 
                 iterations: int = 10,
                 warmup: int = 2) -> Dict[str, float]:
        """Run performance benchmark with warmup cycles"""
        # Warmup runs
        for _ in range(warmup):
            test_func()

        # Actual measurements
        timings = []
        for i in range(iterations):
            start_time = time.perf_counter()
            test_func()
            timings.append(time.perf_counter() - start_time)
        
        return {
            "iterations": iterations,
            "min": min(timings),
            "max": max(timings),
            "mean": statistics.mean(timings),
            "median": statistics.median(timings),
            "stdev": statistics.stdev(timings) if len(timings) > 1 else 0,
            "p90": np.percentile(timings, 90),
            "p95": np.percentile(timings, 95),
            "raw_times": timings
        }

    @staticmethod
    def save_results(results: Dict[str, Any], 
                   output_dir: Path = Path("results/performance")):
        """Save benchmark results in multiple formats"""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_path = output_dir / f"benchmark_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save as CSV
        csv_path = output_dir / f"benchmark_{timestamp}.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            for k, v in results.items():
                if k != 'raw_times':
                    writer.writerow([k, v])
        
        # Save raw times
        times_path = output_dir / f"raw_times_{timestamp}.csv"
        with open(times_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Iteration', 'Time'])
            for i, t in enumerate(results['raw_times']):
                writer.writerow([i+1, t])
        
        return json_path, csv_path, times_path

    @staticmethod
    def visualize_results(results: Dict[str, Any],
                        output_dir: Path = Path("results/performance")):
        """Generate performance visualizations"""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timings = results['raw_times']
        
        # Time Series Plot
        plt.figure(figsize=(12, 6))
        plt.plot(timings, 'b-o', label='Execution Time')
        plt.axhline(y=results['mean'], color='r', linestyle='--', label='Mean')
        plt.title(f"Performance Benchmark (n={results['iterations']})")
        plt.xlabel('Iteration')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        ts_path = output_dir / f"timeseries_{timestamp}.png"
        plt.savefig(ts_path)
        plt.close()

        # Distribution Plot
        plt.figure(figsize=(12, 6))
        plt.hist(timings, bins=min(20, len(timings)//2), edgecolor='black')
        plt.title("Execution Time Distribution")
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency')
        plt.grid(True)
        dist_path = output_dir / f"distribution_{timestamp}.png"
        plt.savefig(dist_path)
        plt.close()

        return ts_path, dist_path

    @staticmethod
    def compare_results(baseline: Dict[str, Any],
                      current: Dict[str, Any],
                      output_dir: Path = Path("results/performance")) -> Path:
        """Generate comparison report between two test runs"""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        metrics = ['mean', 'median', 'p90', 'p95']
        comparison = {
            'metrics': metrics,
            'baseline': {m: baseline[m] for m in metrics},
            'current': {m: current[m] for m in metrics},
            'difference': {m: current[m] - baseline[m] for m in metrics},
            'percentage_change': {
                m: ((current[m] - baseline[m]) / baseline[m]) * 100 
                for m in metrics
            }
        }
        
        # Save comparison report
        report_path = output_dir / f"comparison_{timestamp}.json"
        with open(report_path, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        # Visual comparison
        plt.figure(figsize=(12, 6))
        x = np.arange(len(metrics))
        width = 0.35
        plt.bar(x - width/2, [baseline[m] for m in metrics], 
               width, label='Baseline')
        plt.bar(x + width/2, [current[m] for m in metrics], 
               width, label='Current')
        plt.xticks(x, metrics)
        plt.title("Performance Comparison")
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        comp_path = output_dir / f"comparison_{timestamp}.png"
        plt.savefig(comp_path)
        plt.close()
        
        return report_path, comp_path

    @staticmethod
    def load_test(test_func: Callable,
                 duration: int = 60,
                 interval: int = 5) -> Dict[str, Any]:
        """Run continuous load test"""
        start_time = time.time()
        timings = []
        
        while time.time() - start_time < duration:
            cycle_start = time.time()
            test_func()
            timings.append(time.time() - cycle_start)
            time.sleep(max(0, interval - (time.time() - cycle_start)))
        
        return {
            "duration": duration,
            "interval": interval,
            "total_cycles": len(timings),
            "throughput": len(timings) / duration,
            "timings": timings
        }
