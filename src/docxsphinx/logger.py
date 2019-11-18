import sys
import logging

logging.basicConfig(
    filename='docx.log',
    filemode='w',
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)s:  %(message)s"
)
logger = logging.getLogger('docx')


def dprint(_func=None, **kw):
    """Print debug information."""
    logger.info('-'*50)
    # noinspection PyProtectedMember
    f = sys._getframe(1)
    if kw:
        text = ', '.join('%s = %s' % (k, v) for k, v in kw.items())
    else:
        text = dict((k, repr(v)) for k, v in f.f_locals.items() if k != 'self')
        text = str(text)

    if _func is None:
        _func = f.f_code.co_name

    logger.info(' '.join([_func, text]))
    
    