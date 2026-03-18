// Node.js SDK integration tests
const { WebWeaveXClient } = require('../../sdk/node/index');

async function testNodeSDK() {
  const client = new WebWeaveXClient('http://127.0.0.1:8001');
  
  try {
    // Test crawl
    const result = await client.crawl('http://example.com');
    
    // Validate response
    if (result.status !== 200) {
      throw new Error(`Expected status 200, got ${result.status}`);
    }
    console.log('✅ Node.js SDK crawl test passed');
    
    // Validate JSON structure
    if (!result.html) {
      throw new Error('Missing html in response');
    }
    if (!result.metadata) {
      throw new Error('Missing metadata in response');
    }
    if (!result.url) {
      throw new Error('Missing url in response');
    }
    console.log('✅ Node.js SDK response structure validated');
    
    // Test JSON parsing
    if (typeof result !== 'object') {
      throw new Error('Response should be an object');
    }
    console.log('✅ Node.js SDK response is valid JSON object');
    
    return true;
  } catch (error) {
    console.error(`❌ Node.js SDK test failed: ${error.message}`);
    return false;
  }
}

testNodeSDK().then(success => {
  process.exit(success ? 0 : 1);
}).catch(error => {
  console.error(`Unexpected error: ${error}`);
  process.exit(1);
});
