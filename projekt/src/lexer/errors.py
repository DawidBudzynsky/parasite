class LexerError(Exception):
    pass


ERROR_MESSAGES = {
    "invalid_escape": "Error, invalid escaping sequence",
    "unclosed_string": "Error, unclosed string;",
    "token_build_failed": "Error, lexer was unable to create token;",
    "string_length": "Error, string too long, 200 char is max;",
}
