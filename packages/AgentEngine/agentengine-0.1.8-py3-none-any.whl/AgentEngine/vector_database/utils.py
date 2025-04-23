from datetime import datetime
from typing import Dict, Any, List

def format_size(size_in_bytes):
    """Convert size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def format_timestamp(timestamp_ms):
    """Convert millisecond timestamp to formatted date string"""
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def print_index_info(stats, index_name):
    """Print formatted index information"""
    print(f"\nKnowledge Base {index_name} Core Statistics:")
    
    for category, metrics in stats.items():
        print(f"\n{category}:")
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value}")

def format_search_results(results: List[Dict[str, Any]], query: str):
    """Format search results for display"""
    print(f"\nSearch results for: '{query}'")
    print("-" * 50)
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Score: {result['score']}")
        print(f"Title: {result['document']['title']}")
        print(f"Content: {result['document']['content']}")
        print("\n" + "=" * 50 + "\n") 