from enum import IntEnum

class ErrorCode(IntEnum):
    """
    HTTP 状态码及业务语义别名
    基于 RFC 7231 & RFC 7807 规范
    """

    # --- 2xx Success (通常不作为错误码，但为了完整性列出) ---
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # --- 400 Bad Request: 客户端请求语法错误 ---
    # 适用：JSON 格式错误、缺少必填头信息、参数类型错误
    BAD_REQUEST = 400
    INVALID_PARAMETER = 400  # 别名：参数无效（通用）
    MALFORMED_REQUEST = 400  # 别名：请求格式错误（如 JSON 解析失败）

    # --- 401 Unauthorized: 未认证 ---
    # 适用：Token 缺失、Token 过期、密码错误
    # 注意：REST 中 401 特指“身份未验证”，而非“权限不足”
    UNAUTHORIZED = 401
    NOT_LOGGED_IN = 401      # 别名：未登录
    TOKEN_EXPIRED = 401      # 别名：令牌过期
    TOKEN_INVALID = 401      # 别名：令牌无效

    # --- 403 Forbidden: 禁止访问 ---
    # 适用：已登录但无权操作、IP 被封禁、账号被冻结
    FORBIDDEN = 403
    PERMISSION_DENIED = 403  # 别名：权限不足
    ACCESS_DENIED = 403      # 别名：拒绝访问
    ACCOUNT_SUSPENDED = 403  # 别名：账号被挂起

    # --- 404 Not Found: 资源不存在 ---
    # 适用：ID 对应的记录不存在、URL 错误
    NOT_FOUND = 404
    RESOURCE_NOT_FOUND = 404 # 别名：资源未找到

    # --- 405 Method Not Allowed: 方法禁用 ---
    # 适用：用 POST 请求只支持 GET 的接口
    METHOD_NOT_ALLOWED = 405

    # --- 409 Conflict: 资源冲突 ---
    # 适用：注册重复邮箱、并发修改冲突（乐观锁失败）
    CONFLICT = 409
    RESOURCE_ALREADY_EXISTS = 409 # 别名：资源已存在
    STATE_CONFLICT = 409          # 别名：状态冲突（如：只能取消“进行中”的订单，但当前是“已完成”）

    # --- 415 Unsupported Media Type: 不支持的媒体类型 ---
    # 适用：上传了不支持的文件格式，或 Content-Type 不对
    UNSUPPORTED_MEDIA_TYPE = 415
    INVALID_FILE_TYPE = 415       # 别名：文件类型错误

    # --- 422 Unprocessable Entity: 语义错误 (WebDAV扩展，现常用) ---
    # 适用：格式正确但逻辑校验失败（如：密码长度不够、库存不足）
    VALIDATION_ERROR = 422
    BUSINESS_LOGIC_ERROR = 422    # 别名：业务逻辑校验失败

    # --- 429 Too Many Requests: 请求过多 ---
    # 适用：限流、防止暴力破解
    TOO_MANY_REQUESTS = 429
    RATE_LIMIT_EXCEEDED = 429     # 别名：超出频率限制

    # --- 500 Internal Server Error: 服务器内部错误 ---
    # 适用：未捕获的异常、代码 Bug
    INTERNAL_ERROR = 500
    SERVER_EXCEPTION = 500        # 别名：服务器异常

    # --- 501 Not Implemented: 未实现 ---
    # 适用：接口已定义但功能尚未开发
    NOT_IMPLEMENTED = 501

    # --- 502 Bad Gateway: 网关错误 ---
    # 适用：上游服务（如数据库、微服务）响应无效
    BAD_GATEWAY = 502
    UPSTREAM_ERROR = 502          # 别名：上游服务错误

    # --- 503 Service Unavailable: 服务不可用 ---
    # 适用：服务器维护、过载、数据库连接池满
    SERVICE_UNAVAILABLE = 503
    MAINTENANCE_MODE = 503        # 别名：维护模式