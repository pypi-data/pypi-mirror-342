from enum import Enum


class HttpStatus():
    """HTTP 状态码枚举"""
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    Range = 206

    # 重定向状态码
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304

    # 客户端错误状态码
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    PAYLOAD_TOO_LARGE = 413
    TOO_MANY_REQUESTS = 429
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # 服务器错误状态码
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

class ResponseEnum(Enum):
    """响应枚举类，包含错误代码、描述和 HTTP 状态码"""
    AccessDenied = ("AccessDenied", "访问被拒绝", HttpStatus.FORBIDDEN)
    InternalError = ("InternalError", "我们遇到了内部错误。请稍后再试。", HttpStatus.INTERNAL_SERVER_ERROR)
    InvalidArgument = ("InvalidArgument", "无效参数", HttpStatus.BAD_REQUEST)
    InvalidRequest = ("InvalidRequest", "SOAP 请求必须通过 HTTPS 连接发送。", HttpStatus.BAD_REQUEST)
    InvalidURI = ("InvalidURI", "无法解析指定的 URI。", HttpStatus.BAD_REQUEST)
    RequestTimeout = ("RequestTimeout", "您的套接字连接在超时期间内未读取或写入数据。", HttpStatus.BAD_REQUEST)
    NotFoundApi = ("NotFoundApi", "未找到 API", HttpStatus.NOT_FOUND)
    NotFoundData = ("NotFoundData", "未找到数据", HttpStatus.NOT_FOUND)
    URLExpired = ("URLExpired", "URL 已过期，请获取一个新的。", HttpStatus.FORBIDDEN)
    InvalidKey = ("InvalidKey", "无效密钥", HttpStatus.BAD_REQUEST)
    Unauthorized = ("Unauthorized", "请求需要用户身份验证", HttpStatus.UNAUTHORIZED)
    NotifyFail = ("NotifyFail", "通知失败", HttpStatus.BAD_REQUEST)
    CallbackFail = ("CallbackFail", "回调服务器失败", HttpStatus.BAD_REQUEST)
    OK = ("OK", "成功", HttpStatus.OK)
    Repeat_Request = ("Repeat_Request", "重复请求", HttpStatus.OK)
    Sign_Is_Not_Pass = ("Sign_Is_Not_Pass", "签名未通过", HttpStatus.BAD_REQUEST)
    Error_Token = ("Error_Token", "非法授权", HttpStatus.UNAUTHORIZED)
    Payload_Too_Large = ("Payload_Too_Large", "负载过大！", HttpStatus.FORBIDDEN)
    Too_Many_Request = ("Too_Many_Request", "您已被限制，请稍后再试！", HttpStatus.TOO_MANY_REQUESTS)
    Meta_Data_Error = ("Meta_Data_Error", "元数据错误！", HttpStatus.BAD_REQUEST)
    Param_Error = ("Param_Error", "参数错误", HttpStatus.BAD_REQUEST)
    Time_Error = ("Time_Error", "您的时间参数不正确或已过期！", HttpStatus.BAD_REQUEST)
    Rule_Not_Found = ("Rule_Not_Found", "规则未找到！", HttpStatus.NOT_FOUND)
    Service_Timeout = ("Service_Timeout", "服务调用超时！", HttpStatus.GATEWAY_TIMEOUT)
    Sign_Time_Is_Timeout = ("Sign_Time_Is_Timeout", "签名时间戳已超过 %s 分钟！", HttpStatus.GATEWAY_TIMEOUT)
    Sentinel_Block_Error = ("Sentinel_Block_Error", "请求被 Sentinel 阻止！", HttpStatus.BAD_REQUEST)
    Decryption_Error = (
        "Decryption_Error", "解密失败，请检查参数或密钥，或数据长度过长", HttpStatus.UNAVAILABLE_FOR_LEGAL_REASONS)
    Ecryption_Error = (
        "Ecryption_Error", "加密失败，请检查参数或密钥，或数据长度过长", HttpStatus.UNAVAILABLE_FOR_LEGAL_REASONS)
    Invalid_Xml_Data = ("Invalid_Xml_Data", "XML 数据无效。", HttpStatus.BAD_REQUEST)
    Request_Header_Too_Large = ("Request_Header_Too_Large", "请求头字段过大", HttpStatus.PAYLOAD_TOO_LARGE)
    Request_Entity_Too_Large = ("Request_Entity_Too_Large", "请求实体过大", HttpStatus.PAYLOAD_TOO_LARGE)
    Security_Forbidden = ("Security_Forbidden", "安全禁止", HttpStatus.FORBIDDEN)
    Redis_Error = ("Redis_Error", "Redis 错误", HttpStatus.INTERNAL_SERVER_ERROR)
    Mysql_Error = ("Mysql_Error", "MySQL 错误", HttpStatus.INTERNAL_SERVER_ERROR)
    Request_Header_Invalid = ("Request_Header_Invalid", "请求头错误", HttpStatus.BAD_REQUEST)
    Source_switching_Failed = ("Source_switching_Failed", "第三方服务错误", HttpStatus.INTERNAL_SERVER_ERROR)
    Third_Service_Error = ("Third_Service_Error", "第三方服务错误", HttpStatus.INTERNAL_SERVER_ERROR)
    Data_Write_Failed = ("Data_Write_Failed", "数据写入磁盘失败。", HttpStatus.BAD_REQUEST)
    File_Drop_Field = ("File_Drop_Field", "文件丢弃字段", HttpStatus.BAD_REQUEST)
    File_Create_Field = ("File_Create_Field", "文件创建字段", HttpStatus.BAD_REQUEST)
    PGsql_Error = ("PGsql_Error", "PostgreSQL 错误", HttpStatus.BAD_REQUEST)
    PGsql_Insert_Error = ("PGsql_Insert_Error", "PostgreSQL 插入错误", HttpStatus.BAD_REQUEST)
    PGsql_Update_Error = ("PGsql_Update_Error", "PostgreSQL 更新错误", HttpStatus.BAD_REQUEST)
    PGsql_Query_Error = ("PGsql_Query_Error", "PostgreSQL 查询错误", HttpStatus.BAD_REQUEST)
    Data_Not_Complete = ("Data_Not_Complete", "数据不完整！", HttpStatus.BAD_REQUEST)
    Too_Much_Data = ("Too_Much_Data", "数据过多，停止导出", HttpStatus.BAD_REQUEST)
    Table_No_UniqueIndex = ("Table_No_UniqueIndex", "", HttpStatus.BAD_REQUEST)
    Table_Parse_Failed = ("Table_Parse_Failed", "表解析失败", HttpStatus.BAD_REQUEST)
    Still_Failed_After_Retry = ("Still_Failed_After_Retry", "重试后仍然失败", HttpStatus.BAD_REQUEST)
    Zero_Export_Data = ("Zero_Export_Data", "零导出数据", HttpStatus.OK)
    Zero_Import_Data = ("Zero_Import_Data", "零导入数据", HttpStatus.OK)
    Database_Is_Empty = ("Database_Is_Empty", "数据库中的表为空", HttpStatus.OK)
    Folder_Is_Empty = ("Folder_Is_Empty", "文件夹为空", HttpStatus.OK)
    File_Is_NotExist = ("File_Is_NotExist", "文件不存在", HttpStatus.OK)
    Bucket_Not_Exist = ("Bucket_Not_Exist", "存储桶不存在", HttpStatus.BAD_REQUEST)
    Final_Faild = ("Final_Faild", "任务失败", HttpStatus.BAD_REQUEST)
    DDL_Query_Error = ("DDL_Query_Error", "查询 DDL 错误", HttpStatus.BAD_REQUEST)
    JSON_Transform_Error = ("JSON_Transform_Error", "JSON 转换错误", HttpStatus.BAD_REQUEST)
    Directory_Create_Error = ("Directory_Create_Error", "目录创建错误", HttpStatus.BAD_REQUEST)
    File_Write_Error = ("File_Write_Error", "文件写入错误", HttpStatus.BAD_REQUEST)
    Directory_Not_Exist = ("Directory_Not_Exist", "目录不存在", HttpStatus.BAD_REQUEST)
    File_Read_Error = ("File_Read_Error", "文件读取错误", HttpStatus.BAD_REQUEST)
    Sequence_Query_Error = ("Sequence_Query_Error", "序列查询错误", HttpStatus.BAD_REQUEST)
    Sequence_Create_Error = ("Sequence_Create_Error", "序列创建错误", HttpStatus.BAD_REQUEST)
    Export_File_Error = ("Export_File_Error", "导出文件错误", HttpStatus.BAD_REQUEST)
    Import_Xml_Error = ("Import_Xml_Error", "导入 XML 错误", HttpStatus.BAD_REQUEST)
    Field_Parsing_Error = ("Field_Parsing_Error", "字段解析错误", HttpStatus.BAD_REQUEST)
    Dir_TARGZ_Error = ("Dir_TARGZ_Error", "目录 TAR.GZ 错误", HttpStatus.BAD_REQUEST)
    Minio_Upload_Failed = ("Minio_Upload_Failed", "Minio 上传失败", HttpStatus.BAD_REQUEST)
    Rollback_DDL_Failed = ("Rollback_DDL_Failed", "回滚 DDL 失败", HttpStatus.BAD_REQUEST)
    Rollback_DML_Failed = ("Rollback_DML_Failed", "回滚 DML 失败", HttpStatus.BAD_REQUEST)
    Some_File_Upload_Failed = ("Some_File_Upload_Failed", "部分文件上传失败", HttpStatus.OK)
    Invalid_Tar_Data = ("Invalid_Tar_Data", "tar 名称无效。", HttpStatus.BAD_REQUEST)
    Too_Retry_Request = ("Too_Retry_Request", "您已被限制，请稍后再试！", HttpStatus.BAD_REQUEST)

    @classmethod
    def from_code(cls, code):
        """根据错误代码获取枚举项"""
        for member in cls:
            if member.value[0] == code:
                return member
        return None

    @property
    def getBusiCode(self):
        """获取错误代码"""
        return self.value[0]

    @property
    def getBusiMsg(self):
        """获取描述信息"""
        return self.value[1]

    @property
    def getHttpCode(self):
        """获取描述信息"""
        return int(self.value[2])


if __name__ == '__main__':
    print(ResponseEnum.OK.code)
    print(ResponseEnum.OK.msg)
    print(ResponseEnum.OK.HttpCode)
    # 通过错误代码获取枚举项
    code = "Too_Retry_Request"
    enum_member = ResponseEnum.from_code(code)
    if enum_member:
        print(enum_member.msg)  # 输出: 您已被限制，请稍后再试！