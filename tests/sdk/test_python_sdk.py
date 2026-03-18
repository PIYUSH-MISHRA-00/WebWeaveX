"""Python SDK integration tests."""
import asyncio
import sys
import json
import time
sys.path.insert(0, '.')

from sdk.python.webweavex_client import WebWeaveXClient


def test_python_sdk():
    """Test Python SDK against running API server."""
    client = WebWeaveXClient('http://127.0.0.1:8001')
    
    try:
        # Test crawl
        result = client.crawl('http://example.com')
        assert result['status'] == 200, f"Expected status 200, got {result['status']}"
        assert 'html' in result, "Missing html in response"
        assert 'metadata' in result, "Missing metadata in response"
        print("✅ Python SDK crawl test passed")
        
        # Validate JSON structure
        assert isinstance(result, dict), "Response should be dict"
        assert 'url' in result, "Missing url field"
        print("✅ Python SDK response structure validated")
        
        return True
    except Exception as e:
        print(f"❌ Python SDK test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_python_sdk()
    sys.exit(0 if success else 1)
