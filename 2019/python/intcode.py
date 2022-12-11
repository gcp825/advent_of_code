class IntcodeComputer:
    
    def __init__(self, **kwargs): 

        self.mode = 'return' if kwargs.get('mode','yield') == 'return' else 'yield'
        self.pointer = 0
        self.output = []
        self.relative_base = 0
        if kwargs.get('load',None) is not None: self.load(kwargs['load']) 
        else: self.addr = {}

        inp = kwargs.get('input',[])
        self.input = inp if type(inp) == list else list(inp) if type(inp) == tuple else [inp] if type(inp) in (int,float,str) else []

        self.first_state = self.freeze_state()
        self.last_state = None
        self.active = True

    def __str__(self):  return "I'm an intcode computer"

    def freeze_state(self): 
        
        return (self.mode, self.pointer, self.relative_base, dict(self.addr.items()), [] + self.input, [] + self.output)

    def reset(self,factory_reset=False):

        self.mode, self.pointer, self.relative_base, ad, inp, outp = self.first_state if factory_reset else self.last_state
        self.addr = dict(ad.items())
        self.input = [] + inp
        self.output = [] + outp
        self.last_state = None
        self.active = True

    def load(self,filepath):

        self.addr = dict([(i,int(x)) for i,x in enumerate(open(filepath,'r').read().strip('\n').split(','))])   

    def read(self,inp):

        self.input += inp if type(inp) == list else list(inp) if type(inp) == tuple else [inp] if type(inp) in (int,float,str) else []
        
    def set_addr(self,addr,val):
        
        self.addr[addr] = val

    def dry_run(self,inp=None):

        out = self.run(inp)
        self.reset()
        return out
  
    def run(self,inp=None):

        def _decode(n,i,modes,target='r'):  

            mode = modes[n-1:n]
            if mode == '0': lookup = self.addr.get(i+n,0);  offset = 0
            if mode == '1': lookup = i+n;                   offset = 0
            if mode == '2': lookup = self.addr.get(i+n,0);  offset = self.relative_base

            return lookup+offset if target == 'w' else self.addr.get(lookup+offset,0)

        def _parse_instr(n):

            param = {1:4,2:4,3:2,4:2,5:3,6:3,7:4,8:4,9:2,99:0}
            op = int(('0'+str(n))[-2:]);  p = param[op];   modes = str(n).zfill(p+min(p,1))[:-2][::-1]
            return op, p, modes


        self.active = True
        last_state = self.freeze_state()
        if inp is not None: self.read(inp) 

        i = self.pointer;  end = len(self.addr)
        while 0 <= i < end:

            op, p, modes = _parse_instr(self.addr[i]);  reset = False
            args = (i,modes);  targs = (i,modes,'w')

            try:
                if   op == 99: break
                elif op == 3:  self.addr[_decode(p-1,*targs)] = self.input.pop(0)

                elif op == 1:  self.addr[_decode(p-1,*targs)] = _decode(1,*args) + _decode(2,*args)
                elif op == 2:  self.addr[_decode(p-1,*targs)] = _decode(1,*args) * _decode(2,*args)
                elif op == 7:  self.addr[_decode(p-1,*targs)] = 1 if _decode(1,*args) < _decode(2,*args) else 0
                elif op == 8:  self.addr[_decode(p-1,*targs)] = 1 if _decode(1,*args) == _decode(2,*args) else 0

                elif op == 5:  reset, i = (True, _decode(2,*args)) if _decode(1,*args) != 0 else (False,i)
                elif op == 6:  reset, i = (True, _decode(2,*args)) if _decode(1,*args) == 0 else (False,i)

                elif op == 9:  self.relative_base += _decode(1,*args)

                elif op == 4:  self.output += [_decode(p-1,*args)]

            except (KeyError, IndexError):
                break
            else:
                if not reset: i += p
                if op == 4 and self.mode == 'yield': break

        self.pointer = i
        self.last_state = last_state
        if len(self.output) == 0:  self.active = False

        out = (self.output.pop(0) if self.mode == 'yield' and len(self.output) > 0 else 
               None               if len(self.output) == 0 else 
               self.output[0]     if len(self.output) == 1 else 
               self.output)

        return out
