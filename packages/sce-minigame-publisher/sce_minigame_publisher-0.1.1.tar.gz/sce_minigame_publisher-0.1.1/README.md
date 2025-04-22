# auto-publish

TapTap SCE小游戏自动发布工具，用于自动化发布和管理小游戏项目。


## 功能特点

- 自动化处理游戏资源（图片、文件夹等）
- 支持批量上传游戏文件
- 自动将图片转换为 base64 编码
- 支持自定义配置参数
- 提供详细的错误处理和日志输出

## 使用方法

1. 配置 `minigame_config.json` 文件，设置相关参数
2. 将游戏资源文件放置在指定位置
3. 运行主程序：
   ```bash
   python sce_minigame_publisher.py
   ```

### 命令行参数

```bash
# 使用默认配置文件 (minigame_config.json)
python sce_minigame_publisher.py

# 指定配置文件
python sce_minigame_publisher.py -c path/to/your/config.json

# 显示详细日志
python sce_minigame_publisher.py --verbose

# 自定义API URL
python sce_minigame_publisher.py --url http://your-api-url.com

# 自定义内容类型
python sce_minigame_publisher.py --content-type "application/json"

# 显示版本信息
python sce_minigame_publisher.py -v
```

| 参数 | 描述 |
|------|------|
| `-c, --config` | 配置文件路径 (默认: minigame_config.json) |
| `-v, --version` | 显示版本信息 |
| `--verbose` | 显示详细日志 |
| `--url` | 自定义API URL (默认值已内置) |
| `--content-type` | 内容类型 (默认: application/json) |

## 配置文件说明

配置文件 `minigame_config.json` 包含以下主要部分：

```json
{
    "token": "your-auth-token",
    "data": {
        "projectID": "your-project-id",
        "tapID": 123456,
        "title": "游戏标题",
        "outDirectory": "path/to/game/folder",
        "screenOrientation": "portrait or landscape",
        "description": "游戏描述",
        "tags": ["标签1", "标签2"],
        "versionName": "1.0.0",
        "banner": ["path/to/banner.png"],
        "icon": ["path/to/icon.png"],
        "screenshots": ["path/to/screenshot1.png", "path/to/screenshot2.png"]
    }
}
```

## 注意事项

1. 确保所有图片文件都存在且格式正确
2. 游戏资源文件夹中的文件将被自动转换为 base64 编码
3. 请妥善保管 API token，不要泄露
4. 认证令牌必须在配置文件中通过 `token` 字段设置，且只能包含ASCII字符
5. 建议在发布前先进行测试

## 常见问题解决

如果您在发布过程中遇到问题，请检查：
1. 配置文件是否正确
2. token 是否有效，是否只包含ASCII字符
3. 图片路径是否正确
4. 游戏文件夹是否存在

## 依赖项

- Python 3.6+
- requests

## 许可证

MIT 