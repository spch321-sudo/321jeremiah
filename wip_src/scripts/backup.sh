#!/bin/bash
# 把工作區（不含 usfm_raw/大圖）備份到 321jeremiah 的 wip 分支
set -e
cd /home/claude/321jeremiah
git checkout -q -B wip
rm -rf wip_src && mkdir wip_src
cd /home/claude/jer
tar cf - scripts txt blk lesson serm ch iss blueprint.json build_review.md 2>/dev/null | (cd /home/claude/321jeremiah/wip_src && tar xf -)
find /home/claude/321jeremiah/wip_src -name __pycache__ -prune -exec rm -rf {} \; 2>/dev/null || true
cd /home/claude/321jeremiah
git add -A wip_src
git -c user.name="claude" -c user.email="noreply@anthropic.com" commit -q -m "wip: 耶利米書講義 工作區備份 $(date +%F_%H%M)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01WJZ14gNn5VtgwDGZZcUpNN" || true
git push -q origin wip 2>&1 | tail -2
git checkout -q -
echo backed-up
