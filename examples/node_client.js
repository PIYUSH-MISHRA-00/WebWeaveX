const { WebWeaveXClient } = require("../sdk/node/index");

async function main() {
  const client = new WebWeaveXClient("http://127.0.0.1:8001");
  const result = await client.crawl("http://example.com");
  console.log("✅ Node SDK test passed");
  console.log(result);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
