const { WebWeaveXClient } = require("../sdk/node/index.js");

async function main() {
  const client = new WebWeaveXClient("http://localhost:8000");
  const result = await client.crawl("https://example.com");
  console.log(result);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
