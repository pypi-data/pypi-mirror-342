def 屏蔽网页资源(驱动器对象, 屏蔽列表):
    """
    使用 Chrome DevTools 协议屏蔽网页中指定的资源类型。

    适用于自动化浏览器环境，用户可自定义需要屏蔽的资源 URL 模式，
    提高加载速度，节省带宽资源。(此功能应该在初始化浏览器后调用)

    参数：
        - 驱动器对象：Selenium Chrome 浏览器驱动对象。
        - 屏蔽列表（list）：包含 URL 通配符的字符串列表，表示要屏蔽的资源。例如：
            [
                "*.css",  # 样式表
                "*.svg",  # 矢量图标
                "*.png", "*.jpg", "*.jpeg", "*.gif",  # 图片
                "*.woff", "*.woff2", "*.ttf", "*.otf",  # 字体
                "*.mp4", "*.mp3", "*.webm"  # 视频/音频
            ]

    注意事项：
        1. 需使用 Chrome 浏览器并通过 Selenium 启动。
        2. CDP 功能只在本地或 DevTools 协议支持的浏览器中生效。
        3. URL 模式支持通配符 *，匹配任意字符。

    返回值：
        - 无返回值。操作将直接影响当前页面会话。
    """
    try:
        驱动器对象.execute_cdp_cmd("Network.enable", {})
        驱动器对象.execute_cdp_cmd("Network.setBlockedURLs", {
            "urls": 屏蔽列表
        })
    except Exception:
        pass