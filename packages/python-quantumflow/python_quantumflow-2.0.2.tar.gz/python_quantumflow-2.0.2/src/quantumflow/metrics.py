"""
Metrics and observability for QuantumFlow.
"""

import asyncio
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("quantumflow")

class Metric:
    """Base class for metrics."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def get_value(self) -> Any:
        """Get the current value of the metric."""
        raise NotImplementedError("Subclasses must implement this method")

class Counter(Metric):
    """Counter metric that only increases."""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self._value = 0
    
    def inc(self, value: int = 1):
        """Increment the counter."""
        if value < 0:
            raise ValueError("Counter can only be incremented by non-negative values")
        self._value += value
    
    def get_value(self) -> int:
        """Get the current value of the counter."""
        return self._value

class Gauge(Metric):
    """Gauge metric that can go up and down."""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self._value = 0
    
    def set(self, value: float):
        """Set the gauge value."""
        self._value = value
    
    def inc(self, value: float = 1):
        """Increment the gauge."""
        self._value += value
    
    def dec(self, value: float = 1):
        """Decrement the gauge."""
        self._value -= value
    
    def get_value(self) -> float:
        """Get the current value of the gauge."""
        return self._value

class Histogram(Metric):
    """Histogram metric for measuring distributions."""
    
    def __init__(self, name: str, description: str, buckets: List[float] = None):
        super().__init__(name, description)
        self.buckets = buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
        self._values = []
    
    def observe(self, value: float):
        """Observe a value."""
        self._values.append(value)
    
    def get_value(self) -> Dict[str, Any]:
        """Get the current value of the histogram."""
        result = {"count": len(self._values), "sum": sum(self._values), "buckets": {}}
        
        for bucket in self.buckets:
            result["buckets"][bucket] = sum(1 for v in self._values if v <= bucket)
        
        return result

# Global registry for metrics
_metrics_registry = {}

def counter(name: str, description: str) -> Counter:
    """Create or get a counter metric."""
    if name not in _metrics_registry:
        _metrics_registry[name] = Counter(name, description)
    return _metrics_registry[name]

def gauge(name: str, description: str) -> Gauge:
    """Create or get a gauge metric."""
    if name not in _metrics_registry:
        _metrics_registry[name] = Gauge(name, description)
    return _metrics_registry[name]

def histogram(name: str, description: str, buckets: List[float] = None) -> Histogram:
    """Create or get a histogram metric."""
    if name not in _metrics_registry:
        _metrics_registry[name] = Histogram(name, description, buckets)
    return _metrics_registry[name]

class MetricsServer:
    """Server for exposing metrics."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self._server = None
        self._running = False
    
    async def start(self):
        """Start the metrics server."""
        from aiohttp import web
        
        async def metrics_handler(request):
            """Handle metrics requests."""
            output = []
            
            for name, metric in _metrics_registry.items():
                output.append(f"# HELP {name} {metric.description}")
                
                if isinstance(metric, Counter):
                    output.append(f"# TYPE {name} counter")
                    output.append(f"{name} {metric.get_value()}")
                elif isinstance(metric, Gauge):
                    output.append(f"# TYPE {name} gauge")
                    output.append(f"{name} {metric.get_value()}")
                elif isinstance(metric, Histogram):
                    output.append(f"# TYPE {name} histogram")
                    value = metric.get_value()
                    
                    for bucket, count in value["buckets"].items():
                        output.append(f"{name}_bucket{{le=\"{bucket}\"}} {count}")
                    
                    output.append(f"{name}_count {value['count']}")
                    output.append(f"{name}_sum {value['sum']}")
            
            return web.Response(text="\n".join(output))
        
        app = web.Application()
        app.router.add_get("/metrics", metrics_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        self._server = runner
        self._running = True
        
        logger.info(f"Metrics server started at http://{self.host}:{self.port}/metrics")
        return self
    
    async def stop(self):
        """Stop the metrics server."""
        if self._server and self._running:
            await self._server.cleanup()
            self._running = False
            logger.info("Metrics server stopped")

async def serve_metrics(host: str = "localhost", port: int = 8000) -> MetricsServer:
    """Start a metrics server."""
    server = MetricsServer(host, port)
    return await server.start()