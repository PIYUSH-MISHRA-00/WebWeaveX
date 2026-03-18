# Phase 10 powershell script
Write-Host "Re-running EVERYTHING..."

# CLI
python cli/webweavex.py crawl https://example.com > phase10_cli.txt 2>&1

# Packages
pip install . > phase10_pip.txt 2>&1
cd sdk/node; npm pack > ../../phase10_npm.txt 2>&1; cd ../..
cd sdk/dart; dart pub get > ../../phase10_pub.txt 2>&1; cd ../..
cd sdk/java; mvn clean install > ../../phase10_mvn_java.txt 2>&1; cd ../..
cd sdk/kotlin; mvn clean install > ../../phase10_mvn_kotlin.txt 2>&1; cd ../..

# Website
cd website; npm run build > ../phase10_website.txt 2>&1; cd ..

Write-Host "Phase 10 Core re-runs complete."
