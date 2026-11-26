# COSTWAY Design Radar — GitHub 版

1. 新建公开 GitHub 仓库 `design-radar`（默认 main 分支）。此方案仅存公开竞品信息，网页和历史截图均公开；不要添加内部数据。若公司要求私密共享，先确认 GitHub 套餐或改用公司托管。
2. 解压 ZIP，把全部文件（包括隐藏的 `.github/workflows/radar.yml`）上传到仓库根目录。使用 GitHub 网页时可单独创建该路径并粘贴 YAML，避免漏传隐藏目录。
3. Settings → Pages → Build and deployment → Source 选择 GitHub Actions。Settings → Actions → General 确认允许 Actions 及工作流写入仓库（组织策略可能限制）。
4. Actions → Design Radar → Run workflow → main → Run workflow。等待结果，查看部署步骤输出的 Pages URL。将 URL 分享给设计团队。
5. 默认 UTC 00:17 / 08:17 / 16:17，实际运行可能延迟。公开仓库的定时工作流可能因长期无活动而停用；需检查。私有仓库可能受分钟数和 Pages 套餐限制。首次巡检可能遇到反爬或网络错误，页面明确显示失败，不伪造截图。

首屏 PC 1440×900 / Mobile 390×844。阈值 8%，保存每设备最近10个变化版本，稳定时不重复保存。Git 历史仍会累积，定期检查仓库大小。仅截图首屏，不是全页；自动变化是候选，需人工复核。截图可能涉及第三方版权，请遵循网站条款及公司政策。没有真实截图前页面显示等待采集。

通知：Pages 发布后，可使用 notifications.json 作为 ChatGPT 定时巡检的公开数据源；目前未接入现有任务，需要真实 URL。GitHub Pages 是静态页面，不能直接推送 ChatGPT 消息。
