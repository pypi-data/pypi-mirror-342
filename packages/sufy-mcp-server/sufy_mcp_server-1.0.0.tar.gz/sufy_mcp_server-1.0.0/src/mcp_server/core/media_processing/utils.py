from urllib import parse
from botocore import auth as s3_auth
from botocore import awsrequest
from botocore import credentials as s3_credentials

from ...config import config

_FUNC_PREFIXES = [
    "imgmogr/"
]

async def url_add_processing_func(cfg: config.Config, url: str, func: str) -> str:
    func_items = func.split("/")
    func_prefix = func_items[0]

    url_info = parse.urlparse(url)
    new_query, expire = _remove_query_sign_info(url_info.query)
    new_query = _query_add_processing_func(new_query, func, func_prefix)
    new_query = parse.quote(new_query, safe='&=')
    url_info = url_info._replace(query=new_query)
    new_url = parse.urlunparse(url_info)
    new_url = await _presigned_url(cfg, str(new_url), expire)
    return str(new_url)


def _query_add_processing_func(query: str, func: str, func_prefix: str) -> str:
    queries = query.split("&")
    if '' in queries:
        queries.remove('')

    # query 中不包含任何数据
    if len(queries) == 0:
        return func

    # funcs 会放在第一个元素中
    first_query = parse.unquote(queries[0])

    # funcs 不存在
    if len(first_query) == 0:
        queries.insert(0, func)
        return "&".join(queries)

    # first_query 不是 funcs
    if not _is_func(first_query):
        queries.insert(0, func)
        return "&".join(queries)

    # 移除后面的 =
    first_query = first_query.removesuffix("=")
    queries.remove(queries[0])

    # 未找到当前类别的 func
    if first_query.find(func_prefix) < 0:
        func = first_query + "|" + func
        queries.insert(0, func)
        return "&".join(queries)

    query_funcs = first_query.split("|")
    if '' in query_funcs:
        query_funcs.remove('')

    # 只有一个 func，且和当前 func 相同，拼接其后
    if len(query_funcs) == 1:
        func = first_query + func.removeprefix(func_prefix)
        queries.insert(0, func)
        return "&".join(queries)

    # 多个 func，查看最后一个是否和当前 func 匹配
    last_func = query_funcs[-1]

    # 最后一个不匹配，只用管道符拼接
    if last_func.find(func_prefix) < 0:
        func = first_query + "|" + func
        queries.insert(0, func)
        return "&".join(queries)

    # 最后一个匹配，则直接拼接在后面
    func = first_query + func.removeprefix(func_prefix)
    queries.insert(0, func)
    return "&".join(queries)


async def _presigned_url(cfg: config.Config, original_url: str, expires: int = 3600) -> str:
    try:
        # 创建凭证对象
        creds = s3_credentials.Credentials(
            access_key=cfg.access_key,
            secret_key=cfg.secret_key,
        )

        # 创建 AWS 请求对象
        request = awsrequest.AWSRequest(
            method="GET",
            url=original_url,
            headers={}
        )

        # 创建签名器（禁用路径转义）
        signer = s3_auth.S3SigV4QueryAuth(
            credentials=creds,
            region_name=cfg.region_name,
            expires=expires,
            service_name="s3",
        )
        signer.URI_ESCAPE_PATH = False  # 对应 DisableURIPathEscaping=True

        # 进行签名（直接修改请求对象）
        signer.add_auth(request)

        # 构造最终 URL
        signed_url = request.url
        return signed_url

    except Exception as e:
        raise Exception(f"Presign url:{original_url} error: {e}")


_S3_SIGN_URL_QUERY_KEYS_EXPIRES = "x-amz-expires"
_S3_SIGN_URL_QUERY_KEYS = [
    _S3_SIGN_URL_QUERY_KEYS_EXPIRES,
    "x-amz-algorithm",
    "x-amz-credential",
    "x-amz-date",
    "x-amz-signedheaders",
    "x-amz-signature",
]

def _remove_query_sign_info(query: str) -> (str, int):
    queries = query.split("&")
    if '' in queries:
        queries.remove('')

    expire = 3600
    new_queries = []
    for item in queries:
        # 移除签名信息
        found_sign_info = ""
        for sign_info in _S3_SIGN_URL_QUERY_KEYS:
            if item.lower().find(sign_info) >= 0:
                found_sign_info = sign_info
                break

        if len(found_sign_info) == 0:
            # 不是签名信息
            new_queries.append(item)
        elif found_sign_info == _S3_SIGN_URL_QUERY_KEYS_EXPIRES:
            expires = item.split("=")
            if len(expires) == 2:
                expire = int(expires[1])

    return "&".join(new_queries), expire

def _is_func(func: str) -> bool:
    for prefix in _FUNC_PREFIXES:
        if func.startswith(prefix):
            return True
    return False
