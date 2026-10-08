import logging, re
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        msg = str(record.getMessage())
        msg = re.sub(r'(password|token|otp|secret)["\']?\s*[:=]\s*["\']?[^"\'\s]+', r'\1=***REDACTED***', msg, flags=re.I)
        record.msg = msg
        return True