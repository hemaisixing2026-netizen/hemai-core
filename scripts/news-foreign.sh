#!/bin/bash
# 思行外网权威新闻聚合 v2
# 源: Reuters/Bloomberg/BBC/FT/Guardian/Wired/MIT Tech Review/Ars Technica
export https_proxy=http://172.21.32.1:7899 http_proxy=http://172.21.32.1:7899

pull_google() { curl -sL --max-time 10 "https://news.google.com/rss/search?q=$1&hl=en-US&gl=US&ceid=US:en" 2>/dev/null | grep -oP '<title>[^<]+</title>' | grep -v 'Google News' | head -$2 | sed 's/<[^>]*>//g' | while read l; do echo "  📰 $l"; done; }
pull_rss() { curl -sL --max-time 10 "$1" 2>/dev/null | grep -oP '<title>[^<]+</title>' | grep -v "$2" | head -$3 | sed 's/<[^>]*>//g' | while read l; do echo "  📰 $l"; done; }

echo "🌍 外网权威新闻 · $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "=== Reuters ===" && pull_google "site:reuters.com+when:1d" 8
echo ""
echo "=== Bloomberg ===" && pull_google "site:bloomberg.com+markets+when:1d" 6
echo ""
echo "=== Financial Times ===" && pull_google "site:ft.com+when:1d" 5
echo ""
echo "=== BBC ===" && pull_google "site:bbc.com+when:1d" 5
echo ""
echo "=== The Guardian ===" && pull_google "site:theguardian.com+when:1d" 4
echo ""
echo "=== Wired ===" && pull_google "site:wired.com+when:1d" 4
echo ""
echo "=== MIT Tech Review ===" && pull_rss "https://www.technologyreview.com/feed/" "MIT Technology Review\|The Download" 5
echo ""
echo "=== Ars Technica ===" && pull_rss "https://feeds.arstechnica.com/arstechnica/index" "Ars Technica" 3
echo ""
echo "源: Reuters/Bloomberg/BBC/FT/Guardian/Wired/MIT Tech Review/Ars Technica"
