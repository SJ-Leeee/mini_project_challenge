from email_validator import validate_email, EmailNotValidError

def is_valid_email(email: str) -> bool:
    """
    이메일 형식을 검증하는 함수.

    Args:
        email (str): 검사할 이메일 문자열

    Returns:
        bool: 유효한 형식이면 True, 아니면 False
    """

    try:
        valid = validate_email(email)
        return True, valid.normalized
    except EmailNotValidError:
        return False

def is_valid_password(password: str) -> bool:
    """
    비밀번호가 최소 길이 요건 (8자 이상)을 만족하는지 확인하는 함수.

    Args:
        password (str): 검사할 비밀번호 문자열

    Returns:
        bool: 유효하면 True, 아니면 False
    """

    return len(password) >= 8
