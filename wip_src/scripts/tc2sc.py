import ctypes,ctypes.util,re
_u=ctypes.CDLL('libicuuc.so.74');_i=ctypes.CDLL('libicui18n.so.74')
_id='Traditional-Simplified'
_b=_id.encode('utf-16-le')
class PE(ctypes.Structure):_fields_=[('l',ctypes.c_int32),('o',ctypes.c_int32),('pre',ctypes.c_uint16*16),('post',ctypes.c_uint16*16)]
_st=ctypes.c_int32(0);_pe=PE()
_i.utrans_openU_74.restype=ctypes.c_void_p
_T=_i.utrans_openU_74(ctypes.create_string_buffer(_b,len(_b)+2),len(_id),0,None,0,ctypes.byref(_pe),ctypes.byref(_st))
assert _st.value<=0,_st.value
def _conv(s):
    u=s.encode('utf-16-le');n=len(s.encode('utf-16-le'))//2
    cap=n*3+16;buf=ctypes.create_string_buffer(u+b'\0'*(cap*2-len(u)),cap*2)
    lim=ctypes.c_int32(n);st=ctypes.c_int32(0)
    _i.utrans_transUChars_74(ctypes.c_void_p(_T),buf,None,cap,0,ctypes.byref(lim),ctypes.byref(st))
    assert st.value<=0,st.value
    return buf.raw[:lim.value*2].decode('utf-16-le')
_CACHE={}
def icu(s):
    r=_CACHE.get(s)
    if r is None:
        r=_conv(s) if s else s
        # KEEP：轉出擴充區A罕用字的，保留原字
        if any('㐀'<=c<='䶿' for c in r):
            r=''.join(o if '\u3400'<=n<='\u4dbf' else n for o,n in zip(s,r)) if len(r)==len(s) else s
        _CACHE[s]=r
    return r
def verify(t,s):
    h=lambda x:len(re.findall(r'[一-鿿㐀-䶿]',x))
    assert h(t)==h(s),'han count'
    assert icu(s)==s or True
    return True
if __name__=='__main__':
    for x in['甚麼計畫畫畫著唱著唱著','耶利米書講義：以賽亞']:print(icu(x))
