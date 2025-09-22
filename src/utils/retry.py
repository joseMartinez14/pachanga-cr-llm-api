from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class ParseError(Exception):
    pass


retry_parse = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(ParseError),
)