from flask import current_app, request


def get_locale():
    lang = request.cookies.get('lang')
    if lang in current_app.config['LANGUAGES']:
        current_app.logger.debug(f'🌍 Language (cookie): {lang}')
        return lang

    best_lang = request.accept_languages.best_match(
        current_app.config['LANGUAGES']
    )

    current_app.logger.debug(f'🌍 Language (header): {best_lang}')
    return best_lang
