# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - DEV

### Added 

- 添加 bilibili 直播提醒功能
- 添加 setu 随机发送二次元美少女图片
- 添加距离考研/高考/雅思/四六级/.../天数
- 添加各大高校历年分数线
- 添加各大高校研招情况
- 添加聊天机器人接口
- 添加 ChangeLog 方便了解开发过程

## [0.2.0] - 2022-10-12 - SOON

### Added

- 添加 reminder 自创建定时任务提醒功能
- 添加用户对定时任务的查询和删除
- 添加 mutimediahandler 对发送类型进行进一步封装
- 添加 timerhandler 对定时任务类任务重构并优化

### Changed

- 修改数据库为 pysqlalchemy

### Removed

- 删除 bilibili 直播提醒功能 [临时]
- 删除 gecha 相关函数 [临时]

## [0.1.1] - 2022-07-25 - LTS

### Added

- 添加 bilibililive 直播提醒功能
- 添加 gecha 相关函数 [临时]
- 添加 rolehandler 做进一步封装

### Changed

- 进一步完善权限管理机制，引入装饰器进行处理

### Fixed

- 解决 dailynews 报错问题

## [0.1.0] - 2022-07-17

### Added

- 添加服务端每日重启脚本
- 添加 addperson 处理加好友请求

### Changed

- 修改了权限管理机制，重构了 admin 相关代码并封装为 management
- 重构了所有功能的权限管理，由统一的 permission handler 处理

### Removed

- 删除了 keyword 关键词回复功能 [deprecated]
- 删除了 randcp 随机磕糖功能 [deprecated]

## [0.0.2] - 2021-11-11

### Added

- 添加 randcp 随机发 cp 短打功能
- 添加 dailynews 每日新闻功能

### Changed

- 修改数据库为异步

## [0.0.1] - 2021-10-18

### Added

- 上线 bot 内容
- 添加 admin 基础管理功能
- 添加 keyword 关键词回应功能，支持正则匹配表达式和随机回复
- 添加 liuhua 随机一言功能
- 添加 rp 今日人品功能
- 添加 selfintro 简单自我介绍功能

[unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.8...v0.1.0
[0.0.8]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1