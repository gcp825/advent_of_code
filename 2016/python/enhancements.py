############################################################################################################################
#  Enhancements to out-of-the-box python functions to add extra functionality, flexibility, or to enhance code readability
############################################################################################################################

#  Multi-directional sort with abstraction of itemgetter and directional defaults for trailing keys with unspecified order
def sorted_(obj,*args,reverse=None,order=''):
    
    from operator import itemgetter
    from copy import deepcopy
    
    if len(args) == 0:
        return sorted(obj,reverse=True if reverse is None and order[:1].lower() == 'd' else False)
    else: 
        data = deepcopy(obj) 
        keys = list(reversed(args))
        reverse = False if reverse is None else reverse
        dflt = 'd' if reverse is True else 'a'
        dirs = list(reversed([reverse]*len(keys) if len(order) == 0 else [True if d == 'd' else False for d in list((order[:len(keys)]+(len(keys)*dflt))[:len(keys)])]))

        for i,k in enumerate(keys):
            data.sort(key=itemgetter(k),reverse=dirs[i])
        return data
    
    
#  Translate with abstraction of translation table and pad parameter to avoid repetition of repeated replacement values
def translate_(x,find,repl,delete='',pad=' '):

    pad = (pad[:1]+' ')[:1];   diff = max(0,len(find)-len(repl));   repl = repl[0:len(find)]+(pad*diff)
    return x.translate(''.maketrans(find,repl,delete))


#  Multi value replace allowing avoidance of repeated replacement values
def replace_(x,find,repl):

    repl = (repl,) if type(repl) in (int,str) else repl;   pad = repl[-1:];  diff = max(0,len(find)-len(repl));   repl = repl[0:len(find)] + pad*diff;   data = x
    
    for i,f in enumerate(find): data = data.replace(f,repl[i])
    return data

